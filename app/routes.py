from flask import render_template, redirect, url_for, request, g, flash
from app import app
from app.forms import SearchForm
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime


@app.before_request
def before_request():
    g.search_form = SearchForm()
    url = app.config['SUB_DOMAIN'] + 'api/v2/tickets/count'
    r = requests.get(url, auth=HTTPBasicAuth(app.config['EMAIL_ADDRESS'], app.config['API_TOKEN']))
    if r.status_code >= 400:
        text = r.text.replace('"', '')
        text = text.replace('{', '')
        text = text.replace('}', '')
        return render_template('requesterror.html', text=text)
    num = r.json()['count']['value']
    g.count = num


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/gettickets')
def gettickets():
    defaulturl = app.config['SUB_DOMAIN'] + 'api/v2/tickets.json?page[size]=25'
    url = request.args.get('url', defaulturl, type=str)
    r = requests.get(url, auth=HTTPBasicAuth(app.config['EMAIL_ADDRESS'], app.config['API_TOKEN']))
    if r.status_code >= 400:
        return render_template('requesterror.html', text=r.text)
    tickets = r.json()['tickets']
    for ticket in tickets:
        ticket['created_at'] = datetime.strptime(ticket['created_at'], "%Y-%m-%dT%H:%M:%SZ")
        ticket['updated_at'] = datetime.strptime(ticket['updated_at'], "%Y-%m-%dT%H:%M:%SZ")
    prevurl = url_for('gettickets', url=r.json()['links']['prev']) if url != defaulturl else None
    nexturl = url_for('gettickets', url=r.json()['links']['next']) if r.json()['meta']['has_more'] else None
    return render_template('tickets.html', tickets=tickets, num=len(tickets), prev_url=prevurl, next_url=nexturl)


@app.route('/search')
def search():
    if g.search_form.validate_on_submit():
        id = str(g.search_form.id.data)
        url = app.config['SUB_DOMAIN']+'api/v2/tickets/'+id
        r = requests.get(url, auth=HTTPBasicAuth(app.config['EMAIL_ADDRESS'], app.config['API_TOKEN']))
        if r.status_code >= 400:
            return render_template('requesterror.html', text=r.text)
        if 'ticket' in r.json():
            ticket = r.json()['ticket']
            ticket['created_at'] = datetime.strptime(ticket['created_at'], "%Y-%m-%dT%H:%M:%SZ")
            ticket['updated_at'] = datetime.strptime(ticket['updated_at'], "%Y-%m-%dT%H:%M:%SZ")
            return render_template('ticketdetail.html', ticket=ticket)
        else:
            flash('Error, please input a valid id of a ticket')
            return redirect(url_for('index'))
    id = request.args.get('id', type=str)
    url = app.config['SUB_DOMAIN'] + 'api/v2/tickets/' + id
    r = requests.get(url, auth=HTTPBasicAuth(app.config['EMAIL_ADDRESS'], app.config['API_TOKEN']))
    if r.status_code >= 400:
        return render_template('requesterror.html', text=r.text)
    if 'ticket' in r.json():
        ticket = r.json()['ticket']
        ticket['created_at'] = datetime.strptime(ticket['created_at'], "%Y-%m-%dT%H:%M:%SZ")
        ticket['updated_at'] = datetime.strptime(ticket['updated_at'], "%Y-%m-%dT%H:%M:%SZ")
        return render_template('ticketdetail.html', ticket=ticket)
    else:
        flash('Error, ticket went invalid.')
        return redirect(url_for('index'))