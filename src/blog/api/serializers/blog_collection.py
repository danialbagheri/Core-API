from rest_framework import serializers

from blog.models import BlogCollection, BlogCollectionItem
from . import BlogPostSerializer


class CollectionItemSerializer(serializers.ModelSerializer):
    item = BlogPostSerializer(read_only=True)

    class Meta:
        model = BlogCollectionItem
        fields = ('item',)
        depth = 4


class BlogCollectionSerializer(serializers.ModelSerializer):
    items = CollectionItemSerializer(many=True, source='blogcollectionitem')
    counts = serializers.SerializerMethodField()

    class Meta:
        model = BlogCollection
        fields = '__all__'
        depth = 4

    @staticmethod
    def get_counts(obj):
        return obj.blogcollectionitem.count()
