from rest_framework.pagination import PageNumberPagination  # type: ignore
from rest_framework.exceptions import NotFound # type: ignore
from patient_project.settings import MAXIMUM_PAGE_SIZE, DEFAULT_PAGE_SIZE


class CustomPagination(PageNumberPagination):
    # Default page size, Number of records per page
    page_size = DEFAULT_PAGE_SIZE
    # Allow clients to set page size query param
    page_size_query_param = 'pageSize'
    # Maximum page size allowed
    max_page_size = MAXIMUM_PAGE_SIZE
    # Page Number query param
    page_query_param = 'pageNumber'
    # Last page string indicator
    last_page_strings = ('end',)

    def paginate_queryset(self, queryset, request, view=None):
        """
        Customizes pagination behavior to handle cases where the requested page is empty.
        """
        try:
            return super().paginate_queryset(queryset, request, view)
        except NotFound:
            self.page = None
            return []

    def get_paginated_response(self, data):
        """
        Returns a paginated response even for empty pages.
        """
        if self.page is None:
            return super().get_paginated_response([])
        return super().get_paginated_response(data)

		
		
paginator = CustomPagination()