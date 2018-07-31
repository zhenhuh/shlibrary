from flask import abort, jsonify, render_template
from functools import wraps, lru_cache
from datetime import datetime, timedelta

# region data

page_size = 10

## data server ip
data_server = "http://localhost:2345"

resp_error_code = "error_code"
no_data = "zero_book"
breif_key = "breif"
detail_key = "detail"

## search resp json key
count_key = "count"
current_page_key = "current_page"
first_index_key = "first_index"
last_index_key = "last_index"
page_count_key = "page_count"
page_next_key = "page_next"

## wiki type
baidu = "baidubaike"
hudong = "hudongbaike"
chinese = "zhwiki"

## action
search = "RESTfulWS/JL/wc/gjwc"
random_list = "RESTfulWS/JL/wc/list"
first_letter_list = "RESTfulWS/JL/wc/firstletter"
taxonomy_list = "RESTfulWS/JL/wc/taxonomy"
yn_region_list = "RESTfulWS/JL/wc/ynregion"

detail_info = "RESTfulWS/JL/jtwc/detail"

# endregion data

# region decorator

def returnjson(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return jsonify(func(*args, **kwargs))

    return wrapper

def returnHTML(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return render_template(func(*args, **kwargs))

    return wrapper

def respjson(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        resp = func(*args, **kwargs)
        if resp.status_code == 200:
            return resp.json()

        return {f"{resp_error_code}" : resp.status_code }

    return wrapper

# endregion decorator

# region help function

def check_url_params(args, whichdict):
    for each_arg in args:
        if each_arg not in [item.value for item in whichdict]:
            abort(400, f"{each_arg} is not supported. Params supported: " + " ".join(enum.value for enum in whichdict))

def check_resp_status(content_json):
    if f"{resp_error_code}" in content_json:
        abort(500, "raw response status code: " + str(content_json.get(f"{resp_error_code}")))

# https://gist.github.com/Morreski/c1d08a3afa4040815eafd3891e16b945
def timed_cache(**timedelta_kwargs):
    def _wrapper(f):
        update_delta = timedelta(**timedelta_kwargs)
        next_update = datetime.utcnow() - update_delta
        # Apply @lru_cache to f with no cache size limit
        f = lru_cache(None)(f)

        @wraps(f)
        def _wrapped(*args, **kwargs):
            nonlocal next_update
            now = datetime.utcnow()
            if now >= next_update:
                f.cache_clear()
                next_update = now + update_delta
            return f(*args, **kwargs)
        return _wrapped
    return _wrapper

# endregion help function