from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from scrapy.crawler import CrawlerProcess
import os

from crawler.ecommerce_crawler import ShopeeCrawler, ShopeeShopCrawler, TikiCrawler, LazadaCrawler, SendoCrawler
from config import scrapy_settings
from utils import load_jsonl_file


def crawl_shopee():
    # process.crawl(ShopeeCrawler, name="shopee", num_pages=5, num_items_per_page=100, match_ids=[
    #     *[(match_id, {'sex': 'male', 'main_category': match_id}) for match_id in
    #       ['2827', '2828', '2829', '9566', '9568', '1899', '15023', '2429']],
    #     *[(match_id, {'sex': 'female', 'main_category': match_id}) for match_id in
    #       ['1871', '2821', '2822', '1877', '2334', '1881', '2823', '13506', '1875', '9865', '16848', '161', ]],
    # ])

    shop_ids = [post['shopid'] for post in load_jsonl_file('data/shopee/posts.jsonl')]
    process.crawl(ShopeeShopCrawler, name="shopee_shop", shop_ids=set(shop_ids))


def crawl_tiki():
    process.crawl(TikiCrawler, name='tiki_post', num_pages=10, start_urls=[
        ("https://tiki.vn/ao-kieu/c935", {"main_category": "Áo kiểu", "sex": "female", }),
        ("https://tiki.vn/ao-thun-nu/c933", {'main_category': 'Áo thun', "sex": "female", }),
        ("https://tiki.vn/ao-so-mi-nu/c934", {"main_category": "Áo sơ mi", "sex": "female"}),
        ("https://tiki.vn/chan-vay-nu/c5404", {"main_category": "Chân váy", "sex": "female"}),
        ("https://tiki.vn/jumpsuits-set-do-nu/c1702", {'main_category': "Jumpsuits, set đồ nữ", "sex": "female"}),
        ("https://tiki.vn/ao-cardigan-nu/c27594", {"main_category": "Áo cardigan", "sex": "female"}),
        ("https://tiki.vn/ao-hoodie-nu/c27598", {"main_category": "Áo hoodie", "sex": "female"}),
        ("https://tiki.vn/ao-len-nu/c27596", {"main_category": "Áo len", "sex": "female"}),
        ("https://tiki.vn/quan-jean-nu/c1701", {"main_category": "Quần jean", "sex": "female"}),
        ("https://tiki.vn/quan-kaki-nu/c8385", {"main_category": "Quần kaki", "sex": "female"}),
        ("https://tiki.vn/quan-legging/c1716", {"main_category": "Quần legging", "sex": "female"}),
        ("https://tiki.vn/quan-sooc/c939", {"main_category": "Quần sooc", "sex": "female"}),
        ("https://tiki.vn/quan-thun-jogger-nu/c27602", {"main_category": "Quần thun jogger", "sex": "female"}),
        ("https://tiki.vn/thoi-trang-nu-quan-dai/c938", {"main_category": "Quần dài", "sex": "female"}),
        ("https://tiki.vn/ao-khoac-nu/c936", {"main_category": "Áo khoác", "sex": "female"}),
        ("https://tiki.vn/ao-dai/c10385", {"main_category": "Áo dài", "sex": "female"}),
        ("https://tiki.vn/dam-vay-lien/c941", {"main_category": "Đầm", "sex": "female"}),
        ("https://tiki.vn/do-vest-nu/c27586", {"main_category": "Áo vest", "sex": "female"}),

        ("https://tiki.vn/giay-dep-nam/c1686", {"main_category": "Giày dép", "sex": "male"}),
        ("https://tiki.vn/quan-jeans-nam/c920", {"main_category": "Quan jean nam", "sex": "male", }),
        ("https://tiki.vn/quan-jogger-nam/c5409", {"main_category": "Quần jogger", "sex": "male"}),
        ("https://tiki.vn/thoi-trang-nam-quan-kaki/c921", {"main_category": "Quần kaki", "sex": "male"}),
        ("https://tiki.vn/thoi-trang-nam-quan-sooc/c923", {"main_category": "Quần sooc", "sex": "male"}),
        ("https://tiki.vn/quan-tay-nam/c922", {"main_category": "Quần tây", "sex": "male"}),
        ("https://tiki.vn/ao-dai-nam/c27558", {"main_category": "Áo dài", "sex": "male"}),
        ("https://tiki.vn/ao-khoac-nam/c925", {"main_category": "Áo khoác nam", "sex": "male"}),
        ("https://tiki.vn/ao-cardigan-nam/c27552", {"main_category": "Áo cardigan", "sex": "male"}),
        ("https://tiki.vn/ao-hoodie-nam/c10382", {"main_category": "Áo hoodie", "sex": "male"}),
        ("https://tiki.vn/ao-len-nam/c27554", {"main_category": "Áo len", "sex": "male"}),
        ("https://tiki.vn/ao-so-mi-nam/c918", {"main_category": "Áo sơ mi", "sex": "male"}),
        ("https://tiki.vn/ao-thun-nam/c917", {"main_category": "Áo thun", "sex": "male"}),
    ])


def crawl_lazada():
    process.crawl(LazadaCrawler, name="lazada", num_pages=15, start_urls=[
        ("https://www.lazada.vn/ao-thoi-trang-nam/?page=___NUM___", {'main_category': "ao_thun_nam", "sex": "male"}),
        ("https://www.lazada.vn/ao-so-mi-nam/?page=___NUM___", {'main_category': "ao_so_mi_nam", "sex": "male"}),
        ("https://www.lazada.vn/ao-khoac-nam/?page=___NUM___", {'main_category': "ao_khoac_nam", "sex": "male"}),
        ("https://www.lazada.vn/quan-jeans/?page=___NUM___", {'main_category': "quan_jean_nam", "sex": "male"}),
        ("https://www.lazada.vn/quan-nam/?page=___NUM___", {'main_category': "quan_dai_nam", "sex": "male"}),
        ("https://www.lazada.vn/quan-short-nam/?page=___NUM___", {'main_category': "quan_short_nam", "sex": "male"}),
        ("https://www.lazada.vn/bo-vest-nam/?page=___NUM___", {'main_category': "do_vest_nam", "sex": "male"}),
        ("https://www.lazada.vn/ao-hoodie-cua-nam/?page=___NUM___", {'main_category': "ao_hoodie_nam", "sex": "male"}),
        ("https://www.lazada.vn/ao-sweater-cardigan-nam/?page=___NUM___", {'main_category': "ao_cardigan_nam", "sex": "male"}),
        ("https://www.lazada.vn/do-boi-nam/?page=___NUM___", {'main_category': "do_boi_nam", "sex": "male"}),
        ("https://www.lazada.vn/giay-nam-thoi-trang/?page=___NUM___", {'main_category': "giay_dep_nam", "sex": "male"}),
        ("https://www.lazada.vn/do-lot-nam/?page=___NUM___", {'main_category': "do_lot_nam", "sex": "male"}),

        ("https://www.lazada.vn/dam-nu/?page=___NUM___", {'main_category': "dam_nu", "sex": "female"}),
        ("https://www.lazada.vn/quan-dai-cho-nu/?page=___NUM___", {'main_category': "quan_dai_nu", "sex": "female"}),
        ("https://www.lazada.vn/jeans-nu/?page=___NUM___", {'main_category': "quan_jean_nu", "sex": "female"}),
        ("https://www.lazada.vn/chan-vay/?page=___NUM___", {'main_category': "chan_vay_nu", "sex": "female"}),
        ("https://www.lazada.vn/quan-short-cho-nu/?page=___NUM___", {'main_category': "quan_short_nu", "sex": "female"}),
        ("https://www.lazada.vn/ao-khoac-nu/?page=___NUM___", {'main_category': "ao_khoac_nu", "sex": "female"}),
        ("https://www.lazada.vn/ao-hoodies-sweaters-nu-2/?page=___NUM___", {'main_category': "ao_hoodie_nu", "sex": "female"}),
        ("https://www.lazada.vn/ao-sweater-cardigan-nu/?page=___NUM___", {'main_category': "ao_len_cardigan_nu", "sex": "female"}),
        ("https://www.lazada.vn/ao-so-mi-ao-blouse-nu/?page=___NUM___", {'main_category': "ao_so_mi_nu", "sex": "female"}),
        ("https://www.lazada.vn/ao-thun-cho-nu/?page=___NUM___", {'main_category': "ao_thun_nu", "sex": "female"}),
        ("https://www.lazada.vn/ao-hai-day-nu/?page=___NUM___", {'main_category': "ao_hai_day_nu", "sex": "female"}),
        ("https://www.lazada.vn/ao-kieu-cho-nu/?page=___NUM___", {'main_category': "ao_kieu_nu", "sex": "female"}),
        ("https://www.lazada.vn/jumpsuit-nu/?page=___NUM___", {'main_category': "jumpsuit_nu", "sex": "female"}),
        ("https://www.lazada.vn/do-ngu-noi-y/?page=___NUM___", {'main_category': "do_lot_nu", "sex": "female"}),
        ("https://www.lazada.vn/giay-nu-thoi-trang/?page=___NUM___", {'main_category': "giay_dep_nu", "sex": "female"}),
    ])


def crawl_sendo():
    process.crawl(SendoCrawler, name='sendo', num_pages=5, start_urls=[
        (26, {'main_category': 'dam_nu', 'sex': 'female'}),
        (10, {'main_category': 'ao_so_mi_nu', 'sex': 'female'}),
        (12, {'main_category': 'ao_thun_nu', 'sex': 'female'}),
        (11, {'main_category': 'ao_kieu_nu', 'sex': 'female'}),
        (1917, {'main_category': 'ao_tre_vai_nu', 'sex': 'female'}),
        (666, {'main_category': 'ao_khoac_chong_nang', 'sex': 'female'}),
        (667, {'main_category': 'ao_khoac_kieu_nu', 'sex': 'female'}),
        (665, {'main_category': 'ao_vest_nu', 'sex': 'female'}),
        (1425, {'main_category': 'ao_khoac_jean_nu', 'sex': 'female'}),
        (19, {'main_category': 'quan_jean_nu', 'sex': 'female'}),
        (1945, {'main_category': 'quan_baggy_nu', 'sex': 'female'}),
        (23, {'main_category': 'quan_legging_nu', 'sex': 'female'}),
        (22, {'main_category': 'quan_short_nu', 'sex': 'female'}),
        (695, {'main_category': 'jumpsuit_nu', 'sex': 'female'}),
        (34, {'main_category': 'chan_vay_nu', 'sex': 'female'}),
        (63, {'main_category': 'bikini_nu', 'sex': 'female'}),
        (1938, {'main_category': 'do_ngu', 'sex': 'female'}),
        (52, {'main_category': 'do_lot_nu', 'sex': 'female'}),
        (2545, {'main_category': 'giay_cao_got_nu', 'sex': 'female'}),
        (4170, {'main_category': 'scandals_nu', 'sex': 'female'}),
        (1688, {'main_category': 'dep_nu', 'sex': 'female'}),
        (4162, {'main_category': 'sneaker_nu', 'sex': 'female'}),

        (1666, {'main_category': 'ao_so_mi_nam', 'sex': 'male'}),
        (1864, {'main_category': 'ao_khoac_du_nam', 'sex': 'male'}),
        (1865, {'main_category': 'ao_khoac_kaki_nam', 'sex': 'male'}),
        (681, {'main_category': 'ao_khoac_chong_nang_nam', 'sex': 'male'}),
        (1867, {'main_category': 'ao_khoac_jean_nam', 'sex': 'male'}),
        (1670, {'main_category': 'quan_jean_nam', 'sex': 'male'}),
        (1676, {'main_category': 'quan_short_nam', 'sex': 'male'}),
        (106, {'main_category': 'quan_lot_nam', 'sex': 'male'}),
        (1685, {'main_category': 'ao_thun_dai_tay', 'sex': 'male'}),
        (97, {'main_category': 'ao_polo_nam', 'sex': 'male'}),
        (310, {'main_category': 'ao_thun_ngan_tay_nam', 'sex': 'male'}),
        (2367, {'main_category': 'ao_hoodie_nam', 'sex': 'male'}),
        (3844, {'main_category': 'quan_kaki_nam', 'sex': 'male'}),
        (3845, {'main_category': 'quan_tay_nam', 'sex': 'male'}),
        (690, {'main_category': 'ao_vest_nam', 'sex': 'male'}),
        (4166, {'main_category': 'sneaker_nam', 'sex': 'male'}),
        (4179, {'main_category': 'giay_tay_nam', 'sex': 'male'}),
        (1690, {'main_category': 'dep_nam', 'sex': 'male'}),
    ])


def crawl():
    crawl_shopee()
    # crawl_tiki()
    # crawl_lazada()
    # crawl_sendo()


if __name__ == '__main__':
    if not os.path.exists('log'):
        os.makedirs('log')

    os.remove('log/crawler.log')

    settings = get_project_settings()
    settings.update({
        **scrapy_settings.SETTINGS,
        # **scrapy_settings.SPLASH_SETTINGS,
    })

    process = CrawlerProcess(settings)

    configure_logging()

    crawl()
    process.start()
