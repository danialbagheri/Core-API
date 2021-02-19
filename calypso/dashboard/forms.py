from django import forms
from product.models import ProductVariant, Product, Collection, Tag, ProductType, Collection, ProductImage
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
        exclude = ['reply', 'user','opened']

class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = "__all__"
        widgets = {
            'body': SummernoteWidget(),
            'excerpt': SummernoteWidget(),
        }

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
class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = "__all__"


class PageForm(forms.ModelForm):

    html = GrapesJsField()
    class Meta:
        model = Page
        fields = "__all__"
        # widgets = {
        #     'html': GrapesJsWidget(),
        # }

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
        
