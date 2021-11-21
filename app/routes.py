from flask import render_template, redirect, url_for, request, g, flash
from app import app
from app.forms import SearchForm
from app.Ticket_API import Request


@app.before_request
def before_request():
    g.search_form = SearchForm()
    g.R = Request()
    flag, content = g.R.getcount()
    if not flag:
        return render_template('requesterror.html', text=content)
    g.count = content


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/gettickets')
def gettickets():
    url = request.args.get('url', '', type=str)
    flag, content = g.R.ticketspage(url)
    if not flag:
        return render_template('requesterror.html', text=content)
    tickets, prevurl, nexturl = content
    prevurl = url_for('gettickets', url=prevurl) if prevurl else None
    nexturl = url_for('gettickets', url=nexturl) if nexturl else None
    return render_template('tickets.html', tickets=tickets, num=len(tickets), prev_url=prevurl, next_url=nexturl)


@app.route('/search')
def search():
    if g.search_form.validate_on_submit():
        id = str(g.search_form.id.data)
        flag, content = g.R.getticket(id)
        if not flag:
            return render_template('requesterror.html', text=content)
        if content[0]:
            return render_template('ticketdetail.html', ticket=content[1])
        else:
            flash(content[1])
            return redirect(url_for('index'))
    id = request.args.get('id', type=str)
    flag, content = g.R.getticket(id)
    if not flag:
        return render_template('requesterror.html', text=content)
    if content[0]:
        return render_template('ticketdetail.html', ticket=content[1])
    else:
        flash(content[1])
        return redirect(url_for('index'))