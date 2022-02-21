import csv
from datetime import datetime

from django.contrib import admin
from django.http import HttpResponse


class ExportableAdminMixin:
    export_exclude = ()

    def get_actions(self, request):
        actions = super().get_actions(request)
        actions['export_as_csv'] = (getattr(self.__class__, 'export_as_csv'), 'export_as_csv', 'Export as CSV')
        return actions

    def export_as_csv(self, request, queryset):
        queryset = self.get_queryset(request)
        list_fields = self.get_list_display(request)
        list_fields = [field for field in list_fields if field not in self.export_exclude]

        now = datetime.now().date()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={self.model._meta.model_name}_{now}_report.csv'
        writer = csv.writer(response)
        writer.writerow(list_fields)
        for element in queryset:
            row = []
            for field in list_fields:
                try:
                    if hasattr(element, field):
                        row.append(getattr(element, field))
                    else:
                        row.append(getattr(self, field)(element))
                except Exception:
                    row.append('-')
            writer.writerow(row)
        return response

    export_as_csv.dependant_action = True

    def changelist_view(self, request, extra_context=None):
        try:
            action = self.get_actions(request)[request.POST['action']][0]
            is_dependant = action.dependant_action
        except (KeyError, AttributeError):
            is_dependant = False

        if is_dependant:
            post = request.POST.copy()
            post.setlist(admin.helpers.ACTION_CHECKBOX_NAME, [self.model.objects.first().id])
            request.POST = post

        return admin.ModelAdmin.changelist_view(self, request, extra_context)
