import random


def get_slug():
    slug_instance = random.randint(22, 9991)
    return slug_instance


def icons_directory_path(filename):
    # file will upload to media root "product_images/bandName/product_code/Image_type/fileName"
    return "tags-icon/{0}".format(filename)


def get_ml_number(ml_string):
    ml_number = ""
    number_started = False
    for ml_char in ml_string:
        if ml_char.isdigit():
            ml_number += ml_char
            number_started = True
        elif number_started:
            return int(ml_number)
    return int(ml_number)
