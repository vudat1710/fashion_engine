from utils import *
import os
import pandas as pd


def images_convert(images):
    return [image['path'] for image in images]


def shopee_post2standard(post):
    keep_attributes = [
        "itemid",
        "brand",
        "price",
        "price_before_discount",
        "currency",
        "raw_discount",
        "item_rating",
        "liked_count",
        "name",
        "shopid",
        "options",
        # "main_category",
        "sex",
        "categories",
        "description",
        "post_url",
    ]

    return {
        **{attribute: post[attribute] for attribute in keep_attributes},
        "images": images_convert(post['images']),
        "platform": "shopee.vn",
    }


def tiki_post2standard(post):
    keep_attributes = [
        "itemid",
        "brand",
        "price",
        "price_before_discount",
        "currency",
        "raw_discount",
        "item_rating",
        "liked_count",
        "name",
        "shopid",
        "options",
        # "main_category",
        "sex",
        "categories",
        # "description",
        "post_url",
    ]

    return {
        **{attribute: post[attribute] for attribute in keep_attributes},
        "images": images_convert(post['images']),
        "description": html2text(post["description"]),
        "platform": "tiki.vn",
    }


def sendo_post2standard(post):
    keep_attributes = [
        "itemid",
        "brand",
        "price",
        "price_before_discount",
        "currency",
        "raw_discount",
        "item_rating",
        "liked_count",
        "name",
        "shopid",
        "options",
        # "main_category",
        "sex",
        "categories",
        # "description",
        "post_url",
    ]

    return {
        **{attribute: post[attribute] for attribute in keep_attributes},
        "images": images_convert(post['images']),
        "description": html2text(post["description"]),
        "platform": "sendo.vn",
    }


def process_post(shopee_jsonl_fn, tiki_jsonl_fn, sendo_jsonl_fn, output_fn):
    shopee_posts = load_jsonl_file(shopee_jsonl_fn)
    tiki_posts = load_jsonl_file(tiki_jsonl_fn)
    sendo_posts = load_jsonl_file(sendo_jsonl_fn)

    all_posts = [
        *[shopee_post2standard(post) for post in shopee_posts],
        *[tiki_post2standard(post) for post in tiki_posts],
        *[sendo_post2standard(post) for post in sendo_posts],
    ]

    dump_jsonl_file(all_posts, output_fn)


def shopee_shop2standard(shop):
    keep_attributes = [
        "shopid",
        "follower_count",
        "name",
        "rating_star",
    ]

    return {
        **{attribute: shop[attribute] for attribute in keep_attributes},
        "shop_location": shop.get("place"),
        "platform": "shopee.vn",
    }


def tiki_shop2standard(shop):
    keep_attributes = [
        "name"
    ]

    return {
        "shopid": shop['id'],
        **{attribute: shop[attribute] for attribute in keep_attributes},
        "rating_star": 0,
        "shop_location": None,
        "platform": "tiki.vn",
    }


def sendo_shop2standar(shop):
    keep_attributes = [
        "shopid",
        "name",
        "shop_location",
        "rating_star"
    ]

    return {
        **{attribute: shop[attribute] for attribute in keep_attributes},
        "platform": "sendo.vn",
    }


def process_shop(shopee_shops, tiki_shops, sendo_shops, output_fn):
    all_shops = [
        *[shopee_shop2standard(shop) for shop in shopee_shops],
        *[tiki_shop2standard(shop) for shop in tiki_shops],
        *[sendo_shop2standar(shop) for shop in sendo_shops]
    ]

    all_shops_dict = {
        (shop["shopid"], shop["platform"]): shop
        for shop in all_shops
    }
    
    dump_jsonl_file(list(all_shops_dict.values()), output_fn)


def all_posts2image_paths_csv(posts):
    image_paths = []
    for post in posts:
        platform = post['platform'].split('.')[0]
        image_paths.extend([
            (f"{platform}_{post['itemid']}", os.path.join(platform, 'images', path))
            for path in post['images']
        ])

    item_ids, paths = zip(*image_paths)
    df = pd.DataFrame({'item_id': item_ids, 'path': paths})
    df['image_id'] = list(range(len(df)))
    df[['image_id', 'item_id', 'path']].to_csv('data/all_images_path.csv', sep='\t', index=False)


if __name__ == '__main__':
    # process_post(
    #     shopee_jsonl_fn="data/shopee/preprocess_posts.jsonl",
    #     tiki_jsonl_fn="data/tiki/posts.jsonl",
    #     sendo_jsonl_fn="data/sendo/posts.jsonl",
    #     output_fn="data/all_posts.jsonl",
    # )
    #
    # shopee_shops = load_jsonl_file('data/shopee/shops.jsonl')
    # tiki_shops = [post['shop_info'] for post in load_jsonl_file('data/tiki/posts.jsonl')]
    # sendo_shops = [post['shop_info'] for post in load_jsonl_file('data/sendo/posts.jsonl')]
    #
    # process_shop(
    #     shopee_shops=shopee_shops,
    #     tiki_shops=tiki_shops,
    #     sendo_shops=sendo_shops,
    #     output_fn='data/all_shops.jsonl',
    # )

    all_posts2image_paths_csv(load_jsonl_file('data/all_posts.jsonl'))
