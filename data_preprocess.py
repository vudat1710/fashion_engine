from utils import load_jsonl_file, dump_jsonl_file
import pandas as pd
from collections import defaultdict
import os
import shutil
from sklearn.model_selection import train_test_split


def post2url(post):
    item_id = post.get('itemid')
    shop_id = post.get('shopid')
    return f'https://shopee.vn/shopee-i.{shop_id}.{item_id}'


def preprocess_posts(fn):
    posts = load_jsonl_file(fn)
    for post in posts:
        post['post_url'] = post2url(post)

    dump_jsonl_file(posts, 'data/shopee/preprocess_posts.jsonl')


def statistic_categories(fn, out_fn, mapping_category: dict = None):
    posts = load_jsonl_file(fn)
    groups = defaultdict(list)
    for post in posts:
        category = post['categories'][-1] + ' ' + post['sex']
        # category = post['main_category'] + ' ' + post['sex']
        if mapping_category is not None:
            category = mapping_category.get(category)
        if category is not None:
            groups[category].append(post)

    print('number of categories', len(groups.keys()))
    print('---------------------------')
    for category, category_posts in groups.items():
        print(category, len(category_posts))

    print('start export to csv')
    group2csv(groups, out_fn)
    print('export to csv successfully')


def group2csv(groups: dict, fn):
    data = []
    for category, items in groups.items():
        for item in items:
            data.extend([
                {
                    'label': category,
                    'image_name': image.get('path'),
                }
                for image in item.get('images')
            ])
    df = pd.DataFrame(data)
    df.to_csv(fn, index=False, sep='\t')


def truncate_csv(fn, out_fn, sep='\t', label_col='label', content_col='image_name', num_min=50, num_max=100):
    df = pd.read_csv(fn, sep=sep)
    df_count = df.groupby(label_col)[content_col].count()
    df_count = df_count[df_count >= num_min]
    labels = df_count.index.tolist()
    dfs = [
        df[df[label_col] == label].sample(n=min(df_count.loc[label], num_max))
        for label in labels
    ]
    df = pd.concat(dfs)
    df.to_csv(out_fn, index=False, sep=sep)


def csv2image_folder(src_folder, dest_folder, csv_fn, image_col, sep='\t'):
    assert os.path.exists(src_folder), f'{src_folder} folder is not existed'
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    df = pd.read_csv(csv_fn, sep=sep)
    for image in df[image_col].values:
        shutil.copy(os.path.join(src_folder, image), dest_folder)


def csv2multi_image_folder(src_folder, dest_folder, csv_fn, label_col, image_col, sep='\t'):
    assert os.path.exists(src_folder), f'{src_folder} folder is not existed'
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    df = pd.read_csv(csv_fn, sep=sep)
    for label in df[label_col].unique():
        os.makedirs(os.path.join(dest_folder, label), exist_ok=True)

    for label, image_name in df[[label_col, image_col]].values:
        shutil.copy(os.path.join(src_folder, image_name), os.path.join(dest_folder, label))


def statistic_category_by_folder(folder_name, output_csv_fn, sep='\t'):
    images = []
    for category in os.listdir(folder_name):
        cat_dir = os.path.join(folder_name, category)
        for fn in os.listdir(cat_dir):
            images.append({
                'label': category,
                'path': os.path.join(category, fn),
            })

    df = pd.DataFrame(images)
    df.to_csv(output_csv_fn, sep=sep, index=False)
    print(df.groupby("label")['path'].count())


def split_train_test(csv_fn, src_folder, dest_folder, label_col, path_col, test_pct=0.2, sep='\t'):
    df = pd.read_csv(csv_fn, sep=sep)
    labels = df[label_col].unique()
    train, test = train_test_split(df, test_size=test_pct)

    os.makedirs(os.path.join(dest_folder, 'train'), exist_ok=True)
    os.makedirs(os.path.join(dest_folder, 'test'), exist_ok=True)

    train_folder = os.path.join(dest_folder, 'train')
    test_folder = os.path.join(dest_folder, 'test')

    for label in labels:
        os.makedirs(os.path.join(train_folder, label), exist_ok=True)
        os.makedirs(os.path.join(test_folder, label), exist_ok=True)

    print('Copying files into train folder')
    for label, path in train[[label_col, path_col]].values:
        shutil.copy(os.path.join(src_folder, path), os.path.join(train_folder, label))

    print('Copying files into test folder')
    for label, path in test[[label_col, path_col]].values:
        shutil.copy(os.path.join(src_folder, path), os.path.join(test_folder, label))


if __name__ == '__main__':
    # shopee
    # preprocess_posts('data/shopee/posts.jsonl')
    # statistic_categories('data/shopee/preprocess_posts.jsonl', 'data/shopee/images.csv')
    # truncate_csv('data/shopee/images.csv', 'data/shopee/train_images.csv', num_min=50, num_max=200)
    # csv2image_folder('data/shopee/images', 'data/shopee/train_images/full', 'data/shopee/train_images.csv', 'image_name')
    # csv2multi_image_folder(
    #     src_folder='data/shopee/images',
    #     dest_folder='data/shopee/train_images',
    #     csv_fn='data/shopee/train_images.csv',
    #     label_col='label',
    #     image_col='image_name',
    # )

    # tiki
    # tiki_map = dict(pd.read_csv('data/tiki/mapping_category.csv', sep='\t').values)
    # preprocess_posts('data/tiki/posts.jsonl')
    # statistic_categories('data/tiki/posts.jsonl', 'data/tiki/images.csv', mapping_category=tiki_map)
    # truncate_csv('data/tiki/images.csv', 'data/tiki/train_images.csv', num_min=50, num_max=200)
    # csv2image_folder('data/tiki/images', 'data/tiki/train_images/full', 'data/tiki/train_images.csv', 'image_name')
    # csv2multi_image_folder(
    #     src_folder='data/tiki/images',
    #     dest_folder='data/tiki/train_images',
    #     csv_fn='data/tiki/train_images.csv',
    #     label_col='label',
    #     image_col='image_name',
    # )

    statistic_category_by_folder('data/merge_ver2', 'data/images_ver2.csv')

    split_train_test('data/images_ver2.csv', 'data/merge_ver2', 'data/fashion_data', 'label', 'path', test_pct=0.2)