import requests
from requests.auth import HTTPBasicAuth
from app import app
from datetime import datetime
import json


def modtext(text):
    out = json.loads(text)
    return out


class Request():
    def __init__(self):
        self.errormessage = 'Invalid Response'

    def getcount(self):
        url = app.config['SUB_DOMAIN'] + 'api/v2/tickets/count'
        r = requests.get(url, auth=HTTPBasicAuth(app.config['EMAIL_ADDRESS'], app.config['API_TOKEN']))
        if r.status_code >= 400:
            text = modtext(r.text)
            return False, text['error']
        else:
            if 'count' not in r.json():
                return False, self.errormessage
            return True, r.json()['count']['value']

    def ticketspage(self, url):
        number = app.config['TICKETS_PER_PAGE']
        defaulturl = app.config['SUB_DOMAIN'] + 'api/v2/tickets.json?page[size]=' + str(number)
        if not url:
            url = app.config['SUB_DOMAIN'] + 'api/v2/tickets.json?page[size]=' + str(number)
        r = requests.get(url, auth=HTTPBasicAuth(app.config['EMAIL_ADDRESS'], app.config['API_TOKEN']))
        if r.status_code >= 400:
            text = modtext(r.text)
            return False, text['error']
        if 'tickets' not in r.json():
            return False, self.errormessage
        tickets = r.json()['tickets']
        for ticket in tickets:
            ticket['created_at'] = datetime.strptime(ticket['created_at'], "%Y-%m-%dT%H:%M:%SZ")
            ticket['updated_at'] = datetime.strptime(ticket['updated_at'], "%Y-%m-%dT%H:%M:%SZ")
        prevurl = r.json()['links']['prev'] if url != defaulturl else None
        nexturl = r.json()['links']['next'] if r.json()['meta']['has_more'] else None
        return True, (tickets, prevurl, nexturl)

    def alltickets(self):
        url = app.config['SUB_DOMAIN'] + 'api/v2/tickets'
        r = requests.get(url, auth=HTTPBasicAuth(app.config['EMAIL_ADDRESS'], app.config['API_TOKEN']))
        if r.status_code >= 400:
            text = modtext(r.text)
            return False, text['error']
        if 'tickets' not in r.json():
            return False, self.errormessage
        tickets = r.json()['tickets']
        for ticket in tickets:
            ticket['created_at'] = datetime.strptime(ticket['created_at'], "%Y-%m-%dT%H:%M:%SZ")
            ticket['updated_at'] = datetime.strptime(ticket['updated_at'], "%Y-%m-%dT%H:%M:%SZ")
        return True, tickets

    def getticket(self, id):
        url = app.config['SUB_DOMAIN'] + 'api/v2/tickets/' + str(id)
        r = requests.get(url, auth=HTTPBasicAuth(app.config['EMAIL_ADDRESS'], app.config['API_TOKEN']))
        if r.status_code >= 400:
            text = modtext(r.text)
            return False, text['error']
        if 'ticket' in r.json():
            ticket = r.json()['ticket']
            ticket['created_at'] = datetime.strptime(ticket['created_at'], "%Y-%m-%dT%H:%M:%SZ")
            ticket['updated_at'] = datetime.strptime(ticket['updated_at'], "%Y-%m-%dT%H:%M:%SZ")
            return True, (True, ticket)
        else:
            return True, (False, self.errormessage)
