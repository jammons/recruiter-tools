from collections import defaultdict
import datetime
import json
import requests
from requests.auth import HTTPBasicAuth

from flask import Flask, send_from_directory
from flask import render_template
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config_file.cfg')
app.secret_key = app.config['SECRET_KEY']

Bootstrap(app)
db = SQLAlchemy(app)


class Interviewer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<Interviewer %r>' % self.name


def load_names_from_list():

    included_names = [
        # Add name strings here to put them in the DB with this method
    ]

    for name in included_names:
        interviewer = Interviewer(name=name)
        db.session.add(interviewer)
    db.session.commit()


def fetch_scheduled_interviews(starts_after, ends_before):
    '''
    Fetches all scheduled interviews starting after `starts_after` date and
    ending before `ends_before`.

    This method handles pagination and returns an array of dictionaries
    derived from the JSON returned by the API.
    '''
    auth = HTTPBasicAuth(app.config['GREENHOUSE_KEY'], '')

    params = {
        'starts_after': starts_after,
        'ends_before': ends_before,
        'per_page': 100,
    }
    url = 'https://harvest.greenhouse.io/v1/scheduled_interviews'

    page = 1
    result_count = -1
    results = []

    while result_count != 0:  # keep going until an empty page
        params['page'] = page

        r = requests.get(
            url,
            auth=auth,
            params=params,
        )

        c = json.loads(r.content)
        results += c

        page += 1
        result_count = len(c)

    return results


@app.route('/')
def show_interview_counts():
    '''
    Fetches and displays the counts of interviews scheduled to occur from 4
    days ago to 4 days in the future. Counts per interviewer and renders a
    table of results.
    '''
    interviewers = defaultdict(int)
    product_dev_interviewers = \
        [interviewer.name for interviewer in Interviewer.query.all()]

    today = datetime.datetime.now()
    days = datetime.timedelta(days=4)
    starts_after = today - days
    ends_before = today + days

    interviews = fetch_scheduled_interviews(
        starts_after,
        ends_before
    )
    for interview in interviews:
        for interviewer in interview['interviewers']:
            if interviewer['name'] in product_dev_interviewers:
                interviewers[interviewer['name']] += 1

    return render_template(
        'home.html',
        interviewers=interviewers,
        starts_after=starts_after,
        ends_before=ends_before,
        today=today,
    )


######################## ADMIN PAGES  ######################## # noqa
admin = Admin(app, name='recruiting_tools')
admin.add_view(ModelView(Interviewer, db.session))


######################## STATIC SERVING ######################## # noqa
@app.route('/vendor/<path:path>')
def send_vendor(path):
    return send_from_directory('vendor', path)


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)
################################################################
