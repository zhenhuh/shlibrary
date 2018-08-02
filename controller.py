from flask import Flask, render_template, request
from server import app
from util import *

@app.route("/")
@returnHTML
def index():
    return "index.html"

@app.route("/index/leftfrm", methods = ["POST", "GET"])
@returnjson
def index_leftfrm():
    from index_page import query_random_list
    return {"count" : page_size, "data" : query_random_list()}

@app.route("/index/rightfrm_letter", methods = ["POST", "GET"])
@returnjson
def index_rightfrm_letter():
    from index_page import query_first_letter_list
    return query_first_letter_list()

@app.route("/index/rightfrm_taxonomy", methods = ["POST", "GET"])
@returnjson
def index_rightfrm_taxonomy():
    from index_page import query_taxonomy_list
    return query_taxonomy_list()

@app.route("/index/rightfrm_region", methods = ["POST", "GET"])
@returnjson
def index_rightfrm_region():
    from index_page import query_yn_region_list
    return query_yn_region_list()

@app.route("/product_detail/", methods = ["GET"])
@returnHTML
def product_detail():
    return "product_detail.html"

# shanghai library other gj
@app.route("/shlib/", methods = ["GET"])
@returnjson
def shlib_gj_action():
    from shlibrary import ShlibDataMgr
    shlib = ShlibDataMgr()
    return shlib.get_gj_detail_info()

# wiki data
@app.route("/wiki/", methods = ["GET"])
@returnjson
def wiki_action():
    from wiki import Wiki
    wiki = Wiki()
    return wiki.get_wiki_info()

# search
@app.route("/search/", methods = ["GET", "POST"])
@returnjson
def search_action():
    from search import SearchHandler
    searchHandler = SearchHandler()
    return searchHandler.search()

# poem
@app.route("/poem/", methods = ["GET", "POST"])
@returnjson
def poem_action():
    from poem import PoemHandler
    poemHandler = PoemHandler()
    return poemHandler.get_poem_info()

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 8080, debug = True)