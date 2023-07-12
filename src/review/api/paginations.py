from django.db.models import Count
from rest_framework import pagination
from rest_framework.response import Response


class ReviewPagination(pagination.PageNumberPagination):
    total = 12

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.total_review_count = 0
        self.review_average_score = 0
        self.reviews_score_chart = {i: 0 for i in range(1, 6)}

    def paginate_queryset(self, queryset, request, view=None):
        scores_data = queryset.values('score').annotate(score_count=Count('id'))
        for score_data in scores_data:
            self.total_review_count += score_data['score_count']
            self.review_average_score += score_data['score'] * score_data['score_count']
            self.reviews_score_chart[score_data['score']] += score_data['score_count']
        self.review_average_score = (
            self.review_average_score / self.total_review_count if self.total_review_count else 0
        )
        return super().paginate_queryset(queryset, request, view=view)

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'total_review_count': self.total_review_count,
            'review_average_score': self.review_average_score,
            'score_chart': self.reviews_score_chart,
            'results': data,
        })

    @staticmethod
    def get_total_review_score(data):
        review_count = len(data)
        score = 0
        for review in data:
            score += review['score']
        if review_count == 0:
            return 0
        return score / review_count
