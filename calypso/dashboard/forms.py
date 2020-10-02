from django import forms

from product.models import ProductVariant, Product
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = "__all__"
        exclude = ['tags']
        widgets = {
            'description': SummernoteWidget(),
            'direction_of_use': SummernoteWidget(),
        }


class ProductVariantForm(forms.ModelForm):

    class Meta:
        model = ProductVariant
        fields = "__all__"
