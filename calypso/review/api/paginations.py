from rest_framework import pagination
from rest_framework.response import Response


class ReviewPagination(pagination.PageNumberPagination):
    total = 12

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'total_review_count': len(data) + 1,
            'review_average_score': self.get_total_review_score(data),
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
