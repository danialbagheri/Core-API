from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import View, UpdateView, DetailView, ListView, DeleteView, CreateView, TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from product.models import ProductVariant, Product, ProductImage, ProductType, Tag, Collection, Keyword
from review.models import Review
from blog.models import BlogPost
from faq.models import Faq
from page.models import Page
from web.models import Configuration
from .forms import ProductForm, ProductVariantForm, CollectionForm, ReviewForm, FaqForm, BlogForm, PageForm, ImageForm
import json
# Create your views here.


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


def staff_required(login_url=None, *args, **kwargs):
    return user_passes_test(lambda u: u.is_staff, login_url=login_url)


@staff_required(login_url="/login")
def dashboard(request):
    sku_count = ProductVariant.objects.all().count()
    context = {
        "sku_count": sku_count
    }
    return render(request, "dashboard/index.html", context=context)


@staff_required(login_url="/login")
def products(request):
    product = Product.objects.all()
    top_seller = request.GET.get('top', None)

    if top_seller is not None and top_seller.lower() == "yes":
        product = product.filter(top_seller=True)
    context = {
        "products": product
    }
    return render(request, "dashboard/products/products.html", context=context)


class ProductEdit(StaffRequiredMixin, View):

    def list_of_tags(self, tags):
        tag_string = ""
        for tag in tags:
            tag_string += tag.name
            tag_string += ","
        return tag_string

    def get_object(self):
        product_instance = Product.objects.filter(
            slug=self.kwargs['slug']).first()
        return product_instance

    def get_the_tags(self):
        available_tags = Tag.objects.all()
        available_tags_list = []
        for tag in available_tags:
            available_tags_list.append(tag.name)
        return available_tags_list

    def get_the_keywords(self):
        available_keywords = Keyword.objects.all()
        available_keyword_list = []
        for keyword in available_keywords:
            available_keyword_list.append(keyword.name)
        return available_keyword_list

    def variant_form_list(self):
        product_instance = self.get_object()
        variant_forms = []
        for variant in product_instance.variants.all():
            variant_form = ProductVariantForm(instance=variant)
            variant_forms.append(variant_form)
        return variant_forms

    def get_context_data(self, **kwargs):
        product_instance = self.get_object()
        product_form = ProductForm(
            instance=product_instance)
        variant_forms = self.variant_form_list()
        available_tags_list = self.get_the_tags()  # Get all the tags
        available_keyword_list = self.get_the_keywords()  # Get all the tags
        tags = self.list_of_tags(
            product_instance.tags.all())  # Get the instance tags

        context = {
            "product_form": product_form,
            "tags": tags,
            "available_tags": available_tags_list,
            "available_keywords": available_keyword_list,
            "variant_forms": variant_forms
        }
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, "dashboard/products/product_edit.html", context=context)

    def save_tag_list(self, product, tags_list):
        if len(tags_list) >= 1:
            product.tags.clear()
            for tag in tags_list:
                tag_instance, created = Tag.objects.get_or_create(
                    name=tag['value'])
                product.tags.add(tag_instance)
            product.save()

    def save_keyword_list(self, product, keyword_list):
        if len(keyword_list) >= 1:
            product.keyword.clear()
            for keyword in keyword_list:
                keyword_instance, created = Keyword.objects.get_or_create(
                    name=keyword['value'])
                product.keyword.add(keyword_instance)
            product.save()

    def save_variants(self):
        pass

    def post(self, request, *args, **kwargs):
        product_instance = self.get_object()
        context = self.get_context_data()
        product_form = ProductForm(request.POST, instance=product_instance)
        if product_form.is_valid():
            product = product_form.save()
            tags_list = json.loads(request.POST.get(
                'tagslist').replace("'", "\""))
            self.save_tag_list(product, tags_list)
            import pdb
            pdb.set_trace()
            messages.success(
                request, f"{product_form.instance.name} have been updated.")
            return redirect(reverse("dashboard:products"))
        context['product_form'] = product_form
        return render(request, "dashboard/products/product_edit.html", context=context)


@staff_required(login_url="/login")
def product_tags(request):
    tags = Tag.objects.all()
    context = {
        "tags": tags
    }
    return render(request, "dashboard/products/tags/tags.html", context=context)

class ReviewList(StaffRequiredMixin, ListView):
    model = Review
    context_object_name = 'reviews'
    template_name = 'dashboard/reviews/list.html'

class ReviewEditView(StaffRequiredMixin, UpdateView):
    model = Review
    template_name = 'dashboard/reviews/edit.html'
    form_class = ReviewForm
    success_url = reverse_lazy('dashboard:reviews')

class CollectionsList(StaffRequiredMixin, ListView):
    model = Collection
    context_object_name = 'collections'
    template_name = 'dashboard/products/collection/collection_list.html'


class CollectionEditView(StaffRequiredMixin, UpdateView):
    model = Collection
    template_name = 'dashboard/products/collection/collection_edit.html'
    form_class = CollectionForm
    success_url = reverse_lazy('dashboard:collections')
    # def get_success_url(self):
    #     return reverse('dashboard:collections')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        messages.success(
            self.request, f"Collection name: \"{form.instance.name}\" Sussessfully updated.")
        return super().form_valid(form)


class CollectionCreate(StaffRequiredMixin, CreateView):
    model = Collection
    template_name = 'dashboard/products/collection/collection_edit.html'
    success_url = reverse_lazy('dashboard:collections')
    fields = ['name', 'slug']


class CollectionDelete(StaffRequiredMixin, DeleteView):
    model = Collection
    template_name = "dashboard/products/collection/collection_confirm_delete.html"
    success_url = reverse_lazy('dashboard:collections')


class ProductTagUpdate(StaffRequiredMixin, UpdateView):
    model = Tag
    template_name = "dashboard/products/tags/tag_edit.html"
    success_url = reverse_lazy('dashboard:tags')
    fields = ['name', 'icon']


class ProductTagDelete(StaffRequiredMixin, DeleteView):
    model = Tag
    template_name = "dashboard/products/tags/tag_confirm_delete.html"
    success_url = reverse_lazy('dashboard:tags')

    def form_valid(self, form):
        messages.success(
            self.request, f"tag name: \"{form.instance.name}\" Sussessfully deleted.")
        return super().form_valid(form)


class ImageUploadView(TemplateView):
    template_name = "dashboard/products/images/upload.html"


class ApiEndpointView(TemplateView):
    template_name = "dashboard/api-endpoint.html"

class ShopifySyncView(TemplateView):
    template_name = "dashboard/products/shopify.html"

@staff_required(login_url="/login")
def synchronise_with_shopify(request):
    products_variants = ProductVariant.objects.all() #TODO: remove after test
    result_list = []
    for variant in products_variants:
        synch = variant.synchronise_with_shopify
        if synch:
            result_list.append(
                {"success": f"{variant.sku} Successfully synched."}
            )
        else:
            result_list.append(
                {"failed": f"{variant.sku} couldn't be synchronised. please make sure the SKU on Shopify matches your product variant SKU."}
            )
    return JsonResponse(result_list, safe=False)



class FaqList(StaffRequiredMixin, ListView):
    model = Faq
    context_object_name = 'faqs'
    template_name = 'dashboard/faqs/list.html'

class FaqEditView(StaffRequiredMixin, UpdateView):
    model = Faq
    template_name = 'dashboard/faqs/edit.html'
    form_class = FaqForm
    success_url = reverse_lazy('dashboard:faqs')

class FaqCreate(StaffRequiredMixin, CreateView):
    model = Faq
    form_class = FaqForm
    template_name = 'dashboard/faqs/edit.html'
    success_url = reverse_lazy('dashboard:faqs')

class BlogList(StaffRequiredMixin, ListView):
    model = BlogPost
    context_object_name = 'blogs'
    template_name = 'dashboard/blogs/list.html'

class BlogEditView(StaffRequiredMixin, UpdateView):
    model = BlogPost
    template_name = 'dashboard/blogs/edit.html'
    form_class = BlogForm
    success_url = reverse_lazy('dashboard:blogs')

class BlogCreate(StaffRequiredMixin, CreateView):
    model = BlogPost
    form_class = BlogForm
    template_name = 'dashboard/blogs/edit.html'
    success_url = reverse_lazy('dashboard:blogs')


class PageList(StaffRequiredMixin, ListView):
    model = Page
    context_object_name = 'pages'
    template_name = 'dashboard/pages/list.html'

class PageEditView(StaffRequiredMixin, UpdateView):
    model = Page
    template_name = 'dashboard/pages/edit.html'
    form_class = PageForm
    success_url = reverse_lazy('dashboard:pages')

class PageCreate(StaffRequiredMixin, CreateView):
    model = Page
    form_class = PageForm
    template_name = 'dashboard/blogs/edit.html'
    success_url = reverse_lazy('dashboard:pages')


class ImageList(StaffRequiredMixin, ListView):
    model = ProductImage
    context_object_name = 'images'
    template_name = 'dashboard/images/list.html'

class ImageEditView(StaffRequiredMixin, UpdateView):
    model = ProductImage
    form_class = ImageForm
    template_name = 'dashboard/images/edit.html'

class ImageCreate(StaffRequiredMixin, CreateView):
    model = ProductImage
    form_class = ImageForm
    template_name = 'dashboard/images/edit.html'

class ConfigurationList(StaffRequiredMixin, ListView):
    model = Configuration
    context_object_name = 'configs'
    template_name = 'dashboard/configs/list.html'
    def get_queryset(self):
        object_list = super().get_queryset()
        return object_list