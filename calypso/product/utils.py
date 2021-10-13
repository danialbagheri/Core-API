import random


def get_slug():
    slug_instance = random.randint(22, 9991)
    return slug_instance


def icons_directory_path(instance, filename):
    # file will upload to media root "product_images/bandName/product_code/Image_type/fileName"
    return "tags-icon/{0}".format(filename)


def extract_number(number_str):
    number = ""
    number_started = False
    for c in number_str:
        if c.isdigit():
            number += c
            number_started = True
        elif number_started:
            return int(number)
    return int(number)


def get_ml_number(ml_string):
    litre_const = 1
    quantity_number = 1
    ml_string = ml_string.lower()
    if 'x' in ml_string.lower():
        index = ml_string.index('x')
        quantity_number = ml_string[:index]
        quantity_number = extract_number(quantity_number)
        ml_string = ml_string[index:]

    if 'litre' in ml_string or ('ml' not in ml_string and 'l' in ml_string):
        litre_const = 1000
    ml_number = extract_number(ml_string)

    return ml_number * quantity_number * litre_const
