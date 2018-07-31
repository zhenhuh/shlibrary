from flask import request, abort
from server import app
from util import *
import requests

@lru_cache()
@respjson
def query_random_list():
    return requests.get(f"{data_server}/{random_list}")

@lru_cache()
@respjson
def query_first_letter_list():
    return requests.get(f"{data_server}/{first_letter_list}")

@lru_cache()
@respjson
def query_taxonomy_list():
    return requests.get(f"{data_server}/{taxonomy_list}")

@lru_cache()
@respjson
def query_yn_region_list():
    return requests.get(f"{data_server}/{yn_region_list}")