from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class CustomRewiewPagination(LimitOffsetPagination):
    page_size = 5

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })


class CustomCommentPagination(LimitOffsetPagination):
    page_size = 5

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })