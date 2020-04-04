import json
import os
import sys

from bottle import template, run, request, Bottle, TEMPLATE_PATH, response

sys.path.insert(0, os.path.abspath("./"))
from src.database.sqlite3 import Database
from src.definition import TABLES, ROOT

app = Bottle()

TEMPLATE_PATH.append(f"{ROOT}/views")

if __name__ == "__main__":
    db = Database(TABLES.production)
else:
    db = Database(TABLES.test)


@app.get("/")
def index():
    return template("index.tpl.html", saved=-1)


@app.post("/", method="POST")
def index_post():
    data = request.forms.get("data")
    return template("index.tpl.html", saved=db.save(data))


@app.route("/api/exist", method="POST")
def api_exist():
    req = request.json
    if req is None:
        return {}

    body = json.dumps({"data": db.exist(req["data"])})
    response.headers["Content-Type"] = "application/json"
    return body


@app.route("/api/post", method="POST")
def api_post():
    req = request.json
    if req is None:
        return False

    db.save_many(req["data"])


@app.hook("after_request")
def enable_cors():
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST"
    response.headers[
        "Access-Control-Allow-Headers"
    ] = "Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token"


@app.route("<any:path>", method="OPTIONS")
def response_for_options(**kwargs):
    return {}


if __name__ == "__main__":
    run(app, host="localhost", port=10000)
