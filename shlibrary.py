from flask import request, abort
from enum import Enum, unique
from server import app
from util import *
import requests

def get_userkey():
    with open(r"conf\key") as f:
        return f.readline()

userkey = get_userkey()

@unique
class ShlibParam(Enum):
    gj = "gj"
    # redirect
    place = "place"
    dynasty = "dynasty"
    person = "person"
    instanceOfUri = "instanceOfUri"
    personUri = "personUri"

class ShlibDataMgr:

    def __check_shlib_params(self, args, *must_have):
        check_url_params(args, ShlibParam)
        for param in must_have:
            if param not in args:
                abort(500, f"{must_have} must has/have a value")

    def __make_brief_info(self, book_info):
        return book_info.update({"title" : book_info.get("dtitle", ""), "instanceOf" : ""})

    def __make_detail_info(self, book_info):
        return book_info.get("data")

    def get_gj_detail_info(self):
        request_params = get_request_params()

        self.__check_shlib_params(request_params, ShlibParam.gj.value)

        gj_name = request_params[ShlibParam.gj.value]
        all_books = query_brief_info_for(gj_name)
        if not check_resp_status(all_books):
            return {f"{no_data}" : ""}

        books = all_books.get("data")
        if books is None:
            return {f"{no_data}" : ""}
        else:
            book_infos = []
            for each_book in books:
                book_uri = each_book.get("uri", "")
                if len(book_uri) == 0:
                    book_infos.append(self.__make_brief_info(each_book))
                else:
                    book_infos.append(self.__make_detail_info(query_detail_info_for(book_uri)))
            return {f"{gjdetail_count_key}" : len(book_infos), f"{gjdetail_data_key}" : book_infos}

    # deal redirect
    def get_redirect_url_for_place(self):
        request_params = get_request_params()

        self.__check_shlib_params(request_params, ShlibParam.place.value)
        try:
            # data format is not json when no data
            resp = query_place_info(request_params[ShlibParam.place.value])
        except ValueError:
            return ""

        return resp.get("@id", "")

    def get_redirect_url_for_dynasty(self):
        request_params = get_request_params()

        self.__check_shlib_params(request_params, ShlibParam.dynasty.value)

        resp = query_dynasty_info(request_params[ShlibParam.dynasty.value])

        return resp["result"].get("uri", "")

    def get_redirect_url_for_person(self):
        request_params = get_request_params()

        self.__check_shlib_params(request_params, ShlibParam.person.value)

        name = remove_other_info_from_name(request_params[ShlibParam.person.value])
        resp = query_person_info(name)

        person_data = resp["data"]

        if len(person_data) == 0:
            return ""

        # assume no duplicate
        for person in person_data:
            if person.get("fname", "") == name:
                person_uri = person.get("uri", "")
                if len(person_uri) == 0:
                    break
                return f"http://names.library.sh.cn/mrgf/service/work/persons?uri={person_uri}&dataType=1"

        return ""

    def get_redirect_url_for_instanceOf_from_uri(self):
        request_params = get_request_params()

        self.__check_shlib_params(request_params, ShlibParam.instanceOfUri.value)

        return f"http://gj.library.sh.cn/gjxz/service/work/instance#uri={request_params[ShlibParam.instanceOfUri.value]}&type=1"

    def get_redirect_url_for_perosn_from_uri(self):
        request_params = get_request_params()

        self.__check_shlib_params(request_params, ShlibParam.personUri.value)

        return f"http://names.library.sh.cn/mrgf/service/work/persons?uri={request_params[ShlibParam.personUri.value]}&dataType=1"

@cache
@respjson()
def query_brief_info_for(gj_name):
    return requests.get(f"http://data1.library.sh.cn/gj/webapi/instances?title={gj_name}&key={userkey}")

@cache
@respjson()
def query_detail_info_for(gj_uri):
    return requests.get(f"http://data1.library.sh.cn/gj/webapi/instanceInfo?uri={gj_uri}&key={userkey}")

@cache
@respjson()
def query_person_info(name):
    return requests.get(f"http://data1.library.sh.cn/persons/data?fname={name}&key={userkey}")

@cache
@respjson()
def query_place_info(place):
    return requests.get(f"http://data1.library.sh.cn/place/{place}?key={userkey}")

@cache
@respjson()
def query_dynasty_info(dynasty):
    return requests.get(f"http://data1.library.sh.cn/data/{dynasty}.json?key={userkey}")

if __name__ == "__main__":
    #app.run(host = "0.0.0.0", port = 8080, debug=True)
    # TODO
    pass