from .utils import read_jsonl_file, read_json_file, time_str2iso_format
from .solr_connection import SolrConnection

print('Create connection...')
solr_connection = SolrConnection('http://localhost:8983/solr/multimedia', 'http://localhost:8983/solr/multimedia_shops')
print('-' * 30)
print('Loading data...')
posts = read_jsonl_file('data/all_posts.jsonl')
print(f'Num posts: {len(posts)}')

print('-' * 30)
print('Adding posts...')
solr_connection.add_posts(posts)
print(f'Added {len(posts)} docs')

#shops = read_jsonl_file('data/all_shops.jsonl')
#print(f'Num shops: {len(shops)}')
#
#print('-' * 30)
#print('Adding shops...')
#solr_connection.add_shops(shops)
#print(f'Added {len(shops)} docs')
