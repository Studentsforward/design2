from flask import current_app, render_template, request, redirect, url_for, make_response, abort
from flask_login import login_required, login_user, logout_user, current_user

from config import AUTHOMATIC_CONFIG
from plaid import Client
import os

from authomatic import Authomatic
from authomatic.adapters import WerkzeugAdapter

import logging
import facebook

from . import main
from .forms import LoginForm
from .. import db
from .. import User
from .. import login_manager
from .. import AUTHOMATIC_CONFIG


authomatic = Authomatic(config=AUTHOMATIC_CONFIG,
                        secret="config.SECRET",
                        report_errors=True,
                        logging_level=logging.DEBUG)


@main.route('/signup', methods=['GET', 'POST'])
def signup():
    form = LoginForm()
    if form.validate_on_submit():

        if(User.query.filter_by(email=request.form['email']).first() is None):
            u = User(email=request.form['email'])
            u.set_password(request.form['password'])
            db.session.add(u)
            db.session.commit()
            login_user(u)
        current_app.logger.info(str(request.form))

        return "Success!"
    return render_template('create_account.html', form=form)

@main.route('/signup/<provider_name>', methods=['GET', 'POST'])
def signup_facebook(provider_name):
    response = make_response()
    print(type(response))
    print(dir(response))
    print(response)
    result = authomatic.login(WerkzeugAdapter(request, response), provider_name)
    if result and result.user:
        token = result.user.data['access_token']
        facebook_graph = facebook.GraphAPI(token)
        args = {'fields': 'id,name,email', }
        info = facebook_graph.get_object('me', **args)

        if(User.query.filter_by(email=info['email']).first() is None):
            u = User(email=info['email'])
            print("FACEBOOK!!!", dir(u))
            db.session.add(u)
            db.session.commit()
            login_user(u)

        return render_template('index.html', users=User.query.all(), user=str(current_user))
    return response

@main.route('/login', methods=['GET', 'POST'])
def login():
    return ""

@main.route('/login/<provider_name>/', methods=['GET', 'POST'])
def login_provider(provider_name):
    response = make_response()
    result = authomatic.login(WerkzeugAdapter(request, response), provider_name)
    if result and result.user:
        token = result.user.data['access_token']
        facebook_graph = facebook.GraphAPI(token)
        args = {'fields': 'id,name,email', }
        info = facebook_graph.get_object('me', **args)
        return render_template('login.html', result=info['email'])
    return response

@main.route('/home')
def home():
    return render_template('index2.html')

@main.route('/')
def index():
    all_users = User.query.all()
    return render_template('index.html', users=all_users, user=str(current_user))

@main.route('/authenticate', methods=['POST'])
def authenticate():
    # request.form =
    # ImmutableMultiDict([('institution[name]', 'Chase'),
    #                     ('institution[type]', 'chase'),
    #                     ('public_token', 'test,chase,connected')])

    if(User.query.filter_by(public_token=request.form['public_token']).first() is None):
        #u = User(public_token=request.form['public_token'])
        current_user.public_token = request.form['public_token']
        db.session.add(current_user)
        db.session.commit()

    # print(f'Form: {request.form}')

    client = Client(client_id='5824eec946eb126b6a860966',
                    secret=os.environ['SECRET_KEY'])

    print("Public token: ", request.form['public_token'])

    response = client.exchange_token(request.form['public_token'])

    user = Client(client_id='5824eec946eb126b6a860966',
                  secret=os.environ['SECRET_KEY'],
                  access_token=response.json()['access_token'])

    available = sum([float(row['balance']['available'])
                    for row in user.balance().json()['accounts']])

    return render_template('info.html',
                           available=available,
                           accounts=user.auth_get().json(),
                           balances=user.balance().json(),
                           transactions=user.connect_get().json()['transactions']
                           # info=user.info_get().json(),
                           # income=user.income_get().json(),
                           # risk=user.risk_get().json()
                           )

# somewhere to logout
@main.route("/logout")
@login_required
def logout():
    logout_user()
    return '<p>Logged out</p>'

@login_manager.user_loader
def load_user(userid):
    return User.query.filter_by(id=userid).first()
