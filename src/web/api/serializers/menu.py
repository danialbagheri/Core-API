from rest_framework import serializers

from web.models import Menu


class MenuListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(is_active=True)
        return super().to_representation(data)


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
        list_serializer_class = MenuListSerializer

    @staticmethod
    def get_sub_menus(menu: Menu):
        sub_menus = menu.sub_menus.all()
        if not sub_menus:
            return []
        return MenuSerializer(instance=sub_menus, many=True).data
