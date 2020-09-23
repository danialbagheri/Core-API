from django import forms

from product.models import ProductCategory, Product
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


class ProductCategoryForm(forms.ModelForm):

    class Meta:
        model = ProductCategory
        fields = "__all__"
        exclude = ['tags']
        widgets = {
            'description': SummernoteWidget(),
            'direction_of_use': SummernoteWidget(),
        }


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = "__all__"
