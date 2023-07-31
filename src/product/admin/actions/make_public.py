def make_public(modeladmin, request, queryset):
    queryset.update(is_public=True)
