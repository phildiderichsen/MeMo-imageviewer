
import csv
from flask import Flask, render_template, request, redirect, url_for
import requests
from pager import Pager


def read_table(url):
    """Return a list of dict"""
    # r = requests.get(url)
    with open(url) as f:
        return [row for row in csv.DictReader(f.readlines())]


APPNAME = "Faksimiler"
STATIC_FOLDER = 'example'
TABLE_FILE = "example/fakecatalog.csv"

table = read_table(TABLE_FILE)
pager = Pager(len(table))


app = Flask(__name__, static_folder=STATIC_FOLDER)
app.config.update(
    APPNAME=APPNAME,
    )


@app.route('/')
def index():
    return redirect('/0')


@app.route('/<int:ind>/')
def image_view(ind=None):
    if ind >= pager.count:
        return render_template("404.html"), 404
    else:
        pager.current = ind
        return render_template(
            'imageview.html',
            index=ind,
            pager=pager,
            data=table[ind])


@app.route('/<filename>/')
def page_view(filename=None):
    if filename != '1874_Albertius_BjergmandensRing_2':
        return render_template("404.html"), 404
    else:
        pager.current = 0
        return render_template(
            'pageview.html',
            index=0,
            pager=pager)


@app.route('/goto', methods=['POST', 'GET'])    
def goto():
    return redirect('/' + request.form['index'])


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
