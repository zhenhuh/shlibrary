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
        self.__check_wiki_params(request.args)

        name = request.args.get(WikiParam.name.value)
        wikitype = request.args.get(WikiParam.type.value)
        field = request.args.get(WikiParam.field.value)

        return query_wiki_info(name, wikitype, field)

@cache
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

    return requests.get(url)

if __name__ == "__main__":
    #app.run(host = "0.0.0.0", port = 8080, debug=True)
    # TODO
    pass
