from bottle import template, run, request, Bottle, TEMPLATE_PATH

from src.database.Database import Database
from src.definition import TABLES, ROOT

app = Bottle()

TEMPLATE_PATH.append(f"{ROOT}/views")

if __name__ == '__main__':
    db = Database(TABLES.rj)
else:
    db = Database(TABLES.test)


@app.get("/")
def index():
    return template("index.tpl.html", saved=-1)


@app.post("/", method="POST")
def index_post():
    data = request.forms.get("data")
    return template("index.tpl.html", saved=db.save(data))


if __name__ == '__main__':
    run(app, host="localhost", port=10070, debug=True, reloader=True)
