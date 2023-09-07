import csv
import os
from collections import defaultdict
from io import StringIO

from django import forms
from django.contrib import admin, messages
from django.db import transaction
from django.db.models import Count
from django.shortcuts import redirect, render
from django.urls import path

from product.models import Ingredient, ProductVariant, VariantIngredientThrough


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()


class ProductVariantInlineAdmin(admin.StackedInline):
    model = ProductVariant.ingredients.through
    extra = 0
    raw_id_fields = ('productvariant',)
    verbose_name = 'Variant'
    verbose_name_plural = 'Variants'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    change_list_template = 'admin/product/ingredient_changelist.html'
    list_display = ('name', 'products_count')
    inlines = (ProductVariantInlineAdmin,)
    search_fields = ('name',)

    def products_count(self, ingredient: Ingredient):
        return ingredient.products_count

    products_count.short_description = 'Products Count'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(products_count=Count('productvariant')).order_by('-products_count')
        return queryset

    @staticmethod
    def clean_ingredient_names(ingredient_names):
        clean_names = []
        for ingredient_name in ingredient_names:
            cut_index = ingredient_name.find('###')
            if cut_index >= 0:
                ingredient_name = ingredient_name[:cut_index]
            clean_names.append(ingredient_name.strip())
        last_name = clean_names[-1]
        if last_name.endswith('.'):
            clean_names[-1] = last_name[:-1]
        return clean_names

    def update_ingredients_with_csv(self, ingredients_file, request):
        reader = csv.reader(ingredients_file, delimiter=',')
        count = 0
        is_valid = True
        variants_map = {}
        ingredients_map = {}
        ingredients_set = set()
        variant_ingredients = defaultdict(list)
        for row in reader:
            count += 1
            if row[0] == '#':
                continue
            sku = row[4]
            variant = ProductVariant.objects.filter(sku=sku).first()
            if not variant:
                is_valid = False
                self.message_user(
                    message=f'Invalid sku {sku} on row {count}',
                    request=request,
                    level=messages.ERROR,
                )
                continue
            variants_map[sku] = variant
            ingredients = row[5]\
                .replace('\n', ' ').replace('contains', '###').replace('Contains', '###')\
                .replace('/ Inneholder / Innehåller / Indeholder / Sisältää', '###').split(', ')
            ingredients = self.clean_ingredient_names(ingredients)
            for ingredient in ingredients:
                if not ingredient:
                    continue
                variant_ingredients[sku].append(ingredient)
                ingredients_set.add(ingredient)
        if not is_valid:
            return False
        for ingredient_name in ingredients_set:
            ingredient, _ = Ingredient.objects.get_or_create(name=ingredient_name)
            ingredients_map[ingredient_name] = ingredient
        for sku, ingredient_names in variant_ingredients.items():
            variant = variants_map[sku]
            ingredients = [ingredients_map[ingredient_name] for ingredient_name in ingredient_names if ingredient_name]
            VariantIngredientThrough.objects.filter(variant=variant).delete()
            variant.ingredients.clear()
            variant.ingredients.add(*ingredients)
            priority = 0
            for ingredient in ingredients:
                VariantIngredientThrough.objects.create(
                    ingredient=ingredient,
                    variant=variant,
                    priority=priority,
                )
                priority += 1
        return True

    def import_csv(self, request):
        if request.method == 'POST':
            file = request.FILES['csv_file']
            _, extension = os.path.splitext(file.name)
            if extension == '.csv':
                csv_file = StringIO(file.read().decode())
                with transaction.atomic():
                    imported = self.update_ingredients_with_csv(csv_file, request)
            else:
                self.message_user(request, 'Invalid file extension.', level=messages.ERROR)
                return redirect('..')
            if imported:
                self.message_user(request, 'Your file has been imported.')
            return redirect('..')
        form = CsvImportForm()
        context = {'form': form}
        return render(
            request=request,
            template_name='admin/ingredients_csv_form.html',
            context=context,
        )

    def get_urls(self):
        urls = super().get_urls()
        urls = [(path('import-csv/', self.import_csv))] + urls
        return urls
