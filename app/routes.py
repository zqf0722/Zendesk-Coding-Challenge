from flask import render_template, redirect, url_for, request, g, flash
from app import app
from app.forms import SearchForm
import requests
from requests.auth import HTTPBasicAuth


@app.before_request
def before_request():
    g.search_form = SearchForm()


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    url = app.config['SUB_DOMAIN']+'api/v2/tickets/count'
    r = requests.get(url, auth=HTTPBasicAuth(app.config['EMAIL_ADDRESS'], app.config['API_TOKEN']))
    num = r.json()['count']['value']
    return render_template('index.html', count=num)


@app.route('/gettickets')
def gettickets():
    defaulturl = app.config['SUB_DOMAIN'] + 'api/v2/tickets.json?page[size]=25'
    url = request.args.get('url', defaulturl, type=str)
    r = requests.get(url, auth=HTTPBasicAuth(app.config['EMAIL_ADDRESS'], app.config['API_TOKEN']))
    tickets = r.json()['tickets']
    prevurl = url_for('gettickets', url=r.json()['links']['prev']) if url != defaulturl else None
    nexturl = url_for('gettickets', url=r.json()['links']['next']) if r.json()['meta']['has_more'] else None
    return render_template('tickets.html', tickets=tickets, prev_url=prevurl, next_url=nexturl)


@app.route('/search')
def search():
    ticket_id = str(g.search_form.id.data)
    url = app.config['SUB_DOMAIN']+'api/v2/tickets/'+ticket_id
    r = requests.get(url, auth=HTTPBasicAuth(app.config['EMAIL_ADDRESS'], app.config['API_TOKEN']))
    if 'ticket' in r.json():
        ticket = r.json()['ticket']
        return render_template('ticketdetail.html', ticket=ticket)
    else:
        flash('Error, please input a valid id of a ticket')
        return redirect(url_for('index'))

