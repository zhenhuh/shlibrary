from flask import request, abort
from enum import Enum, unique
from server import app
from util import *
from product_detail import query_map_location_from_local
import requests

@unique
class StatisticsParams(Enum):
    wcname = "wcname"

class Statistics:
    def __check_statistics_params(self, args):
        check_url_params(args, StatisticsParams)

        if StatisticsParams.wcname.value not in args:
            abort(500, "wcname must has value")

    def wc(self):
        self.__check_statistics_params(get_request_params())
        wcname = get_request_params().get(StatisticsParams.wcname.value)
        wcstat_info = query_wc_statistics(wcname)
        # need to add map info
        wcstat_info_data = wcstat_info.get("data")
        if wcstat_info_data:
            for each_info in wcstat_info_data:
                map_place = each_info.get("area_map")
                map_location = query_map_location_from_local(map_place)
                each_info[f"{stat_map_location_key}"] = map_location

        return wcstat_info

    def fz(self):
        fzstat_info = query_fz_statistics()
        # need to add wc count in each fz - done by db

        return {f"{stat_fz_count_key}" : len(fzstat_info), f"{stat_fz_data_key}" : fzstat_info }

@cache
@respjson()
def query_wc_statistics(name):
    return requests.get(f"{data_server}/{wc_statistics_info}/?wcname={name}")

@cache
@respjson()
def query_fz_statistics():
    return requests.get(f"{data_server}/{fz_statistics_info}")

# [deprecated]
@cache
@respjson()
def query_wc_count_in_fz(name):
    return requests.get(f"{data_server}/{wc_count_in_fz_info}/?fzname={name}")