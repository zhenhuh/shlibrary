from flask import request, abort
from enum import Enum, unique
from server import app
from util import *
import requests

@unique
class LCParams(Enum):
    name = "name"
    wtime = "wtime"

class LocalChroniclesInfo:
    def __check_lc_params(self, args):
        check_url_params(args, LCParams)
        if LCParams.name.value not in args or LCParams.wtime.value not in args:
            abort(500, "name and wtime must have value")

    def get_lc_info(self):
        request_params = get_request_params()

        self.__check_lc_params(request_params)

        name = request_params.get(LCParams.name.value)
        wtime = request_params.get(LCParams.wtime.value)

        return query_lc_detail(name.strip(), wtime)

@cache
@respjson()
def query_lc_detail(name, wtime):
    return requests.get(f"{data_server}/{fz_detail}/?fzname={name}&wtime={wtime}")