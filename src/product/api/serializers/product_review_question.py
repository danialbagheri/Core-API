from rest_framework import serializers

from product.models import ReviewQuestion


class ProductReviewQuestionSerializer(serializers.ModelSerializer):
    answer_choices = serializers.StringRelatedField(many=True)

    class Meta:
        model = ReviewQuestion
        fields = (
            'id',
            'text',
            'is_multiple_choice_question',
            'answer_choices',
        )
        read_only_fields = (
            'id',
            'text',
            'is_multiple_choice_question',
            'answer_choices',
        )
