from flask import request, abort
from enum import Enum, unique
from server import app
from util import *
import requests

@unique
class WikiParam(Enum):
    name = "entity"
    type = "wikitype"
    field = "property"

class Wiki:
    """
    Use data from : http://zhishi.me
    More info : http://zhishi.me/api
    """

    def __check_wiki_params(self, args):
        check_url_params(args, WikiParam)
        if WikiParam.name.value not in args:
            abort(500, "entity must has a value")

    def get_wiki_info(self):
        request_params = get_request_params()

        self.__check_wiki_params(request_params)

        name = request_params.get(WikiParam.name.value)
        wikitype = request_params.get(WikiParam.type.value)
        field = request_params.get(WikiParam.field.value)

        return query_wiki_info(name, wikitype, field)

    @classmethod
    def get_wiki_info_according2props(self, name, *props):
        result_list = []
        for each_prop in props:
            try:
                each_result = query_wiki_info(name=name, field=each_prop)
                if not check_resp_status(each_result):
                    continue
            except:
                continue

            result_list.append(each_result)

        def cmp_to_wiki_count(next_item):
            return len(next_item)

        result_list.sort(key = cmp_to_wiki_count, reverse = True)

        #print([len(e) for e in result_list])

        if len(result_list) == 0:
            return {}

        most_wiki_kind_result = result_list[0]
        for curr_wiki in most_wiki_kind_result:
            for result_item in result_list:
                curr_prop = result_item.get(curr_wiki)
                if curr_prop:
                    most_wiki_kind_result[curr_wiki].update(curr_prop)

        return most_wiki_kind_result

@cache
#@timeout(timeout_secound)
@respjson()
def query_wiki_info(name, wikitype = None, field = None):
    url = f"http://zhishi.me/api/entity/{name}" if wikitype is None and field is None else f"http://zhishi.me/api/entity/{name}?"

    if wikitype is not None and field is not None:
        url += f"baike={wikitype}&property={field}"
    elif wikitype is not None:
        url += f"baike={wikitype}"
    elif field is not None:
        url += f"property={field}"
    else:
        # no wikitype and no field
        pass

    return requests.get(url, verify = False, timeout = timeout_secound)

if __name__ == "__main__":
    #app.run(host = "0.0.0.0", port = 8080, debug=True)
    # TODO
    pass
