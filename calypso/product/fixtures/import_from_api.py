from django.core.files import File
import requests
import re
from product.models import *
import pdb


def getFilename_fromCd(cd):
    """
    Get filename from content-disposition
    """
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0]


def save_image(url, product_code):
    r = requests.get(url)
    filename = getFilename_fromCd(r.headers.get(
        'content-disposition')) or product_code
    path = f'/tmp/{filename}.jpg'
    open(path, 'wb').write(r.content)
    return path


def get_the_products():
    request = requests.get(
        'https://api.lincocare.co.uk/product-categories/').json()
    for i in request:
        product_category = ProductCategory.objects.create(
            name=i["name"],
            slug=i["slug"],
            sub_title=i["second_title"],
            description=i["description"],
            direction_of_use=i["direction_of_use"],

        )
        for product_t in i['types']:
            product_type, created = ProductType.objects.get_or_create(
                name=product_t
            )
            product_category.types.add(product_type)
            product_category.save()
        for tag in i['tags']:
            tag_instance, created = Tag.objects.get_or_create(
                name=tag['custom_tag']
            )
            if created:
                file_name = tag_instance.name.replace(" ", "-")
                icon_path = save_image(tag['icon'], file_name)
                file = File(open(icon_path, 'rb'))
                tag_instance.icon = file
                tag_instance.save()
            product_category.tags.add(tag_instance)
            product_category.save()
        for product in i['products']:
            product_instance = Product.objects.create(
                product_code=product['product_code'],
                product_category=product_category,
                option_name=product['option_name'],
                option_value=product['option_value'],
                shopify_rest_variant_id=product['shopify_variant_id'],
            )
            for image in product['images']:
                image_path = save_image(
                    image['image_url'], product['product_code'])
                image_instance = ProductImage.objects.create(
                    product=product_instance,
                    image_type=image['image_type'],
                    image_angle=image['image_angle'],
                    alternate_text=image['image_alt:']
                )
                file = File(open(image_path, 'rb'))
                image_instance.image = file
                image_instance.save()
                if product_category.main_image == None:
                    product_category.main_image = image_instance
