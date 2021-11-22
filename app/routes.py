from flask import render_template, redirect, url_for, request, g, flash
from app import app
from app.forms import SearchForm
from app.Ticket_API import Request
import math


@app.before_request
def before_request():
    # Set up some global argument like the search form, Request object and the total number of tickets
    # These happen before the mainpage
    g.search_form = SearchForm()
    g.R = Request()
    flag, content = g.R.getcount()
    if not flag:
        return render_template('requesterror.html', text=content)
    g.count = content
    g.pages = math.ceil(g.count/int(app.config['TICKETS_PER_PAGE']))


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    # Mainpage
    return render_template('index.html')


@app.route('/gettickets')
def gettickets():
    # This page shows the pagination tickets we request
    url = request.args.get('url', '', type=str)
    pageid = request.args.get('pageid', 1, type=int)
    flag, content = g.R.ticketspage(url, pageid)
    if not flag:
        # Invalid response, direct to the request_error page
        return render_template('requesterror.html', text=content)
    # Unpack the content, we don't need the 4th value which is the pageid. It's returned only for unittest.
    tickets, prevurl, nexturl, _ = content
    prevurl = url_for('gettickets', url=prevurl, pageid=pageid-1) if prevurl else None
    # Deal with a special case when it's on the last page but the has_more is still true.
    nexturl = url_for('gettickets', url=nexturl, pageid=pageid+1) if nexturl and g.pages != pageid else None
    # Pass the value to the html file and show them there
    return render_template('tickets.html', tickets=tickets, num=len(tickets), prev_url=prevurl,
                           next_url=nexturl)


@app.route('/search')
def search():
    # This page shows the detailed information of a single ticket
    if g.search_form.validate_on_submit():
        # If the id is passed from the search form
        id = int(g.search_form.id.data)
        flag, content = g.R.getticket(id)
        if not flag:
            # Invalid response, direct to the request error page
            return render_template('requesterror.html', text=content)
        if content[0]:
            # Valid response, pass the value to the html and show them there
            # If not the first ticket, then there is a previous ticket
            prevurl = url_for('search', id=id-1) if id != 1 else None
            # If not the last ticket, then there is a next ticket
            nexturl = url_for('search', id=id+1) if id != g.count else None
            return render_template('ticketdetail.html', ticket=content[1], prev_url=prevurl, next_url=nexturl)
        else:
            # Invalid response, flash the error message and direct to the homepage
            flash(content[1])
            return redirect(url_for('index'))
    # If the id is passed from the pagination tickets
    id = request.args.get('id', type=int)
    flag, content = g.R.getticket(id)
    if not flag:
        # Invalid response, direct to the request error page
        return render_template('requesterror.html', text=content)
    if content[0]:
        # Valid response, pass the value to the html and show them there
        # If not the first ticket, then there is a previous ticket
        prevurl = url_for('search', id=id - 1) if id != 1 else None
        # If not the last ticket, then there is a next ticket
        nexturl = url_for('search', id=id + 1) if id != g.count else None
        return render_template('ticketdetail.html', ticket=content[1], prev_url=prevurl, next_url=nexturl)
    else:
        # Invalid response, flash the error message and direct to the homepage
        flash(content[1])
        return redirect(url_for('index'))
