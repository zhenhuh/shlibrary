from flask import Flask, render_template, request
from server import app
from util import *
from shlibrary import ShlibDataMgr
from wiki import Wiki

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/index/leftfrm", methods = ["POST"])
@returnjson
def index_leftfrm():
    return "TODO"

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

# shanghai library other gj
@app.route("/shlib/", methods = ["GET"])
@returnjson
def shlib_gj_action():
    shlib = ShlibDataMgr()
    return shlib.get_gj_detail_info()

# wiki data
@app.route("/wiki/", methods = ["GET"])
@returnjson
def wiki_action():
    wiki = Wiki()
    return wiki.get_wiki_info()

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000, debug = True)