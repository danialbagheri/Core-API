from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib import messages
from django.shortcuts import render
from product.models import Product, ProductCategory, ProductImage, ProductType, Tag
from .forms import ProductCategoryForm, ProductForm
# Create your views here.


def staff_required(login_url=None):
    return user_passes_test(lambda u: u.is_staff, login_url=login_url)


@staff_required(login_url="/accounts/login")
def dashboard(request):
    sku_count = Product.objects.all().count()
    context = {
        "sku_count": sku_count
    }
    return render(request, "dashboard/index.html", context=context)


@staff_required(login_url="/accounts/login")
def products(request):
    product_category = ProductCategory.objects.all()
    top_seller = request.GET.get('top', None)

    if top_seller is not None and top_seller.lower() == "yes":
        product_category = product_category.filter(top_seller=True)
    context = {
        "product_categories": product_category
    }
    return render(request, "dashboard/products/products.html", context=context)


def list_of_tags(tags):
    tag_string = ""
    for tag in tags:
        tag_string += tag.name
        tag_string += ","
    return tag_string


@staff_required(login_url="/accounts/login")
def product_add_or_edit(request, slug=None):
    product_category_instance = None
    available_tags = Tag.objects.all()
    available_tags_list = []
    for tag in available_tags:
        available_tags_list.append(tag.name)
    if slug:
        product_category_instance = ProductCategory.objects.filter(
            slug=slug).first()
    tags = list_of_tags(product_category_instance.tags.all()) or ""
    product_category_form = ProductCategoryForm(
        instance=product_category_instance)
    context = {
        "product_category_form": product_category_form,
        "tags": tags,
        "available_tags": available_tags_list
    }

    return render(request, "dashboard/products/product_edit.html", context=context)


@staff_required(login_url="/accounts/login")
def product_tags(request):
    tags = Tag.objects.all()
    context = {
        "tags": tags
    }
    return render(request, "dashboard/products/tags.html", context=context)
