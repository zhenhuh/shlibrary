from flask import Flask, render_template, request
from server import app
from util import *
from shlibrary import ShlibDataMgr
from wiki import Wiki

def get_userkey():
    with open(r"conf\key") as f:
        return f.readline()

userkey = get_userkey()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/index/leftfrm", methods = ["POST"])
def index_leftfrm():
    return "TODO"

@app.route("/index/rightfrm_letter", methods = ["POST"])
def index_rightfrm_letter():
    return "TODO"

@app.route("/index/rightfrm_label", methods = ["POST"])
def index_rightfrm_label():
    return "TODO"

@app.route("/index/rightfrm_aera", methods = ["POST"])
def index_rightfrm_aera():
    return "TODO"

# shanghai library other gj
@app.route("/shlib/", methods = ["GET"])
@returnstr
def shlib_gj_action():
    shlib = ShlibDataMgr()
    return shlib.get_gj_detail_info()

@app.route("/wiki/", methods = ["GET"])
@returnstr
def wiki_action():
    wiki = Wiki()
    return wiki.get_wiki_info()

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000, debug = True)