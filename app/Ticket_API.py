import requests
from requests.auth import HTTPBasicAuth
from app import app
from datetime import datetime
import json


# Modify the str type response message to json type to extract the error message
def modtext(text):
    out = json.loads(text)
    return out


# Request class for different types of requests
class Request():
    def __init__(self):
        # Init an error message to show when the response is invalid
        self.errormessage = 'Invalid Response'
        self.noenv = 'There is no environment arguments provided. The .env document is missing. Please unzip' \
                     'the env.rar file I attached in the email to find .env document and put it ' \
                     'on the top-level directory of the project.'

    def getcount(self):
        # Get the total number of tickets in the account
        if not app.config['SUB_DOMAIN']:
            return False, self.noenv
        url = app.config['SUB_DOMAIN'] + 'api/v2/tickets/count'
        r = requests.get(url, auth=HTTPBasicAuth(app.config['EMAIL_ADDRESS'], app.config['API_TOKEN']))
        if r.status_code >= 400:
            # Bad response
            text = modtext(r.text)
            return False, text['error']
        else:
            # Good response
            if 'count' not in r.json():
                # But response is invalid
                return False, self.errormessage
            # Valid response
            return True, r.json()['count']['value']

    def ticketspage(self, url, pageid=1):
        # Request for the pagination tickets. Takes a parameter url to specify which page to request
        if not app.config['SUB_DOMAIN']:
            return False, self.noenv
        number = app.config['TICKETS_PER_PAGE']
        defaulturl = app.config['SUB_DOMAIN'] + 'api/v2/tickets.json?page[size]=' + str(number)
        if not url:
            # If url is not specified, use the default url
            url = defaulturl
        r = requests.get(url, auth=HTTPBasicAuth(app.config['EMAIL_ADDRESS'], app.config['API_TOKEN']))
        if r.status_code >= 400:
            # Bad response
            text = modtext(r.text)
            return False, text['error']
        if 'tickets' not in r.json():
            # Invalid response
            return False, self.errormessage
        # Valid response
        tickets = r.json()['tickets']
        for ticket in tickets:
            # Change the str type timestamps to datetime type for moment.js to modify
            ticket['created_at'] = datetime.strptime(ticket['created_at'], "%Y-%m-%dT%H:%M:%SZ")
            ticket['updated_at'] = datetime.strptime(ticket['updated_at'], "%Y-%m-%dT%H:%M:%SZ")
        # If we are at the first page then the pageid is 1
        prevurl = r.json()['links']['prev'] if pageid != 1 else None
        # If we are at the last page then the 'has_more' attribute is False
        nexturl = r.json()['links']['next'] if r.json()['meta']['has_more'] else None
        # return pageid for unittest
        return True, (tickets, prevurl, nexturl, pageid)

    def alltickets(self):
        # Get all the tickets, not used in the application.
        if not app.config['SUB_DOMAIN']:
            return False, self.noenv
        url = app.config['SUB_DOMAIN'] + 'api/v2/tickets'
        r = requests.get(url, auth=HTTPBasicAuth(app.config['EMAIL_ADDRESS'], app.config['API_TOKEN']))
        if r.status_code >= 400:
            # Bad response
            text = modtext(r.text)
            return False, text['error']
        if 'tickets' not in r.json():
            # Invalid response
            return False, self.errormessage
        tickets = r.json()['tickets']
        for ticket in tickets:
            # Change the str type timestamps to datetime type for moment.js to modify
            ticket['created_at'] = datetime.strptime(ticket['created_at'], "%Y-%m-%dT%H:%M:%SZ")
            ticket['updated_at'] = datetime.strptime(ticket['updated_at'], "%Y-%m-%dT%H:%M:%SZ")
        return True, tickets

    def getticket(self, id):
        # Request for a single ticket with its id. Takes a parameter id to specify which ticket is requested
        if not app.config['SUB_DOMAIN']:
            return False, self.noenv
        url = app.config['SUB_DOMAIN'] + 'api/v2/tickets/' + str(id)
        r = requests.get(url, auth=HTTPBasicAuth(app.config['EMAIL_ADDRESS'], app.config['API_TOKEN']))
        if r.status_code >= 400:
            # Bad response
            text = modtext(r.text)
            return False, text['error']
        if 'ticket' in r.json():
            # Valid response
            ticket = r.json()['ticket']
            ticket['created_at'] = datetime.strptime(ticket['created_at'], "%Y-%m-%dT%H:%M:%SZ")
            ticket['updated_at'] = datetime.strptime(ticket['updated_at'], "%Y-%m-%dT%H:%M:%SZ")
            return True, (True, ticket)
        else:
            # Invalid response
            return True, (False, self.errormessage)
