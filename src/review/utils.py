RESIZE_W = 100
RESIZE_H = 100


def check_request_image_size_params(request):
    if request and request.query_params:
        resize_w = request.query_params.get('resize_w', None)
        resize_h = request.query_params.get('resize_h', None)
        return resize_w, resize_h
    return None, None
