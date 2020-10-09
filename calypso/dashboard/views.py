from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import View, UpdateView, DetailView, ListView, DeleteView, CreateView, TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from product.models import ProductVariant, Product, ProductImage, ProductType, Tag, Collection
from .forms import ProductForm, ProductVariantForm, CollectionForm
import json
# Create your views here.


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


def staff_required(login_url=None, *args, **kwargs):
    return user_passes_test(lambda u: u.is_staff, login_url=login_url)


@staff_required(login_url="/accounts/login")
def dashboard(request):
    sku_count = ProductVariant.objects.all().count()
    context = {
        "sku_count": sku_count
    }
    return render(request, "dashboard/index.html", context=context)


@staff_required(login_url="/accounts/login")
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
        tags = self.list_of_tags(
            product_instance.tags.all())  # Get the instance tags

        context = {
            "product_form": product_form,
            "tags": tags,
            "available_tags": available_tags_list,
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


@staff_required(login_url="/accounts/login")
def product_tags(request):
    tags = Tag.objects.all()
    context = {
        "tags": tags
    }
    return render(request, "dashboard/products/tags/tags.html", context=context)


class CollectionsList(ListView):
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
