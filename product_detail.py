from flask import request, abort
from enum import Enum, unique
from wiki import query_wiki_info
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
        detail_info["wiki_info"] = query_wiki_info(name)

        return detail_info

@lru_cache()
@respjson()
def query_product_detail_from_local(id):
    return requests.get(f"{data_server}/{detail_info}/?id={id}")

if __name__ == "__main__":
    pass