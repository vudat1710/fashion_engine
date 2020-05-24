import pysolr
from underthesea import ner
from .utils import *
from operator import itemgetter

class SolrConnection:
    def __init__(self, path_post, path_shop, timeout=1200):
        self.path_post = path_post
        self.path_shop = path_shop
        self.connection_post = pysolr.Solr(path_post, timeout=timeout)
        self.connection_shop = pysolr.Solr(path_shop, timeout=timeout)

    def add_posts(self, posts):
        self.connection_post.add(posts, commit=True)

    def add_shops(self, shops):
        self.connection_shop.add(shops, commit=True)

    def search(self, text, rows=10, start=0, sort='score desc', return_score=False):
        params = {'rows': rows, 'start': start, 'sort': sort}
        if return_score:
            params['fl'] = '*,score'
        query = self.build_query(text=text)
        results = list(self.connection_post.search(q=query, **params))
        
        for result in results:
            result["shop_info"] = self.search_exact_id(result["shopid"])


        return sorted(results, key=itemgetter('item_rating'), reverse=True)
    
    def search_exact_id(self, shop_id):
        return list(self.connection_shop.search(q=f'shopid:{shop_id}'))[0]

    def search_post_id(self, post_id, platform):
        platform = platform + '.vn'
        result = list(self.connection_post.search(q=f'itemid:{post_id} AND platform:"{platform}"'))[0]
        result["shop_info"] = self.search_exact_id(result["shopid"])

        return result

    def build_query(self, text):
        tokens = ner(text)

        query_tokens = [
            f'(name_tokenized:"{token}")'
            for token, _, _, ner_tag in tokens
        ]

        return ' AND '.join(query_tokens)
