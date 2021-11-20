from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
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
