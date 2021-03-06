#
# This source code is licensed under the terms of the
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2016
#

import string
import random

from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )

import db_env

from .root import Root
from .security import get_user_groups
from .views.login_management import view_login
from .routes import configure_routes


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    settings['sqlalchemy.url'] = db_env.substitute(settings['sqlalchemy.url'])


    engine = engine_from_config(settings, 'sqlalchemy.', pool_recycle=600)
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    try:
        with open('auth_token') as token_file:
            token = token_file.readline().strip()
    except FileNotFoundError:
        with open('auth_token', 'w') as token_file:
            new_token = ''.join([random.choice(string.ascii_letters + string.digits + string.punctuation) for n in range(30)])
            print("Generated new auth secret")
            token_file.write(new_token)
            token = new_token

    authn_policy = AuthTktAuthenticationPolicy(secret=token, callback=get_user_groups, hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()

    config = Configurator(settings=settings, root_factory=Root)
    config.include('pyramid_chameleon')
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.set_default_permission("authenticated")

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('extfiles', '../extfiles', cache_max_age=3600)

    configure_routes(config)

    config.scan()
    return config.make_wsgi_app()
