from flask import request, abort
from enum import Enum, unique
from server import app
from util import *
import requests

@unique
class CBDBParam(Enum):
    name = "name"

class CBDB:

    def __check_cbdb_params(self, args):
        check_url_params(args, CBDBParam)
        if CBDBParam.name.value not in args:
            abort(500, "name must has a value")

    def get_cbdb_info(self):
        request_params = get_request_params()

        self.__check_cbdb_params(request_params)

        name = request_params.get(CBDBParam.name.value)

        return query_cbdb(name)

@cache
@respjson()
def query_cbdb(name):
    return requests.get(f"https://cbdb.fas.harvard.edu/cbdbapi/person.php?name={name}&o=json")
