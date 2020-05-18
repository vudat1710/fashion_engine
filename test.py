from fastai.vision import *
import base64

from feature_extractor.feature_extractor import FeatureExtractor
from image_search_engine.faiss_index import ImageSearchEngine, load_npy_file, load_invert_indexed


def test_extractor_and_search():
    index_path = 'image_search_engine/dump/dump_index_resnet.pkl'
    image_index2info = load_invert_indexed(image_ids_fn='data/all_feat.list', image_info_fn='data/all_images_path.csv')

    if not os.path.exists(index_path):
        features = load_npy_file('features_resnet50.npy')
        path = None
    else:
        features = None
        path = index_path

    search_engine = ImageSearchEngine(
        path=path,
        features=features,
        image_index2info=image_index2info,
        train=True,
    )

    if not os.path.exists(index_path):
        search_engine.save_index(index_path)

    # load feature extractor
    learner = load_learner(path='models/colab_export', file='res50_sz150_best_stage3_export.pkl')
    feature_extractor = FeatureExtractor(learner)

    # with open('test_img.jpg', mode='rb') as img_f:
    #     img = img_f.read()
    #     img = base64.b64encode(img)

    img = 'test_img.jpg'

    image_feature = feature_extractor.extract_feature(img, base_64=False)

    results = search_engine.search(image_feature[None], num_results=10)
    print(results)
