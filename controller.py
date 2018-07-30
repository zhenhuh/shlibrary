from flask import Flask, render_template, request
from server import app
from util import *

@app.route("/")
@returnHTML
def index():
    return "index.html"

@app.route("/index/leftfrm", methods = ["POST"])
@returnjson
def index_leftfrm():
    from index_page import query_random_list
    return query_random_list()

@app.route("/index/rightfrm_letter", methods = ["POST"])
@returnjson
def index_rightfrm_letter():
    return "TODO"

@app.route("/index/rightfrm_label", methods = ["POST"])
@returnjson
def index_rightfrm_label():
    return "TODO"

@app.route("/index/rightfrm_aera", methods = ["POST"])
@returnjson
def index_rightfrm_aera():
    return "TODO"

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

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 8080, debug = True)