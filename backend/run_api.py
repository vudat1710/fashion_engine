from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.serving import run_simple
import json
from .solr_connection import SolrConnection
from .settings import APP_BIND_ADDRESS, APP_BIND_PORT, SOLR_POST_PATH, SOLR_SHOP_PATH
import base64
from fastai.vision import *
from .feature_extractor import FeatureHook, FeatureExtractor
from .faiss_index import ImageSearchEngine, load_invert_indexed, load_npy_file
from .settings import INDEX_PATH, LEARNER_PATH, MODEL_FILE_NAME, IMAGE_IDS_FN, IMAGE_INFO_FN, FEATURE_MODEL

# define INDEX_PATH, LEARNER_PATH, MODEL_FILE_NAME, IMAGE_IDS_FN, IMAGE_INFO_FN
# install fastai

def get_app():
    app = Flask(__name__)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    image_index2info = load_invert_indexed(image_ids_fn=IMAGE_IDS_FN, image_info_fn=IMAGE_INFO_FN)
    if not os.path.exists(INDEX_PATH):
        features = load_npy_file(FEATURE_MODEL)
        path = None
    else:
        features = None
        path = INDEX_PATH

    search_engine = ImageSearchEngine(
        path=path,
        features=features,
        image_index2info=image_index2info,
        train=True,
    )

    if not os.path.exists(INDEX_PATH):
        search_engine.save_index(INDEX_PATH)
    learner = load_learner(path=LEARNER_PATH, file=MODEL_FILE_NAME)
    feature_extractor = FeatureExtractor(learner)

    @app.route("/api/searchText", methods=['GET', 'POST'])
    def search():
        data = json.loads(request.data.decode("utf-8"))
        num_results = int(data['numResults'])
        query_text = str(data['inputSearch'])
        results = connection.search(query_text, rows=num_results)
        return jsonify(results)

    return app

    @app.route("/api/searchImage", methods=['POST'])
    def search_image():
        data = json.loads(request.data)
        print(data)
        base64_str = str(data["inputImage"])
        num_results = int(data["numResults"])
        image_feature = feature_extractor.extract_feature(base64_str, base_64=True)
        results = search_engine.search(image_feature[None], num_results=num_results)[0]
        res = []
        for itemid in results.keys():
            search_params = itemid.split("_")
            post = connection.search_post_id(search_params[1], search_params[0])
            res.append(post)
        response = jsonify(res)
        response.headers.add('Access-Control-Allow-Origin', '*')

        return response
            


if __name__ == '__main__':
    connection = SolrConnection(SOLR_POST_PATH, SOLR_SHOP_PATH)
    run_simple(APP_BIND_ADDRESS, APP_BIND_PORT, get_app(), use_reloader=True, use_debugger=True, use_evalex=True)
