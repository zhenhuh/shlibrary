from flask import request, abort
from enum import Enum, unique
from xml.dom import minidom
from util import *
import requests

@unique
class PoemParam(Enum):
    name = "name"

ODD = 1

class PoemHandler:
    def __check_poem_params(self, args):
        check_url_params(args, PoemParam)
        if PoemParam.name.value not in args:
            abort(500, "name must has value")

    def get_poem_info_from_key(self, key):
        poem_resp = query_poem(key)

        return self.__prepare_poem(poem_resp, key)

    def get_poem_info(self):
        request_params = get_request_params()

        self.__check_poem_params(request_params)

        key = request_params.get(PoemParam.name.value)

        poem_resp = query_poem(key)

        return self.__prepare_poem(poem_resp, key)

    def __prepare_poem(self, json_data, key):

        def get_poem_data(poem_list, show_count):
            poem_data = {}
            poem_count = len(poem_list) if len(poem_list) < show_count else show_count
            poem_data[f"{poem_count_key}"] = poem_count

            @pick(poem_count)
            def get_poem_author_title_clause():
                poem_data_list = []
                for poem in poem_list:
                    author = poem.get(r"Author")
                    if author is None:
                        continue

                    title = poem.get(r"Title")
                    if title is None:
                        continue
                    title = title.get(r"Content")
                    if title is None:
                        continue

                    clauses = poem.get(r"Clauses")
                    if clauses is None:
                        continue
                    idx = 0
                    last_ju = ""
                    for clause in clauses:
                        ju = clause.get(r"Content")
                        last_ju = ju if idx == 0 else last_ju

                        if idx % 2 == ODD and ju.find(f"{key}") != -1:
                            last_ju = last_ju + ju
                            break
                        else:
                            if last_ju.find(f"{key}") != -1:
                                last_ju = last_ju + ju
                                break

                        last_ju = ju
                        idx += 1

                    poem_data_list.append({f"{poem_author}": author, f"{poem_title}": title, f"{poem_clause}": last_ju})

                return poem_data_list

            poem_data[f"{poem_data_key}"] = get_poem_author_title_clause()

            return poem_data

        poems = json_data.get(r"ShiData")
        if poems is None:
            return {f"{no_data}": ""}

        return get_poem_data(poems, 5)

@cache
@respjson()
def query_poem(key):
    return requests.get(f"https://api.sou-yun.com/api/poem/?key={key}&jsontype=true")

if __name__ == "__main__":
    pass