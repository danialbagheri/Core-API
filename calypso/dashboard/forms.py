from django import forms
from product.models import ProductVariant, Product, Collection, Tag, ProductType, CollectionItem, ProductImage
from review.models import Review, Reply
from faq.models import Faq
from blog.models import BlogPost
from page.models import Page
from web.models import Configuration
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django_grapesjs.forms import GrapesJsWidget, GrapesJsField


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = "__all__"
        exclude = ['reply', 'user', 'opened']


class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        exclude = ['image_width', 'image_height', ]
        fields = "__all__"
        widgets = {
            'body': SummernoteWidget(),
            'excerpt': SummernoteWidget(),
        }


class ProductTagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = "__all__"


class ConfigForm(forms.ModelForm):
    class Meta:
        model = Configuration
        fields = "__all__"


class ImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = "__all__"


class FaqForm(forms.ModelForm):
    class Meta:
        model = Faq
        fields = "__all__"
        widgets = {
            'answer': SummernoteWidget(),
        }


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['name', 'slug', 'background_image_alt', 'description']


class CollectionItemForm(forms.ModelForm):
    class Meta:
        model = CollectionItem
        fields = "__all__"


class PageForm(forms.ModelForm):

    class Meta:
        model = Page
        fields = "__all__"
        widgets = {
            'html': SummernoteWidget(),
            'section_1': SummernoteWidget(),
            'section_2': SummernoteWidget(),
            'section_3': SummernoteWidget(),
            'section_4': SummernoteWidget(),
        }


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


class ProductCreateForm(forms.ModelForm):
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
    sku = forms.CharField(required=True)
    name = forms.CharField(required=True)

    class Meta:
        model = ProductVariant
        fields = "__all__"
