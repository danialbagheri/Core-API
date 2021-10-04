import csv
from io import StringIO

from django.contrib import admin
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

    def changelist_view(self, request, extra_context=None):
        try:
            action = self.get_actions(request)[request.POST['action']][0]
            is_dependant = action.dependant_action
        except (KeyError, AttributeError):
            is_dependant = False

        if is_dependant:
            post = request.POST.copy()
            post.setlist(admin.helpers.ACTION_CHECKBOX_NAME, self.model.objects.values_list('id', flat=True))
            request.POST = post

        return admin.ModelAdmin.changelist_view(self, request, extra_context)

    @staticmethod
    def update_locations(csv_file):
        reader = csv.reader(csv_file, delimiter=',')
        for row in reader:
            if row[0] == 'variant':
                continue
            sku = row[0].split(',')[0]
            variant = ProductVariant.objects.filter(sku=sku).first()
            stockist = Stockist.objects.filter(name=row[1]).first()
            if not variant or not stockist:
                continue
            WhereToBuy.objects.update_or_create(
                variant=variant,
                stockist=stockist,
                defaults={
                    'url': row[2],
                }
            )

    def import_csv(self, request):
        if request.method == 'POST':
            csv_bytes_file = request.FILES['csv_file']
            csv_file = StringIO(csv_bytes_file.read().decode())
            self.update_locations(csv_file)
            self.message_user(request, 'Your csv file has been imported.')
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
