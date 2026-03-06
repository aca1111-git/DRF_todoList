from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict
from django.conf import settings


class CustomPageNumberPagination(PageNumberPagination):
    default_page_size = settings.REST_FRAMEWORK.get("PAGE_SIZE", 10)

    def paginate_queryset(self, queryset, request, view=None):
        page_size = request.query_params.get("page_size", self.default_page_size)

        # page_size=all 이면 모든 데이터를 반환
        if page_size == "all":
            self.page_size = len(queryset)

        else:
            try:
                # page_size를 정수로 변환
                self.page_size = int(page_size)

            except ValueError:
                # 숫자가 아닌 값이 들어오면 기본값 사용
                self.page_size = self.default_page_size

            # DRF 기본 paginate_queryset 기능 실행
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("data", data),
                    # 현재 페이지의 데이터 목록
                    ("page_size", len(data)),
                    # 현재 페이지에 포함된 데이터 개수
                    ("total_count", self.page.paginator.count),
                    # 전체 데이터 개수
                    ("page_count", self.page.paginator.num_pages),
                    # 전체 페이지 수
                    ("current_page", self.page.number),
                    # 현재 페이지 번호
                    ("next", self.get_next_link()),
                    # 다음 페이지 URL
                    ("previous", self.get_previous_link()),
                    # 이전 페이지 URL
                ]
            )
        )
