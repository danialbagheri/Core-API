from rest_framework import serializers

from web.models import Menu


class MenuSerializer(serializers.ModelSerializer):
    sub_menus = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = (
            'id',
            'slug',
            'name',
            'text',
            'url',
            'image',
            'svg_image',
            'is_mega_menu',
            'is_active',
            'sub_menus',
            'position',
        )

    @staticmethod
    def get_sub_menus(menu: Menu):
        sub_menus = menu.sub_menus.filter(is_active=True)
        if not sub_menus:
            return []
        return MenuSerializer(instance=sub_menus, many=True).data
