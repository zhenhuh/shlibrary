from flask import request, abort, jsonify
from functools import lru_cache
from enum import Enum, unique
from util import *
import requests

@unique
class SearchParam(Enum):
    search_name = "name"
    year_start = "year_start"
    year_end = "year_end"
    source_lc = "source_lc"
    yn_region = "yn_region"

class SearchCond:
    def __init__(self, search_name = None, year_start = None, year_end = None, source_lc = None, yn_region = None):
        self.search_name = search_name
        self.year_start = year_start
        self.year_end = year_end
        self.source_lc = source_lc
        self.yn_region = yn_region

    def CheckValidation(self):
        if not any([v for _, v in vars(self).items()]):
            abort(500, f"must specify one in " + " ".join(enum.value for enum in SearchParam))

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

        cond = SearchCond(request.args.get(SearchParam.search_name.value),
            request.args.get(SearchParam.year_start.value),
            request.args.get(SearchParam.year_end.value),
            request.args.get(SearchParam.source_lc.value),
            request.args.get(SearchParam.yn_region.value))

        cond.CheckValidation()

        return cond

    def search(self):
        return do_search(self.__prepare_search_cond())

@lru_cache()
@respjson
def do_search(condition):
    # for test
    return requests.get("http://zhishi.me/api/entity/本草纲目")
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

