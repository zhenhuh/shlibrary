from flask import abort

# region data

resp_error_code = "error_code"
no_data = "zero_book"
breif_key = "breif"
detail_key = "detail"

## wiki type
baidu = "baidubaike"
hudong = "hudongbaike"
chinese = "zhwiki"

# endregion data

# region decorator

def returnstr(func):
    def wrapper(*args, **kwargs):
        return str(func(*args, **kwargs))

    wrapper.__name__  = func.__name__ 
    return wrapper

def respjson(func):
    def wrapper(*args, **kwargs):
        resp = func(*args, **kwargs)
        if resp.status_code == 200:
            return resp.json()

        return {f"{resp_error_code}" : resp.status_code }

    wrapper.__name__  = func.__name__ 
    return wrapper

# endregion decorator

# region help function

def check_url_params(args, whichdict):
        for each_arg in args:
            if each_arg not in [item.value for item in whichdict]:
                abort(400)

def check_resp_status(content_json):
    if f"{resp_error_code}" in content_json:
        abort(500)

# endregion help function