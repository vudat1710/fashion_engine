import json
import re
from lxml import etree
from html import unescape


def load_jsonl_file(fn):
    data = []
    with open(fn, mode='r', encoding='utf8') as f:
        for line in f:
            data.append(json.loads(line))
        f.close()
    return data


def dump_jsonl_file(data: list, fn):
    with open(fn, mode='w', encoding='utf8') as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False))
            f.write('\n')
        f.close()


def html2text(html, escape=False):
    if escape:
        html = unescape(html)

    tree = etree.HTML(html)
    if tree is None: return ""
    texts = tree.xpath('//text()')
    # texts = [re.sub(r'(\xa0|\uf0b7)', ' ', text) for text in texts]
    text = re.sub(r'\s+', ' ', ' '.join(texts))
    return text
