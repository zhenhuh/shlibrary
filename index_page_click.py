from flask import request, abort
from enum import Enum, unique
from server import app
from util import *
import requests

@unique
class ChessboardType(Enum):
    """
    letter / taxonomy / region
    """
    letter = "letter"
    taxonomy = "taxonomy"
    region = "region"

@unique
class ChessboardParam(Enum):
    """
    3 kinds of params
    """
    current_letter = "current_letter"
    current_taxonomy = "current_taxonomy"
    current_region = "current_region"
    current_page = "current_page"


class Chessboard:
    def __init__(self, type):
        if type not in ChessboardType:
            abort(500, f"{type} unknown")
        self.type = type

    def __check_chessboard_params(self, args):
        check_url_params(args, ChessboardParam)

        if ChessboardParam.current_page.value not in args:
            abort(500, "current_page must specify(start from 1)")

        if not (len(args) == 2 and (ChessboardParam.current_letter.value in args or ChessboardParam.current_taxonomy.value in args or ChessboardParam.current_region.value in args)):
            abort(500, "choose only one in current_letter , current_taxonomy , current_region")

    def get_chessboard_data(self):
        request_params = get_request_params()

        self.__check_chessboard_params(request_params)

        current_page = request_params.get(ChessboardParam.current_page.value)

        if ChessboardType.letter == self.type:
            letter = request_params.get(ChessboardParam.current_letter.value)
            return query_first_letter_info(letter, current_page)
        elif ChessboardType.taxonomy == self.type:
            taxonomy = request_params.get(ChessboardParam.current_taxonomy.value)
            return query_taxonomy_info(taxonomy, current_page)
        elif ChessboardType.region == self.type:
            region = request_params.get(ChessboardParam.current_region.value)
            return query_yn_region_info(region, current_page)
        else:
            pass

@cache
@respjson()
def query_first_letter_info(letter, page):
    return requests.get(f"{data_server}/{first_letter_info}/?letter={letter}&current_page={page}")

@cache
@respjson()
def query_taxonomy_info(taxonomy, page):
    return requests.get(f"{data_server}/{taxonomy_info}/?category={taxonomy}&current_page={page}")

@cache
@respjson()
def query_yn_region_info(region, page):
    return requests.get(f"{data_server}/{yn_region_info}/?region={region}&current_page={page}")