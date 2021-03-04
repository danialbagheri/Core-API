from django.contrib.sites.models import Site
from rest_framework import serializers
from .models import BlogPost
from sorl.thumbnail import get_thumbnail

class BlogPostSerializer(serializers.ModelSerializer):
    resized = serializers.SerializerMethodField()

    def get_resized(self, obj):
        request = self.context.get("request")
        resize_w = request.query_params.get('resize_w',None)
        resize_h = request.query_params.get('resize_h',None)
        domain = Site.objects.get_current().domain
        if resize_w is None:
            resize_w = ""
        if resize_h is None:
            height = ""
        if resize_h is None and resize_w is None:
            resize_w = "100"
        else:
            height = f"x{resize_h}"
        print(f'{resize_w}{height}')
        if obj.image:
            return domain+get_thumbnail(obj.image, f'{resize_w}{height}', quality=100, format="PNG").url
    class Meta:
        model = BlogPost
        fields = '__all__'
        # depth = 2