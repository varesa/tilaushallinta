#
# This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Author: Esa Varemo
#

from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')

    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('home', '/')

    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    config.add_route('order_list', '/tilaukset')
    config.add_route('order_details', '/tilaukset/{id}')

    config.add_route('show_text', '/texts/{name}')

    config.add_route('tilaus', '/tilaus')
    config.add_route('tilaus_submit', '/tilaus_submit')

    config.add_route('db', '/db')
    config.add_route('db_model', '/db/{name}')
    config.add_route('db_model_row', '/db/{name}/{id}')

    config.scan()
    return config.make_wsgi_app()
