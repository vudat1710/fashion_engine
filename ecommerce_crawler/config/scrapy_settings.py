SETTINGS = {
    'LOG_FILE': 'log/crawler.log',

    'ITEM_PIPELINES': {
        # 'crawler.pipelines.kafka_pipelines.KafkaItemPipeline': 300,
        'scrapy.pipelines.images.ImagesPipeline': 300
    },

    'DEPTH_PRIORITY': 1,
    # 'CONCURRENT_REQUESTS': 1,
    # 'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
    'LOG_LEVEL': 'INFO',
    'COOKIES_ENABLED': True,
    'COOKIES_DEBUG': True,
    'TELNETCONSOLE_PORT': None,
    'ROBOTSTXT_OBEY': False,
    'FEED_EXPORT_ENCODING': 'utf-8',
    'FEED_EXPORT': 'jsonlines',
    'REDIRECT_ENABLED': False,
    # 'FEED_URI': 'data.jsonl',
    # 'CLOSESPIDER_ITEMCOUNT': 1000,
    # 'DOWNLOAD_DELAY': 1,
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
}

SPLASH_SETTINGS = {
    # SPLASH SETTING
    'SPLASH_URL': "http://127.0.1.1:8050",
    'DOWNLOADER_MIDDLEWARES': {
        'scrapy_splash.SplashCookiesMiddleware': 723,
        'scrapy_splash.SplashMiddleware': 725,
        'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    },
    'SPIDER_MIDDLEWARES': {
        'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
    },
    'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter',
    'HTTPCACHE_STORAGE': 'scrapy_splash.SplashAwareFSCacheStorage',
}

SHOPEE_SHOP_URL = "https://shopee.vn/api/v2/shop/get?is_brief=1&shopid=173385614"
SHOPEE_ITEM_URL = "https://shopee.vn/api/v2/item/get?itemid=2833598869&shopid=173385614"
SHOPEE_IMAGE_URL = "https://cf.shopee.vn/file/19728bb800e3db72c742ac4cc9c056a2"

TIKI_ITEM_URL = "https://tiki.vn/api/v2/products/48498668"
