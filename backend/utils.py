from underthesea import word_tokenize
import re
from dateutil.parser import parse
import json 

def tokenize(terms):
    return word_tokenize(terms, format="text")


def time_str2iso_format(time_str, is_24h_format=True):
    time = re.search(fr'\d[\d/:,\- ]+[\d{"AMP" if is_24h_format else  ""}]+', time_str)[0]
    time = parse(time)
    return time.strftime('%Y-%m-%dT%H:%M:%SZ')


def read_jsonl_file(fn):
    docs = []
    with open(fn, mode='r', encoding='utf8') as f:
        for line in f:
            docs.append(json.loads(line))
        f.close()
    
    tok_field = "name"

    for doc in docs:
        if tok_field in doc.keys():
            doc["name_tokenized"] = tokenize(doc[tok_field], format="text")
        else:
            doc["name_tokenized"] = ""

    return docs


def read_json_file(fn):
    with open(fn, mode='r', encoding='utf8') as f:
        docs = json.load(f)
        f.close()
    return docs


def dump_jsonl_file(fn, docs):
    with open(fn, mode='w', encoding='utf8') as f:
        for doc in docs:
            f.write(json.dumps(doc, ensure_ascii=False))
        f.close()


if __name__ == '__main__':
    # docs = read_json_file('data/data_baomoi.json')
    # docs = read_jsonl_file('data/all_posts.jsonl')
    print(tokenize(" THUỘC TÍNH SẢN PHẨM Chất vải: Jean. Họa tiết: Khác. Phong cách: Tự do. CHI TIẾT SẢN PHẨM Quần jean baggy lưng thun cao cấp với kiểu dáng baggy , ống lửng cùng thiết kế lưng thun có dây rút ( hoặc nút) tiện lợi giúp cảm giác thoải mái vận động và diện mặc trong thời tiết nắng nóng Thiết kế phối túi 2 bên, 2 túi sau wash rách đơn giản nhưng sẽ tạo thêm điểm nhấn đặc biệt cho sản phẩm Với 2 màu trẻ trung năng động đang là xu hướng Hot nhất đang được tìm đến trong thời gian này Có thể phối với nhiều kiểu áo khác nhau Size S: 45kg trở lại M:48kg trở lại L:51kg trở lại \\ 30:54kg trở lại 31:57kg trở lại 32:60kg trở lại "))
