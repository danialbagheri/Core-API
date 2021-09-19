import random


def get_slug():
    slug_instance = random.randint(22, 9991)
    return slug_instance


def icons_directory_path(filename):
    # file will upload to media root "product_images/bandName/product_code/Image_type/fileName"
    return "tags-icon/{0}".format(filename)
