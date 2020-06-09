import json


def load_jsonl_file(fn):
    objs = []
    with open(fn, mode='r', encoding='utf8') as f:
        for line in f:
            obj = json.loads(line)
            objs.append(obj)
        f.close()
    return objs
