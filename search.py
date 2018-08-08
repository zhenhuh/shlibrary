from flask import request, abort
from functools import lru_cache, reduce
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

    def check_validation_simple(self):
        if not self.current_page or not self.name:
            abort(500, "current_page and name must have value")

    def get_search_clause(self):
        return "&".join([f"{k}={v}" if v else f"{k}=-1" for k, v in vars(self).items()])

    def get_search_simple_clause(self):
        return "&".join([f"{k}={v}" for k, v in vars(self).items() if v])

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

    def __prepare_search_cond(self, is_simple = False):
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

        if is_simple:
            cond.check_validation_simple()
        else:
            cond.check_validation()

        return cond

    def search(self, is_simple = False):
        search_cond = self.__prepare_search_cond(is_simple)
        search_data = do_search_simple(search_cond) if is_simple else do_search(search_cond)
        count = search_data.get(f"{search_count_key}")
        pages = count // page_size + 1
        current_page = search_cond.get_current_page()

        search_data[f"{page_count_key}"] = pages
        search_data[f"{current_page_key}"] = current_page
        search_data[f"{page_next_key}"] = pages > current_page
        search_data[f"{page_prev_key}"] = current_page >= 2
        if current_page <= pages:
            search_data[f"{first_index_key}"], search_data[f"{last_index_key}"] = page_size * (current_page - 1), min(page_size * current_page - 1, count - 1)
        else:
            search_data[f"{first_index_key}"], search_data[f"{last_index_key}"] = -1, -1

        idx = 0
        def add_category_for_each_data(data_list):
            # assume data list is sorted by product_name
            if len(data_list) == 0:
                return data_list

            first_data = data_list[idx]
            name = first_data[f"{search_product_name_key}"].strip()

            def deal_each_data(each_data):
                nonlocal idx, name
                if each_data[f"{search_product_name_key}"].strip() != name:
                    name = each_data[f"{search_product_name_key}"].strip()
                    idx += 1

                each_data[f"{category_key}"] = idx

            list(map(deal_each_data, data_list))
            return data_list

        search_data[f"{search_data_key}"] = add_category_for_each_data(search_data.get(f"{search_data_key}"))

        def create_catgory_data_node(category_dict, data_list):
            if len(data_list) == 0:
                return category_dict

            def add_to_dict(accu_dict, each_data):
                accu_dict.update({each_data[f"{search_product_name_key}"].strip() : each_data[(f"{category_key}")]})
                return accu_dict

            return reduce(add_to_dict, data_list, category_dict)

        search_data[f"{category_data_key}"] = create_catgory_data_node(dict(), search_data.get(f"{search_data_key}"))

        search_data[f"{categories_key}"] = idx + 1

        return search_data


@cache
@respjson()
def do_search(condition):
    return requests.get(f"{data_server}/{search}/?{condition.get_search_clause()}")

@cache
@respjson()
def do_search_simple(condition):
    return requests.get(f"{data_server}/{search_simple}/?{condition.get_search_simple_clause()}")
