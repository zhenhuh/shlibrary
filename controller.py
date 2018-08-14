from flask import Flask, render_template, request, redirect
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

@app.route("/index/rightfrm", methods = ["POST", "GET"])
@returnjson
def index_rightfrm():
    from index_page import query_right_all
    return query_right_all()

@app.route("/index/rightfrm_letter_click/", methods = ["POST", "GET"])
@returnjson
def index_rightfrm_letter_click():
    from index_page_click import Chessboard, ChessboardType
    chess = Chessboard(ChessboardType.letter)
    return chess.get_chessboard_data()

@app.route("/index/rightfrm_taxonomy_click/", methods = ["POST", "GET"])
@returnjson
def index_rightfrm_taxonomy_click():
    from index_page_click import Chessboard, ChessboardType
    chess = Chessboard(ChessboardType.taxonomy)
    return chess.get_chessboard_data()

@app.route("/index/rightfrm_region_click/", methods = ["POST", "GET"])
@returnjson
def index_rightfrm_region_click():
    from index_page_click import Chessboard, ChessboardType
    chess = Chessboard(ChessboardType.region)
    return chess.get_chessboard_data()

@app.route("/product_detail_test/", methods = ["POST", "GET"])
@jsut4test
@returnjson
def product_detail_test():
    from product_detail import ProductInfo
    prod = ProductInfo()
    return prod.get_product_info()

@app.route("/product_detail/", methods = ["GET"])
#@returnHTML
def product_detail_page():
    from product_detail import ProdParam
    id, name = get_request_params().get(ProdParam.id.value), get_request_params().get(ProdParam.name.value)
    #return "product_detail.html", {f"{ProdParam.id.value}": id, f"{ProdParam.name.value}": name}
    return render_template("product_detail.html", id = id, name = name)

@app.route("/fz_detail_test/", methods = ["POST", "GET"])
@jsut4test
@returnjson
def fz_detail_test():
    from fz_detail import LocalChroniclesInfo
    fz = LocalChroniclesInfo()
    return fz.get_lc_info()

@app.route("/fz_detail/", methods = ["GET"])
#@returnHTML
def fz_detail_page():
    from fz_detail import LocalChroniclesInfo
    fz = LocalChroniclesInfo()
    return render_template("fz_detail.html", fzdetail = fz.get_lc_info())

# shanghai library
## other gj
@app.route("/shlib/", methods = ["GET"])
@returnjson
def shlib_gj_action():
    from shlibrary import ShlibDataMgr
    shlib = ShlibDataMgr()
    return shlib.get_gj_detail_info()

## redirect
## person
@app.route("/shlib/person/", methods = ["GET"])
@tryredirect
def shlib_person_action():
    from shlibrary import ShlibDataMgr
    shlib = ShlibDataMgr()
    return shlib.get_redirect_url_for_person()

### place
@app.route("/shlib/place/", methods = ["GET"])
@tryredirect
def shlib_place_action():
    from shlibrary import ShlibDataMgr
    shlib = ShlibDataMgr()
    return shlib.get_redirect_url_for_place()

### dynasty
@app.route("/shlib/dynasty/", methods = ["GET"])
@tryredirect
def shlib_dynasty_action():
    from shlibrary import ShlibDataMgr
    shlib = ShlibDataMgr()
    return shlib.get_redirect_url_for_dynasty()

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

@app.route("/search_simple/", methods = ["GET", "POST"])
@returnjson
def search_simple_action():
    from search import SearchHandler
    searchHandler = SearchHandler()
    return searchHandler.search(True)

# statistics
@app.route("/wcstat/", methods = ["GET", "POST"])
@returnjson
def wc_statistics_action():
    from statistics import Statistics
    stat = Statistics()
    return stat.wc()

@app.route("/fzstat/", methods = ["GET", "POST"])
@returnjson
def fz_statistics_action():
    from statistics import Statistics
    stat = Statistics()
    return stat.fz()

# poem
@app.route("/poem/", methods=["GET", "POST"])
@jsut4test
@returnjson
def poem_action():
    from poem import PoemHandler
    poemHandler = PoemHandler()
    return poemHandler.get_poem_info()

# CBDB
@app.route("/cbdb/", methods = ["GET"])
@tryredirect
def cbdb_action():
    from cbdb import CBDB
    cbdb = CBDB()
    return cbdb.get_redirect_url_for_person()

if __name__ == "__main__":
    #app.run(host = "0.0.0.0", port = 8080, debug = True)
    import server
    server.run(True)