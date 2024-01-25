import random

RESIZE_W = 100
RESIZE_H = 100


def get_slug():
    slug_instance = random.randint(22, 9991)
    return slug_instance


def icons_directory_path(instance, filename):
    # file will upload to media root "product_images/bandName/product_code/Image_type/fileName"
    return "tags-icon/{0}".format(filename)


def check_request_image_size_params(request):
    if request and request.query_params:
        resize_w = request.query_params.get('resize_w', None)
        resize_h = request.query_params.get('resize_h', None)
        return resize_w, resize_h
    return None, None

