from flask import request, abort
from server import app
from util import *
import requests

# @cache
@respjson(True)
def query_random_list():
    return requests.get(f"{data_server}/{random_list}")

@cache
@respjson()
def query_first_letter_list():
    return requests.get(f"{data_server}/{first_letter_list}")

@cache
@respjson()
def query_taxonomy_list():
    return requests.get(f"{data_server}/{taxonomy_list}")

@cache
@respjson()
def query_yn_region_list():
    return requests.get(f"{data_server}/{yn_region_list}")

def query_right_all():
    return {f"{first_letter_key}" : query_first_letter_list(), 
        f"{taxonomy_key}" : query_taxonomy_list(), 
        f"{yn_region_key}" : query_yn_region_list()}