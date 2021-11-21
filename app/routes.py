from flask import render_template, redirect, url_for, request, g, flash
from app import app
from app.forms import SearchForm
from app.Ticket_API import Request


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


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    # Mainpage
    return render_template('index.html')


@app.route('/gettickets')
def gettickets():
    # This page shows the pagination tickets we request
    url = request.args.get('url', '', type=str)
    flag, content = g.R.ticketspage(url)
    if not flag:
        # Invalid response, direct to the request_error page
        return render_template('requesterror.html', text=content)
    # Unpack the content
    tickets, prevurl, nexturl = content
    prevurl = url_for('gettickets', url=prevurl) if prevurl else None
    nexturl = url_for('gettickets', url=nexturl) if nexturl else None
    # Pass the value to the html file and show them there
    return render_template('tickets.html', tickets=tickets, num=len(tickets), prev_url=prevurl, next_url=nexturl)


@app.route('/search')
def search():
    # This page shows the detailed information of a single ticket
    if g.search_form.validate_on_submit():
        # If the id is passed from the search form
        id = str(g.search_form.id.data)
        flag, content = g.R.getticket(id)
        if not flag:
            # Invalid response, direct to the request error page
            return render_template('requesterror.html', text=content)
        if content[0]:
            # Valid response, pass the value to the html and show them there
            return render_template('ticketdetail.html', ticket=content[1])
        else:
            # Invalid response, flash the error message and direct to the homepage
            flash(content[1])
            return redirect(url_for('index'))
    # If the id is passed from the pagination tickets
    id = request.args.get('id', type=str)
    flag, content = g.R.getticket(id)
    if not flag:
        # Invalid response, direct to the request error page
        return render_template('requesterror.html', text=content)
    if content[0]:
        # Valid response, pass the value to the html and show them there
        return render_template('ticketdetail.html', ticket=content[1])
    else:
        # Invalid response, flash the error message and direct to the homepage
        flash(content[1])
        return redirect(url_for('index'))
