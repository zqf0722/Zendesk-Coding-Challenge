from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import EmptyForm
import requests
from requests.auth import HTTPBasicAuth


@app.route('/')
@app.route('/index', methods = ['GET','POST'])
def index():
    tickets = [
        {
            "subject": "Help, my printer is on fire!",
            "requester_id": '20978392',
            "created_at": "2009-07-20T22:55:29Z"
        },
        {
            "subject": "Testing tickets for fun",
            "requester_id": '7777777',
            "created_at": "2021-11-19T23:20:29Z"
        }
    ]
    return render_template('index.html', title='Home', tickets=tickets)


@app.route('/gettickets')
def gettickets():
    url = app.config['SUB_DOMAIN']+'api/v2/tickets'
    r = requests.get(url, auth=HTTPBasicAuth(app.config['EMAIL_ADDRESS'], app.config['API_TOKEN']))
    return r.json()
