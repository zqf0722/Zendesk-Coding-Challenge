from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import EmptyForm
import requests
from requests.auth import HTTPBasicAuth


@app.route('/')
@app.route('/index', methods = ['GET','POST'])
def index():
    return render_template('index.html', title='Home')


@app.route('/gettickets')
def gettickets():
    defaulturl = app.config['SUB_DOMAIN'] + 'api/v2/tickets.json?page[size]=25'
    url = request.args.get('url', defaulturl, type=str)
    flash(url)
    r = requests.get(url, auth=HTTPBasicAuth(app.config['EMAIL_ADDRESS'], app.config['API_TOKEN']))
    tickets = r.json()['tickets']
    prevurl = url_for('gettickets', url=r.json()['links']['prev']) if url != defaulturl else None
    nexturl = url_for('gettickets', url=r.json()['links']['next']) if r.json()['meta']['has_more'] else None
    flash(prevurl)
    flash(nexturl)
    flash(url == defaulturl)
    return render_template('tickets.html', tickets=tickets, prev_url=prevurl, next_url=nexturl)
