from collections import namedtuple
from http import HTTPStatus
from typing import Annotated, Literal, Optional
from fastapi import Query
from pydantic import conint

from app.middlewares.exception_handler import GeneralException

DEFAULT_OFFSET = 0
DEFAULT_PAGE_NUMBER = 1
DEFAULT_PAGE_SIZE = 100
MAXIMUM_RETRIVAL_SIZE = 300

PaginationParam = namedtuple("PaginationParam", ["limit", "offset"], defaults=[DEFAULT_PAGE_SIZE, DEFAULT_OFFSET])
SortParam = namedtuple("SortParam", ["by", "order"])
SearchParam = namedtuple("SearchParam", ["by", "value"])


def pagination_param(
        size: conint(ge=0, le=300) = DEFAULT_PAGE_SIZE,
        page: conint(ge=1) = DEFAULT_PAGE_NUMBER,
        offset: conint(ge=0) = DEFAULT_OFFSET
):
    offset = offset if offset else (page - 1) * size
    size = min(size, MAXIMUM_RETRIVAL_SIZE)
    return PaginationParam(limit=size, offset=offset)


class SearchDependencyParams:
    def __init__(self, possible_search_fields, sort_model):
        self.possible_search_fields = possible_search_fields
        self.search_model = sort_model

    def __call__(
            self,
            search_field: Annotated[Optional[str], Query()] = None,
            search_value: Annotated[Optional[str], Query()] = None,
    ):
        if not search_field:
            return
        if search_field not in self.possible_search_fields:
            raise GeneralException(detail="INVALID_FIELD", status_code=HTTPStatus.UNPROCESSABLE_ENTITY)
        if not search_value:
            raise GeneralException(detail="EMPTY_SEARCH_VALUE", status_code=HTTPStatus.UNPROCESSABLE_ENTITY)
        return SearchParam(by=getattr(self.search_model, search_field), value=search_value)


class SortDependencyParams:
    def __init__(
            self,
            possible_sort_fields: list[str],
            sort_model,
            default_sort_field: Optional[str] = None,
            default_sort_order: Optional[Literal["asc", "desc"]] = "asc",
    ):
        self.possible_sort_fields = possible_sort_fields
        self.sort_model = sort_model
        self.default_sort_field = default_sort_field
        self.default_sort_order = default_sort_order

    def __call__(
            self,
            sort_field: Annotated[Optional[str], Query()] = None,
            sort_order: Annotated[Optional[Literal["asc", "desc"]], Query()] = None,
    ):
        sort_field = sort_field or self.default_sort_field
        sort_order = sort_order or self.default_sort_order

        if not sort_field:
            return None

        if sort_field not in self.possible_sort_fields:
            raise GeneralException(detail="INVALID_FIELD", status_code=HTTPStatus.UNPROCESSABLE_ENTITY)

        return SortParam(by=getattr(self.sort_model, sort_field), order=sort_order)
