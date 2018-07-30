from flask import request, abort, jsonify
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
        return "&".join([f"{k}={v}" for k, v in vars(self).items() if v])

    def __convertNone2str(self, value):
        return value if value is not None else ""

    def __hash__(self):
        return hash("".join([(self.__convertNone2str(v)).upper() for _, v in vars(self).items()]))

    def __eq__(self, other):
        return hash(self) == hash(other)

class SearchHandler:
    def __check_search_params(self, args):
        check_url_params(args, SearchParam)

    def __prepare_search_cond(self):
        self.__check_search_params(request.args)

        cond = SearchCond(request.args.get(SearchParam.name.value),
            request.args.get(SearchParam.year_start.value),
            request.args.get(SearchParam.year_end.value),
            request.args.get(SearchParam.source_lc.value),
            request.args.get(SearchParam.yn_region.value),
            request.args.get(SearchParam.current_page.value))

        cond.check_validation()

        return cond

    def search(self):
        return do_search(self.__prepare_search_cond())

@lru_cache()
@respjson
def do_search(condition):
    return requests.get(f"{data_server}/search/?{condition.get_search_clause()}")
    # return """{"status_code":200,
    #         [{
    #         "uid" : 1,
    #         "product_name" : "松子",
    #         "temporal" : "明 景泰6年(1455)",
    #         "desc" : "	树皮無龍鳞而稍光滑枝上結松毬大如茶甌其中含寶有二三百粒者"
    #         },
    #         {
    #         "uid" : 2,
    #         "product_name" : "松子",
    #         "temporal" : "明 景泰6年(1455)",
    #         "desc" : "	树皮無龍鳞而稍光滑枝上結松毬大如茶甌其中含寶有二三百粒者"
    #         }]}"""

