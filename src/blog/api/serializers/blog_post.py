from bs4 import BeautifulSoup
from rest_framework import serializers
from sorl.thumbnail import get_thumbnail

from blog.models import BlogPost
from product.api.serializers import ProductSerializer


class BlogPostSerializer(serializers.ModelSerializer):
    read_time = serializers.ReadOnlyField()
    related_products = ProductSerializer(many=True)
    resized = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()
    plain_body = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = '__all__'
        depth = 2

    def get_resized(self, obj):
        request = self.context.get("request")
        resize_w = request.query_params.get('resize_w',None)
        resize_h = request.query_params.get('resize_h',None)
        if resize_h is None and resize_w is None:
            resize_w = '100'
        if resize_w is None:
            resize_w = ''
        if resize_h is None:
            height = ''
        else:
            height = f'x{resize_h}'
        if obj.image:
            return get_thumbnail(obj.image, f'{resize_w}{height}', quality=100, format='PNG').url

    def get_is_bookmarked(self, blog_post: BlogPost):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return user.bookmarked_blogposts.all().filter(id=blog_post.id).exists()

    @staticmethod
    def get_plain_body(blog_post: BlogPost):
        plain_description = BeautifulSoup(blog_post.body, features='html.parser').text
        return plain_description[:200]
