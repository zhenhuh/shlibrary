from flask import request, abort
from server import app
from util import *
import requests

@lru_cache()
@respjson
def query_random_list():
    return requests.get(f"{data_server}/{random_list}")