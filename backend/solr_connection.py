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
        results = []
        query = self.build_query(text=text)
        query = query.split("OR")
        for q in query:
            params = {'rows': int(rows / len(query)), 'start': start, 'sort': sort}
            if return_score:
                params['fl'] = '*,score'
            results.extend(list(self.connection_post.search(q=q, **params)))
        
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
        search_list = []
        keywords = ["platform", "sex", ":"]
        if "," in text:
            small_text = text.split(",")
        else:
            small_text = [text]
        for t in small_text:
            tokens = word_tokenize(t, format="text").split(" ")
            platform = ""
            sex = ""
            temp = keywords
            if "platform" in t:
                platform = tokens[tokens.index("platform") + 2]
                temp.append(platform)
            if "sex" in t:
                sex = tokens[tokens.index("sex") + 2]
                temp.append(sex)
            tokens = [word for word in tokens if word not in temp]
            search_list.append((tokens, platform, sex))
        query_tokens = []
        for tokens, platform, sex in search_list:
            q = [f'(name_tokenized:"{token}")'
            for token in tokens]
            q = ' AND '.join(q)
            if platform != "":
                q += ' AND (platform:"{}")'.format(platform)
            if sex != "":
                q += ' AND (sex:"{}")'.format(sex)
            query_tokens.append("({})".format(q))
        print(' OR '.join(query_tokens))
        return ' OR '.join(query_tokens)
