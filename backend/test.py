import pandas as pd
import re

from .solr_connection import SolrConnection
from .settings import SOLR_SHOP_PATH, SOLR_POST_PATH

connection = SolrConnection(SOLR_POST_PATH, SOLR_SHOP_PATH)

result = connection.search("áo thun nam")
print(result)
for r in result:
    print (r)
