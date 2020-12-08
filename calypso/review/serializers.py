from .models import Review, Reply
from rest_framework import serializers, pagination
from rest_framework.response import Response

class ReviewPagination(pagination.PageNumberPagination):
    total = 12
    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'review_count': len(data),
            'total_score':self.get_total_review_score(data),
            'results': data
        })
    
    def get_total_review_score(self, data):
        review_count = len(data)
        score = 0
        for review in data:
            score += review['score']
        total_score = score / review_count
        return total_score
class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    reply = ReplySerializer(many=True, read_only=True,)
    name = serializers.ReadOnlyField()
    approved = serializers.ReadOnlyField()
    
    class Meta:
        model = Review
        exclude = ['customer_email', 'ip_address']



class ReviewCreateSerializer(serializers.ModelSerializer):
    reply = ReplySerializer(many=True, read_only=True,)
    name = serializers.ReadOnlyField()
    approved = serializers.ReadOnlyField()

    class Meta:
        model = Review
        fields = '__all__'


