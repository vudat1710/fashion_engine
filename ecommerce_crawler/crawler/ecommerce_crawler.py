from scrapy import Spider, Request
from scrapy_splash import SplashRequest
import json


class ShopeeCrawler(Spider):
    custom_settings = {
        'FEED_URI': 'data/shopee/posts.jsonl',
        'IMAGES_STORE': 'data/shopee/images/'
    }

    def __init__(self, name=None, **kwargs):
        super(ShopeeCrawler, self).__init__(name=name, **kwargs)
        self.num_pages = kwargs.get('num_pages', 50)
        self.num_items_per_page = kwargs.get('num_items_per_page', 100)
        self.match_ids = kwargs.get('match_ids', [])

    def start_requests(self):
        for match_id, additional_fields in self.match_ids:
            yield Request(
                url=f"https://shopee.vn/api/v2/search_items/?by=relevancy&limit={self.num_items_per_page}&match_id={match_id}&newest={0 * self.num_items_per_page}&order=desc&page_type=search&version=2",
                callback=self.parse,
                meta={
                    'current_page': 0,
                    'match_id': match_id,
                    'additional_fields': additional_fields
                }
            )

    def parse(self, response):
        additional_fields = response.meta['additional_fields']
        data = json.loads(response.body_as_unicode())
        items = [
            {
                'itemid': item['itemid'],
                # 'image_ids': item['images'],
                'brand': item['brand'],
                'price': item['price'],
                'price_before_discount': item['price_before_discount'],
                'price_max': item['price_max'],
                'price_max_before_discount': item['price_max_before_discount'],
                'price_min': item['price_min'],
                'price_min_before_discount': item['price_min_before_discount'],
                'currency': item['currency'],
                'raw_discount': item['raw_discount'],
                'item_rating': item['item_rating']['rating_star'],
                'catid': item['catid'],
                'liked_count': item['liked_count'],
                'name': item['name'],
                'shopid': item['shopid'],
                'options': {
                    tier_variation['name']: tier_variation['options']
                    for tier_variation in item['tier_variations']
                },
                **additional_fields
            }
            for item in data['items']
        ]

        for item in items:
            yield Request(
                url=f"https://shopee.vn/api/v2/item/get?itemid={item['itemid']}&shopid={item['shopid']}",
                callback=self.parse_item,
                meta=item
            )

        next_page = response.meta['current_page'] + 1
        if next_page < self.num_pages:
            match_id = response.meta['match_id']
            yield Request(
                url=f"https://shopee.vn/api/v2/search_items/?by=relevancy&limit={self.num_items_per_page}&match_id={match_id}&newest={next_page * self.num_items_per_page}&order=desc&page_type=search&version=2",
                callback=self.parse,
                meta={
                    'current_page': next_page,
                    'match_id': match_id,
                    'additional_fields': additional_fields
                }
            )

    def parse_item(self, response):
        item = response.meta
        data = json.loads(response.body_as_unicode())
        yield {
            **item,
            'categories': [category['display_name'] for category in data['item']['categories']],
            'description': data['item']['description'],
            'image_urls': [f'https://cf.shopee.vn/file/{image_id}' for image_id in data['item']['images']]
        }


class ShopeeShopCrawler(Spider):
    custom_settings = {
        'FEED_URI': 'data/shopee/shops.jsonl',
    }

    def __init__(self, name=None, **kwargs):
        super(ShopeeShopCrawler, self).__init__(name=name, **kwargs)
        self.shop_ids = kwargs.get('shop_ids', [])

    def start_requests(self):
        for shop_id in self.shop_ids:
            yield Request(
                url=f"https://shopee.vn/api/v2/shop/get?is_brief=1&shopid={shop_id}",
                callback=self.parse
            )

    def parse(self, response):
        data = json.loads(response.body_as_unicode())['data']
        return {
            "shopid": data['shopid'],
            "rating_bad": data['rating_bad'],
            "cancellation_rate": data['cancellation_rate'],
            "is_official_shop": data['is_official_shop'],
            "preparation_time": data['preparation_time'],
            "follower_count": data['follower_count'],
            "shop_location": data['shop_location'],
            "description": data['description'],
            "rating_good": data['rating_good'],
            "account": {
                "username": data['account']['username'],
                "following_count": data['account']['following_count'],
                "total_avg_star": data['account']['total_avg_star'],
                "portrait": data['account']['portrait'],
            },
            "response_rate": data['response_rate'],
            "name": data['name'],
            "rating_star": data['rating_star'],
            "country": data['country'],
            "cover": data['cover'],
            "place": data['place']
        }


class TikiCrawler(Spider):
    custom_settings = {
        'FEED_URI': 'data/tiki/posts.jsonl',
        'IMAGES_STORE': 'data/tiki/images/',
    }

    xpath = {
        'product_id': "//*[@class='product-box-list']//*[@data-seller-product-id]/@data-id",
        'next_page': "//*[@class='list-pager']//a[@class='next']/@href",
        'image': "//*[@class='group-images']//*[@class='images']//img/@src"
    }

    def __init__(self, name=None, **kwargs):
        super(TikiCrawler, self).__init__(name=name, **kwargs)
        self.start_urls = kwargs.get('start_urls', [])
        self.num_pages = kwargs.get('num_pages', 50)

    def start_requests(self):
        for start_url, additional_fields in self.start_urls:
            yield Request(
                url=start_url,
                callback=self.parse,
                meta={
                    'current_page': 0,
                    'additional_fields': additional_fields,
                }
            )

    def parse(self, response):
        product_ids = response.xpath(self.xpath['product_id']).getall()
        for product_id in product_ids:
            yield Request(
                url=f"https://tiki.vn/api/v2/products/{product_id}",
                callback=self.parse_post,
                meta=response.meta
            )

        next_page = response.xpath(self.xpath['next_page']).get()
        next_page_number = response.meta['current_page'] + 1
        if next_page_number < self.num_pages and next_page is not None:
            yield Request(
                url=response.urljoin(next_page),
                callback=self.parse,
                meta={
                    'current_page': next_page_number,
                    'additional_fields': response.meta['additional_fields'],
                }
            )

    def parse_post(self, response):
        additional_fields = response.meta['additional_fields']
        data = json.loads(response.body_as_unicode())
        item = {
            'itemid': data.get('id'),
            'name': data.get('name'),
            'brand': data['brand']['name'],
            'price': data['price'],
            'price_before_discount': data['list_price'],
            'currency': 'VND',
            'raw_discount': data['discount_rate'],
            'item_rating': data['rating_average'],
            'catid': data['categories']['id'],
            'liked_count': data['favourite_count'],
            'shopid': data['current_seller']['id'],
            'categories': data['productset_group_name'].split('/'),
            'options': self.get_options(data.get('configurable_options')),
            'description': data['description'],
            'image_urls': None,
            'post_url': f"https://tiki.vn/{data.get('url_path')}",
            **additional_fields,
            'shop_info': data['current_seller'],
        }
        yield Request(
            url=item["post_url"],
            callback=self.parse_post_images,
            meta=item,
        )

    def parse_post_images(self, response):
        item = response.meta
        image_urls = [
            image.replace('/w80/', '/w780/')
            for image in response.xpath(self.xpath['image']).getall()
        ]
        return {
            **item,
            'image_urls': image_urls,
        }

    @staticmethod
    def get_options(options):
        if options is None:
            return None
        return {
            option['name']: [item['label'] for item in option['values']]
            for option in options
        }


class TikiShopCrawler(Spider):
    custom_settings = {
        'FEED_URI': 'data/tiki/shops.jsonl',
    }

    def __init__(self, name=None, **kwargs):
        super(TikiShopCrawler, self).__init__(name=name, **kwargs)
        self.shop_ids = kwargs.get('shop_ids', [])

    def start_requests(self):
        for shop_id in self.shop_ids:
            yield Request(
                url=f"https://seller-store-api.tiki.vn/seller-profiles?id={shop_id}"
            )

    def parse(self, response):
        data = json.loads(response.body_as_unicode())
        return {
            'shopid': data['id'],
            'name': data['name'],
            'logo': data['logo'],
            'slug': data['url_slug'],
            'shop_url': f'https://tiki.vn/cua-hang/{data["url_slug"]}',
        }


class LazadaCrawler(Spider):
    custom_settings = {
        'FEED_URI': 'data/lazada/posts.jsonl',
        'IMAGES_STORE': 'data/lazada/images/',
    }

    lua_script = """
    function main(splash, args)
      splash:init_cookies(splash.args.cookies)
      assert(splash:go(args.url))
      assert(splash:wait(0.5))
      data = splash:evaljs("window.pageData")
      return {
        cookies = splash:get_cookies(),
        html = splash:html(),
        data = data,
      }
    end 
    """

    def __init__(self, name=None, **kwargs):
        super(LazadaCrawler, self).__init__(name=name, **kwargs)
        self.start_urls = kwargs.get('start_urls', [])
        self.num_pages = kwargs.get('num_pages', 50)

    def start_requests(self):
        for start_url, additional_fields in self.start_urls:
            yield SplashRequest(
                start_url.replace("___NUM___", str(1)),
                callback=self.parse,
                args={
                    "lua_source": self.lua_script,
                    "cookies": {}
                },
                endpoint='execute',
                meta={
                    'start_url': start_url,
                    'additional_fields': additional_fields,
                    'current_page': 1,
                }
            )

    def parse(self, response):
        additional_fields = response.meta['additional_fields']

        data = response.data.get('data')
        if data is not None:
            for item in data['mods']['listItems']:
                res_item = {
                    'itemid': item.get('itemId'),
                    'name': item.get('name'),
                    'brand': item.get('brandName'),
                    'price': item['price'],
                    'price_before_discount': item['originalPrice'],
                    'currency': 'VND',
                    'raw_discount': item['discount'],
                    'item_rating': item['ratingScore'],
                    # 'catid': item['categories']['id'],
                    # 'liked_count': item['favourite_count'],
                    # 'shopid': item['current_seller']['id'],
                    'categories': item.get('categories'),
                    # 'options': self.get_options(item.get('configurable_options')),
                    'description': item['description'],
                    'image_urls': [image['image'] for image in item.get('thumbs', [])],
                    'post_url': item.get("productUrl"),
                    **additional_fields,
                    'shop_info': {
                        'shopid': item.get('mainSellerId'),
                        'place': item.get('location'),
                        'name': item.get('sellerName'),
                    }
                }
                yield res_item

        next_page = response.meta['current_page'] + 1
        if next_page <= self.num_pages:
            start_url = response.meta['start_url']
            yield SplashRequest(
                start_url.replace("___NUM___", str(next_page)),
                callback=self.parse,
                endpoint='execute',
                args={
                    "lua_source": self.lua_script,
                    "cookies": response.data['cookies'],
                },
                meta={
                    'start_url': start_url,
                    'current_page': next_page,
                    'additional_fields': additional_fields,
                }
            )


class SendoCrawler(Spider):
    custom_settings = {
        'FEED_URI': 'data/sendo/posts.jsonl',
        'IMAGES_STORE': 'data/sendo/images/',
    }

    def __init__(self, name=None, **kwargs):
        super(SendoCrawler, self).__init__(name=name, **kwargs)
        self.categories = kwargs.get('start_urls', [])
        self.num_pages = kwargs.get('num_pages', 10)

    def start_requests(self):
        for category_id, additional_fields in self.categories:
            yield Request(
                url=f"https://www.sendo.vn/m/wap_v2/category/product?category_id={category_id}&listing_algo=algo14&p=1&platform=web&s=60&sortType=listing_v2_location_desc",
                callback=self.parse,
                meta={
                    'current_page': 1,
                    'additional_fields': additional_fields,
                    'category_id': category_id,
                }
            )

    def parse(self, response):
        additional_fields = response.meta['additional_fields']
        data = json.loads(response.body_as_unicode())
        if data['status']['code'] != 200:
            self.logger.error(f'Request error from {response.request.url}')
        else:
            for item in data['result']['data']:
                path = item['cat_path'].split('.')[0]
                yield Request(
                    url=f"https://www.sendo.vn/m/wap_v2/full/san-pham/{path}?platform=web",
                    callback=self.parse_post,
                    meta={
                        'additional_fields': additional_fields,
                    }
                )

        next_page = response.meta['current_page'] + 1
        if next_page <= self.num_pages:
            category_id = response.meta['category_id']
            yield Request(
                url=f"https://www.sendo.vn/m/wap_v2/category/product?category_id={category_id}&listing_algo=algo14&p={next_page}&platform=web&s=60&sortType=listing_v2_location_desc",
                callback=self.parse,
                meta={
                    'current_page': next_page,
                    'additional_fields': additional_fields,
                    'category_id': category_id,
                }
            )

    def parse_post(self, response):
        additional_fields = response.meta['additional_fields']
        data = json.loads(response.body_as_unicode())
        item = data['result']['data']
        yield {
            'itemid': item.get('id'),
            'name': item.get('name'),
            'brand': None,
            'price': item['final_price'],
            'price_before_discount': item['price'],
            'currency': 'VND',
            'raw_discount': item['promotion_percent'],
            'item_rating': self.get_rating(item['rating_info']),
            'liked_count': item['counter_like'],
            'shopid': item['shop_info']['shop_id'],
            'categories': [category['title'] for category in item['category_info']],
            'options': {
                option['name']: [value.get('name') or value.get('value') for value in option['value']]
                for option in item['attribute']
            },
            'description': item['description'],
            'image_urls': [image['image'] for image in item['media'] if image['type'] == 'image'],
            'post_url': f"https://www.sendo.vn/{item['cat_path']}",
            **additional_fields,
            'shop_info': {
                "shopid": item['shop_info']['shop_id'],
                "preparation_time": item['shop_info']['time_prepare_product'],
                "shop_location": item['shop_info']['warehourse_region_name'],
                "rating_good": item['shop_info']['good_review_percent'],
                "response_rate": item['shop_info']['percent_response'],
                "name": item['shop_info']['shop_name'],
                "rating_star": item['shop_info']['rating_avg'],
                "cover": item['shop_info']['shop_logo'],
            }
        }

    @staticmethod
    def get_rating(rating_info):
        star1, star2, star3, star4, star5, total_rated = (
            rating_info.get('star1', 0),
            rating_info.get('star2', 0),
            rating_info.get('star3', 0),
            rating_info.get('star4', 0),
            rating_info.get('star5', 0),
            rating_info.get('total_rated', 0),
        )
        return (star1 + star2 * 2 + star3 * 3 + star4 * 4 + star5 * 5) / total_rated if total_rated > 0 else 0
