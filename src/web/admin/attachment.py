import os

from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from django_summernote.utils import get_attachment_model

attachment_model = get_attachment_model()
admin.site.unregister(attachment_model)


class AttachmentAdminForm(forms.ModelForm):
    file = forms.FileField(required=True)

    class Meta:
        model = get_attachment_model()
        fields = '__all__'


class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'file', 'attachment_preview', 'uploaded')
    search_fields = ('name',)
    ordering = ('-id',)
    form = AttachmentAdminForm

    def attachment_preview(self, obj):
        file = obj.file
        _, extension = os.path.splitext(file.name)
        image_extensions = ['.tif', '.tiff', '.bmp', '.jpg', '.jpeg', '.gif', '.png', '.eps']
        if extension.lower() in image_extensions:
            return mark_safe('<img src="{}" width="100" />'.format(file.url))
        return 'Not an image'

    attachment_preview.short_description = 'Attachment Preview'


admin.site.register(attachment_model, AttachmentAdmin)
