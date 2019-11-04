from flask import Flask, render_template, request, redirect
from flask_cors import CORS
from server import app
from util import *

@app.route("/")
def index():
    user_agent = request.headers.get("User-Agent")
    return render_template("index.html", ismobile = is_mobile(user_agent))

@app.route("/amazing")
def amazing():
    return render_template("amazing.html")

@app.route("/404/")
def error():
    return render_template("404.html", info = get_request_params().get("info"))

@app.route("/index/leftfrm", methods = ["POST", "GET"])
@returnjson
def index_leftfrm():
    from index_page import query_random_list
    return {"count" : search_page_size, "data" : query_random_list()}

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

@app.route("/product_detail_data/", methods = ["POST", "GET"])
@jsut4test
@returnjson
def product_detail_data_action():
    from product_detail import ProductInfo
    prod = ProductInfo()
    return prod.get_product_info()

@app.route("/product_detail_data/nowiki/", methods = ["POST", "GET"])
@returnjson
def product_detail_data_without_wiki_action():
    from product_detail import ProductInfo
    prod = ProductInfo()
    return prod.get_product_info(ignore_wiki = True)

@app.route("/product_detail_data/wiki/", methods = ["POST", "GET"])
@returnjson
def product_detail_wiki_action():
    from product_detail import ProductInfo
    prod = ProductInfo()
    return prod.wiki_info()

@app.route("/product_detail/", methods = ["GET"])
#@returnHTML
def product_detail_page():
    from product_detail import ProdParam
    user_agent = request.headers.get("User-Agent")
    id, name = get_request_params().get(ProdParam.id.value), get_request_params().get(ProdParam.name.value)
    #return "product_detail.html", {f"{ProdParam.id.value}": id, f"{ProdParam.name.value}": name}
    return render_template("product_detail.html", id = id, name = name, ismobile = is_mobile(user_agent))

@app.route("/fz_detail_data/", methods = ["POST", "GET"])
#@jsut4test
@returnjson
def fz_detail_data():
    from fz_detail import LocalChroniclesInfo
    fz = LocalChroniclesInfo()
    return fz.get_lc_info()

@app.route("/fz_detail/", methods = ["GET"])
#@returnHTML
def fz_detail_page():
    from fz_detail import LocalChroniclesInfo
    user_agent = request.headers.get("User-Agent")
    fz = LocalChroniclesInfo()
    return render_template("fz_detail.html", fzdetail = fz.get_lc_info(), ismobile = is_mobile(user_agent))

# shanghai library
## other gj only data
@app.route("/shlib/gj_data/", methods = ["POST", "GET"])
@returnjson
def shlib_gj_data():
    from shlibrary import ShlibDataMgr
    shlib = ShlibDataMgr()
    return shlib.get_gj_detail_info()

## other gj
@app.route("/shlib/gj/", methods = ["GET"])
#@returnHTML
def shlib_gj_page():
    from shlibrary import ShlibDataMgr
    user_agent = request.headers.get("User-Agent")
    shlib = ShlibDataMgr()
    return render_template("gj_detail.html", gjdetail = shlib.get_gj_detail_info(), ismobile = is_mobile(user_agent))

## redirect
### gj person
@app.route("/shlib/gj/person/", methods = ["GET"])
@tryredirect
def shlib_gj_person_action():
    from shlibrary import ShlibDataMgr
    shlib = ShlibDataMgr()
    return shlib.get_redirect_url_for_perosn_from_uri()

### gj instanceOf
@app.route("/shlib/gj/instanceOf/", methods = ["GET"])
@tryredirect
def shlib_gj_instanceOf_action():
    from shlibrary import ShlibDataMgr
    shlib = ShlibDataMgr()
    return shlib.get_redirect_url_for_instanceOf_from_uri()

### person
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

@app.route("/fzstatfuzz/", methods = ["GET", "POST"])
@returnjson
def fz_statistics_fuzz_action():
    from statistics import Statistics
    stat = Statistics()
    return stat.fz_fuzz()

@app.route("/statistics/", methods = ["GET"])
#@returnHTML
def fz_statistics_page():
    user_agent = request.headers.get("User-Agent")
    return render_template("statistics.html", ismobile = is_mobile(user_agent))

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

@app.route("/produce/uri/<int:id>", methods = ["GET"])
def fzwc_produce_uri_action(id):
    from sparql.sparql import fzwc_produce_data_uri
    return fzwc_produce_data_uri(id)

@app.route("/produce/<string:showtype>/<int:id>", methods = ["GET"])
#@returnjson
def fzwc_produce_data_action(showtype, id):
    from sparql.sparql import fzwc_produce_data_select_from_id, fzwc_produce_data_construct_from_id
    JSON   = "json"
    JSONLD = "json-ld"
    XML    = "xml"
    TURTLE = "turtle"
    N3     = "n3"
    RDF    = "rdf"
    RDFXML = "rdf+xml"
    CSV    = "csv"
    TSV    = "tsv"
    output_type = str.lower(showtype)
    if output_type in set([JSON, XML]):
        return fzwc_produce_data_select_from_id(id, output_type)
    elif output_type in set([RDFXML]):
        return fzwc_produce_data_construct_from_id(id, output_type)
    else:
        return {}

@app.route("/fz/<string:showtype>/<int:id>", methods = ["GET"])
def fz_data_action(showtype, id):
    from sparql.chronicle import Chronicle
    JSON   = "json"

    output_type = str.lower(showtype)
    if output_type == JSON:
        fz = Chronicle()
        return fz.query_fz_data_from_id(id)
    else:
        return {}

@app.route("/uuid/produce/<string:showtype>/<string:uuid>", methods = ["GET"])
def produce_data_from_uuid_action(showtype, uuid):
    from sparql.sparql import fzwc_produce_data_select_from_uuid, fzwc_produce_data_construct_from_uuid
    JSON   = "json"
    RDFXML = "rdf+xml"
    output_type = str.lower(showtype)
    if output_type in set([JSON]):
        return fzwc_produce_data_select_from_uuid(uuid, output_type)
    elif output_type in set([RDFXML]):
        return fzwc_produce_data_construct_from_uuid(uuid, output_type)
    else:
        return {}

@app.route("/uuid/fz/<string:showtype>/<string:uuid>", methods = ["GET"])
def fz_data_from_uuid_action(showtype, uuid):
    from sparql.chronicle import Chronicle
    JSON   = "json"

    output_type = str.lower(showtype)
    if output_type == JSON:
        fz = Chronicle()
        return fz.query_fz_data_from_uuid(uuid)
    else:
        return {}

@app.route("/fz/ecnu/json/<int:id>", methods = ["GET"])
def ecnu_fz_data_action(id):
    from sparql.chronicle import Chronicle
    ecnu_fz = Chronicle()
    return ecnu_fz.query_ecnu_fz_data(id)

@app.route("/fz/fzwc/json/<int:id>", methods = ["GET"])
def fzwc_fz_data_action(id):
    from sparql.chronicle import Chronicle
    fzwc_fz = Chronicle()
    return fzwc_fz.query_fzwc_fz_data(id)

if __name__ == "__main__":
    #app.run(host = "0.0.0.0", port = 8080, debug = True)
    import server
    CORS(app, supports_credentials = True)
    server.run()