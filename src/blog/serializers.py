from django.contrib.sites.models import Site
from rest_framework import serializers
from .models import BlogPost, BlogCollection, BlogCollectionItem
from sorl.thumbnail import get_thumbnail
from product.api.serializers import ProductSerializer


class BlogPostSerializer(serializers.ModelSerializer):
    resized = serializers.SerializerMethodField()
    read_time = serializers.ReadOnlyField()
    related_products = ProductSerializer(many=True)
    is_bookmarked = serializers.SerializerMethodField()

    def get_resized(self, obj):
        request = self.context.get("request")
        resize_w = request.query_params.get('resize_w',None)
        resize_h = request.query_params.get('resize_h',None)
        domain = Site.objects.get_current().domain
        if resize_h is None and resize_w is None:
            resize_w = "100"
        if resize_w is None:
            resize_w = ""
        if resize_h is None:
            height = ""
        else:
            height = f"x{resize_h}"
        if obj.image:
            return domain+get_thumbnail(obj.image, f'{resize_w}{height}', quality=100, format="PNG").url

    class Meta:
        model = BlogPost
        fields = '__all__'
        depth = 2

    def get_is_bookmarked(self, blog_post: BlogPost):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return user.bookmarked_blogposts.all().filter(id=blog_post.id).exists()


class CollectionItemSerializer(serializers.ModelSerializer):
    item = BlogPostSerializer(read_only=True)

    class Meta:
        model = BlogCollectionItem
        fields = ('item',)
        depth = 4

class BlogCollectionSerializer(serializers.ModelSerializer):
    # items = serializers.SerializerMethodField()
    items = CollectionItemSerializer(many=True, source="blogcollectionitem")
    counts = serializers.SerializerMethodField()

    # def get_items(self, obj):
    #     items = [n.item for n in obj.blogcollectionitem.order_by("order")]
    #     request = self.context.get("request")
    #     return BlogPostSerializer(context={'request': request}, instance=items, many=True).data

    def get_counts(self, obj):
        return obj.blogcollectionitem.count()

    class Meta:
        model = BlogCollection
        fields = '__all__'
        depth = 4
