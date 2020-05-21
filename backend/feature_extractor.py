from fastai.vision import *
import base64

from .faiss_index import ImageSearchEngine, load_invert_indexed, load_npy_file

warnings.filterwarnings('always')
warnings.filterwarnings('ignore')


class FeatureHook:
    def __init__(self, module: nn.Module, hook_func: HookFunc, forward: bool = True, detach: bool = True):
        self.hook_func, self.forward, self.detach = hook_func, forward, detach
        f = module.register_forward_hook if forward else module.register_backward_hook
        self.hook = f(self._hook)
        self.removed = False
        self.stored = None

    def _hook(self, module: nn.Module, input: Tensors, output: Tensors):
        if self.detach:
            input = (i.detach() for i in input) if is_listy(input) else input.detach()
            output = (o.detach() for o in output) if is_listy(output) else output.detach()
        hook_out = self.hook_func(module, input, output)
        self.stored = hook_out if self.stored is None else np.row_stack((self.stored, hook_out))

    def remove(self):
        if not self.removed:
            self.hook.remove()
            self.removed = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.remove()


class FeatureExtractor:
    def __init__(self, learner: Learner, module_name='1.4', ):
        assert learner is not None, f"learner is required"
        self.learner = learner
        self.module = self._get_module_by_name(model=self.learner.model, name=module_name)

    @staticmethod
    def _get_module_by_name(model: nn.Module, name):
        return dict(model.named_modules()).get(name)

    def extract_feature(self, img, base_64=False):
        assert type(img) in [str, bytes]
        if base_64:
            img = open_image(io.BytesIO(base64.b64decode(img))).resize(150)
        else:
            # if type(img) is str:
            #     with open(img, mode='rb') as f:
            #         img = open_image(f.read()).resize(150)
            # else:
            img = open_image(img).resize(150)

        with FeatureHook(self.module, self._get_feature, forward=True, detach=True) as hook:
            self.learner.predict(img)
            output = hook.stored

        output = output / (((output ** 2).sum(axis=1, keepdims=True)) ** 0.5)
        return output.squeeze()

    @staticmethod
    def _get_feature(module: nn.Module, input: Tensors, output: Tensors):
        return output.flatten(1).cpu().numpy()


if __name__ == '__main__':
    # load faiss
    index_path = '../image_search_engine/dump/dump_index_resnet.pkl'
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
    learner = load_learner(path='../models/colab_export', file='res50_sz150_best_stage3_export.pkl')
    feature_extractor = FeatureExtractor(learner)

    # with open('test_img.jpg', mode='rb') as img_f:
    #     img = img_f.read()
    #     img = base64.b64encode(img)

    img = 'test_img.jpg'

    image_feature = feature_extractor.extract_feature(img, base_64=False)

    results = search_engine.search(image_feature[None], num_results=10)
    print(results)

