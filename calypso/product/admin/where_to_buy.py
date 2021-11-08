import csv
import os
from io import StringIO

import openpyxl
from django.contrib import admin, messages
from django import forms
from django.shortcuts import redirect, render
from django.urls import path

from product.admin.actions import check_locations
from product.models import WhereToBuy, ProductVariant, Stockist


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()


@admin.register(WhereToBuy)
class WhereToBuyAdmin(admin.ModelAdmin):
    change_list_template = 'admin/product/where_to_buy_changelist.html'
    list_display = (
        'variant',
        'stockist',
        'url',
    )
    search_fields = ('variant__sku', 'variant__name', 'stockist__name')
    list_filter = ('stockist',)
    actions = (check_locations,)

    def is_valid_data(self, variant, stockist, request, row_num):
        if variant and stockist:
            return True
        if not variant:
            self.message_user(
                message=f'Invalid variant at row {row_num}',
                request=request,
                level=messages.ERROR,
            )
        if not stockist:
            self.message_user(
                message=f'Invalid stockist at row {row_num}',
                request=request,
                level=messages.ERROR,
            )
        return False

    def update_locations_with_csv(self, locations_file, request):
        reader = csv.reader(locations_file, delimiter=',')
        count = 0
        to_create_data = []
        is_valid = True
        for row in reader:
            count += 1
            if row[0] == 'variant':
                continue
            sku = row[0].split(',')[0]
            variant = ProductVariant.objects.filter(sku=sku).first()
            stockist = Stockist.objects.filter(name=row[1]).first()
            if not self.is_valid_data(variant, stockist, request, count):
                is_valid = False
                continue
            to_create_data.append(dict(
                variant=variant,
                stockist=stockist,
                defaults={
                    'url': row[2],
                }
            ))
        if not is_valid:
            return is_valid
        for location_data in to_create_data:
            WhereToBuy.objects.update_or_create(**location_data)
        return is_valid

    def update_locations_with_xlsx(self, locations_file, request):
        locations_workbook = openpyxl.load_workbook(locations_file.file)
        locations_data = locations_workbook.active
        count = 0
        to_create_data = []
        is_valid = True
        for row in locations_data.iter_rows(values_only=True):
            if row[0] == 'variant':
                continue
            sku = row[0].split(',')[0]
            variant = ProductVariant.objects.filter(sku=sku).first()
            stockist = Stockist.objects.filter(name=row[1]).first()
            if not self.is_valid_data(variant, stockist, request, count):
                is_valid = False
                continue
            to_create_data.append(dict(
                variant=variant,
                stockist=stockist,
                defaults={
                    'url': row[2],
                }
            ))
        if not is_valid:
            return is_valid
        for location_data in to_create_data:
            WhereToBuy.objects.update_or_create(**location_data)
        return is_valid

    def import_csv(self, request):
        if request.method == 'POST':
            file = request.FILES['csv_file']
            _, extension = os.path.splitext(file.name)
            if extension == '.csv':
                csv_file = StringIO(file.read().decode())
                imported = self.update_locations_with_csv(csv_file, request)
            elif extension == '.xlsx':
                imported = self.update_locations_with_xlsx(file, request)
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
            template_name='admin/csv_form.html',
            context=context,
        )

    def get_urls(self):
        urls = super().get_urls()
        urls = [(path('import-csv/', self.import_csv))] + urls
        return urls
