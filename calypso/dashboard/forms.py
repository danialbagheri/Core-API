from django import forms

from product.models import ProductVariant, Product, Collection, Tag, ProductType, Collection
from review.models import Review, Reply
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = "__all__"
        exclude = ['reply', 'user']

class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = "__all__"


class ProductForm(forms.ModelForm):
    collections = forms.ModelMultipleChoiceField(
        queryset=Collection.objects.all(), required=False)

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
