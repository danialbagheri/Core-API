from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, ListView
from product.models import ProductCategory
# Create your views here.

class HomePage(ListView):
    model = ProductCategory
    context_object_name = "product_categories"
    template_name = "pages/home.html"