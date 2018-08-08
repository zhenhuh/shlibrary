from flask import request, abort
from enum import Enum, unique
from wiki import query_wiki_info
from poem import PoemHandler
from util import *
import requests

@unique
class ProdParam(Enum):
    id = "id"
    name = "name"

class ProductInfo:

    def __check_prod_params(self, args):
        check_url_params(args, ProdParam)
        if ProdParam.id.value not in args or ProdParam.name.value not in args:
            abort(500, "id and name must have value")

    def get_product_info(self):
        self.__check_prod_params(request.args)

        id = request.args.get(ProdParam.id.value)
        name = request.args.get(ProdParam.name.value)

        detail_info = query_product_detail_from_local(id)

        place_name_in_map = detail_info["mapPlace"]

        gj_list = detail_info.get(f"{gj_list_key}")
        if gj_list and len(gj_list) != 0:
            detail_list = query_gj_detail_from_local(name, gj_list)
            wc_desc_in_gj = {detail["gjsource"] : detail["gjdesc"] for detail in detail_list if len(detail["gjdesc"]) != 0}
        else:
            wc_desc_in_gj = {}

        detail_info[f"{gj_desc_key}"] = wc_desc_in_gj
        detail_info[f"{wiki_info_key}"] = query_wiki_info(name)

        poemHandler = PoemHandler()
        detail_info[f"{related_poems_key}"] = poemHandler.get_poem_info_from_key(name)

        detail_info[f"{map_location_key}"] = query_map_location_from_local(place_name_in_map)

        return detail_info

@cache
@respjson()
def query_product_detail_from_local(id):
    return requests.get(f"{data_server}/{detail_info}/?id={id}")

@cache
@respjson()
def query_gj_detail_from_local(name, gj_list):
    return requests.get(f"{data_server}/{gj_detail}/?wcname={name}&gjname={gj_list}")

@cache
@respjson()
def query_map_location_from_local(map_place):
    return requests.get(f"{data_server}/{map_location}/?place={map_place}")

if __name__ == "__main__":
    pass