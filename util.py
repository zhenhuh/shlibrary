from flask import abort

# region data

resp_error_code = "error_code"
no_data = "zero_book"
breif_key = "breif"
detail_key = "detail"

# endregion data

# region decorator

def returnstr(func):
    def wrapper(*args, **kwargs):
        return str(func(*args, **kwargs))
    return wrapper

def respjson(func):
    def wrapper(*args, **kwargs):
        resp = func(*args, **kwargs)
        if resp.status_code == 200:
            return resp.json()

        return {f"{resp_error_code}" : resp.status_code }
    return wrapper

# endregion decorator

# region help function

def check_resp_status(content_json):
    if f"{resp_error_code}" in content_json:
        abort(500)

# endregion help function