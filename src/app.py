import bottle
from bottle import template, run

from definition import ROOT

bottle.TEMPLATE_PATH.append(f"{ROOT}/src/views")


@bottle.route("/")
def index():
    return template("index.tpl.html", isDuplicated=-1)


if __name__ == '__main__':
    run(host="0.0.0.0", port=10070, debug=True)
