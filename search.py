from flask import request, abort
from functools import lru_cache
from enum import Enum, unique
from util import *
import requests

@unique
class SearchParam(Enum):
    name = "name"
    year_start = "year_start"
    year_end = "year_end"
    source_lc = "source_lc"
    yn_region = "yn_region"
    current_page = "current_page"

class SearchCond:
    def __init__(self, name = None, year_start = None, year_end = None, source_lc = None, yn_region = None, current_page = 1):
        self.name = name
        self.year_start = year_start
        self.year_end = year_end
        self.source_lc = source_lc
        self.yn_region = yn_region
        self.current_page = current_page

    def check_validation(self):
        if not self.current_page:
            abort(500, "current_page must specify(start from 1)")
        params = set([enum.value.lower() for enum in SearchParam])
        if not any([v for k, v in vars(self).items() if k in params and k != "current_page"]):
            abort(500, f"must specify one in " + " ".join(params - set(["current_page"])))

    def get_search_clause(self):
        return "&".join([f"{k}={v}" if v else f"{k}=-1" for k, v in vars(self).items()])

    def get_current_page(self):
        return int(self.current_page)

    def __convertNone2empty_str(self, value):
        return value if value is not None else ""

    def __hash__(self):
        return hash("".join([(self.__convertNone2empty_str(v)).upper() for _, v in vars(self).items()]))

    def __eq__(self, other):
        return hash(self) == hash(other)

class SearchHandler:
    def __check_search_params(self, args):
        check_url_params(args, SearchParam)

    def __prepare_search_cond(self):
        if request.method == "POST":
            request_params = request.form
        elif request.method == "GET":
            request_params = request.args
        else:
            abort(500, "method not support")

        self.__check_search_params(request_params)

        cond = SearchCond(request_params.get(SearchParam.name.value),
            request_params.get(SearchParam.year_start.value),
            request_params.get(SearchParam.year_end.value),
            request_params.get(SearchParam.source_lc.value),
            request_params.get(SearchParam.yn_region.value),
            request_params.get(SearchParam.current_page.value))

        cond.check_validation()

        return cond

    def search(self):
        search_cond = self.__prepare_search_cond()
        search_data = do_search(search_cond)
        count = search_data.get(f"{search_count_key}")
        pages = count // page_size + 1
        current_page = search_cond.get_current_page()

        search_data[f"{page_count_key}"] = pages
        search_data[f"{current_page_key}"] = current_page
        search_data[f"{page_next_key}"] = pages > current_page
        if current_page <= pages:
            search_data[f"{first_index_key}"], search_data[f"{last_index_key}"] = page_size * (current_page - 1), min(page_size * current_page - 1, count)
        else:
            search_data[f"{first_index_key}"], search_data[f"{last_index_key}"] = -1, -1
        return search_data

@lru_cache()
@respjson
def do_search(condition):
    return requests.get(f"{data_server}/{search}/?{condition.get_search_clause()}")

