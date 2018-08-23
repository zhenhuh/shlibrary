from flask import request, abort, jsonify, render_template, redirect
from functools import wraps, lru_cache
from datetime import datetime, timedelta
import eventlet
import re

eventlet.monkey_patch()

DEBUG_ONLY = True

# region data

search_page_size = 10
chessboard_page_size = 24
timeout_secound = 30

## data server ip
def get_data_server():
    with open(r"conf\datasrv") as f:
        return f.readline()
data_server = get_data_server() # "http://47.97.124.135" # "http://localhost:2345"

resp_error_code = "error_code"
resp_timeout = "timeout"
no_data = "no_data"
breif_key = "breif"
detail_key = "detail"
gjdetail_count_key = "count"
gjdetail_data_key = "data"

## paginate
current_page_key = "current_page"
first_index_key = "first_index"
last_index_key = "last_index"
page_count_key = "page_count"
page_next_key = "page_next"
page_prev_key = "page_prev"

## index right
first_letter_key = "letter"
taxonomy_key = "taxonomy"
yn_region_key = "region"

## search resp json key
search_count_key = "count"
search_data_key = "data"
search_product_name_key = "product_name"
categories_key = "categories"
category_data_key = "category_data"
category_key = "category"

## detail resp json key
gj_list_key = "wcsource_qt"
gj_beautify_gj_list_key = "beautify_wcsource_qt"
gj_desc_key = "gjdesc"
wiki_info_key = "wiki_info"
related_poems_key = "poems"
map_location_key = "map_location"
wtime_key = "wtime"

## statistics
stat_fz_count_key = "count"
stat_fz_data_key = "data"
stat_map_location_key = "map_location"
stat_area_wccount_key = "stat_area_wccount"
stat_category_wccount_key = "stat_category_wccount"

## wiki type
baidu = "baidubaike"
hudong = "hudongbaike"
chinese = "zhwiki"

## poem key
poem_count_key = "count"
poem_data_key = "data"
poem_author = "author"
poem_title = "title"
poem_clause = "clause"

## action
search_simple = "RESTfulWS/JL/wc/fzwc"
search = "RESTfulWS/JL/wc/gjwc"
random_list = "RESTfulWS/JL/wc/list"
first_letter_list = "RESTfulWS/JL/wc/firstletter"
taxonomy_list = "RESTfulWS/JL/wc/taxonomy"
yn_region_list = "RESTfulWS/JL/wc/ynregion"

first_letter_info = "RESTfulWS/JL/wc/certainL"
taxonomy_info = "RESTfulWS/JL/wc/certainClass"
yn_region_info = "RESTfulWS/JL/wc/certainRegion"

wc_detail = "RESTfulWS/JL/jtwc/detail"
gj_detail = "RESTfulWS/JL/jtwc/gjdetail"
fz_detail = "RESTfulWS/JL/jtwc/lyfzDetail"
map_location = "RESTfulWS/JL/jtwc/lyplace"

wc_statistics_info = "RESTfulWS/JL/wc/tjwc"
fz_statistics_info = "RESTfulWS/JL/jtwc/allFZ"
wc_count_in_fz_info = "RESTfulWS/JL/jtwc/wcTJ"

# endregion data

# region decorator

def timeout(second):
    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                with eventlet.Timeout(second):
                    return func(*args, **kwargs)
            except eventlet.Timeout:
                return {f"{resp_timeout}" : f"{resp_timeout}: {second}"}

        return wrapper
    return inner

def pick(count):
    def inner(func):
        import random
        @wraps(func)
        def wrapper(*args, **kwargs):
            lst = func(*args, **kwargs)
            if len(lst) <= count:
                return lst

            random.shuffle(lst)
            return lst[:count]

        return wrapper
    return inner

def jsut4test(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if DEBUG_ONLY:
            return func(*args, **kwargs)
        abort(404, "Page not found")

    return wrapper

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

def tryredirect(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        url = func(*args, **kwargs)
        if url == "":
            render_template("404.html")
        return redirect(url)

    return wrapper


def respjson(ignoreJSONDecodeError_UntilGetData = False, ignoreJSONDecodeError_Onetime = True):
    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            resp = func(*args, **kwargs)
            if resp.status_code == 200:
                if not ignoreJSONDecodeError_UntilGetData:
                    if ignoreJSONDecodeError_Onetime:
                        try:
                            return resp.json()
                        except ValueError: # from simplejson import JSONDecodeError
                            return {}
                    return resp.json()
                else:
                    def consume_exceptions(gen):
                        action = next(gen)
                        while True:
                            try:
                                json_result = action(*args, **kwargs).json()
                            except ValueError: # from simplejson import JSONDecodeError
                                json_result = None

                            try:
                                action = gen.send(json_result)
                            except StopIteration:
                                return json_result

                    def try_do_infinitely():
                        while True:
                            json_data = yield func
                            if json_data is not None:
                                # raise StopIteration() # error in Python3.7 
                                return
                            continue

                    return consume_exceptions(try_do_infinitely())

            return {f"{resp_error_code}" : resp.status_code }

        return wrapper
    return inner

# endregion decorator

# region help function

def get_request_params():
    if request.method == "POST":
        request_params = request.form
    elif request.method == "GET":
        request_params = request.args
    else:
        abort(500, "method not support")

    return request_params

def check_url_params(args, whichdict):
    for each_arg in args:
        if each_arg not in [item.value for item in whichdict]:
            abort(400, f"{each_arg} is not supported. Params supported: " + " ".join(enum.value for enum in whichdict))

def check_resp_status(content_json, abort_when_fail = False):
    def abort_for(reason_key):
        if abort_when_fail:
            abort(500, "raw response status code: " + str(content_json.get(reason_key)))
        else:
            return False

    if f"{resp_error_code}" in content_json:
        abort_for(resp_error_code)
    elif f"{resp_timeout}" in content_json:
        abort_for(resp_timeout)

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

            try:
                return f(*args, **kwargs)
            except Exception as e:
                f.cache_clear()
                raise e

        return _wrapped
    return _wrapper

cache = timed_cache(hours = 2)

def get_paginate_info(count, page_size, current_page):
    if page_size <= 0:
        page_size = 1

    pages = count // page_size + (1 if count % page_size != 0 else 0)

    info = {}

    info[f"{page_count_key}"] = pages
    info[f"{current_page_key}"] = current_page
    info[f"{page_next_key}"] = pages > current_page
    info[f"{page_prev_key}"] = current_page >= 2
    if current_page <= pages:
        info[f"{first_index_key}"], info[f"{last_index_key}"] = page_size * (current_page - 1), min(page_size * current_page - 1, count - 1)
    else:
        info[f"{first_index_key}"], info[f"{last_index_key}"] = -1, -1

    return info

def is_mobile(user_agent):
    if not user_agent:
        return False

    is_mobile = False
    factor = user_agent
    _long_matches = r'googlebot-mobile|android|avantgo|blackberry|blazer|elaine|hiptop|ip(hone|od)|kindle|midp|mmp' \
                    r'|mobile|o2|opera mini|palm( os)?|pda|plucker|pocket|psp|smartphone|symbian|treo|up\.(browser|link)' \
                    r'|vodafone|wap|windows ce; (iemobile|ppc)|xiino|maemo|fennec'
    _long_matches = re.compile(_long_matches, re.IGNORECASE)
    _short_matches = r'1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)' \
                     r'|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)' \
                     r'|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw' \
                     r'|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8' \
                     r'|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit' \
                     r'|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)' \
                     r'|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji' \
                     r'|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|e\-|e\/|\-[a-w])|libw|lynx' \
                     r'|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(di|rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi' \
                     r'|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)' \
                     r'|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg' \
                     r'|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21' \
                     r'|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-' \
                     r'|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it' \
                     r'|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)' \
                     r'|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)' \
                     r'|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit' \
                     r'|wi(g |nc|nw)|wmlb|wonu|x700|xda(\-|2|g)|yas\-|your|zeto|zte\-'

    _short_matches = re.compile(_short_matches, re.IGNORECASE)

    if _long_matches.search(factor):
        is_mobile = True

    print(factor)

    if _short_matches.search(factor[0:4]):
        is_mobile = True

    return is_mobile

# endregion help function

# region etl for data

def remove_other_info_from_name(person_name):
    if not person_name:
        return ""

    temp_name = person_name.split(")")
    if len(temp_name) >= 2:
        temp_name = temp_name[1]
    else:
        temp_name = temp_name[0].split("）")
        if len(temp_name) >= 2:
            temp_name = temp_name[1]
        else:
            temp_name = temp_name[0]

    ends_dict = {
        "ends3" : ["续纂修"],
        "ends2" : ["增修", "纂修", "原纂", "续纂", "原修", "纂辑", "同纂", "增纂", "增订", "重校", "等纂"],
        "ends1" : ["纂", "修", "撰", "辑", "编", "校"]
    }
    for _, ends in ends_dict.items():
        for end in ends:
            if temp_name.endswith(end) and len(temp_name) > len(end) + 1:
                temp_name = temp_name.rstrip(end)
                return temp_name.strip()

    return temp_name.strip()

# endregion etl for data