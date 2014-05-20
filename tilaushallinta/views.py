from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    )


@view_config(route_name='home', renderer='templates/tilauslomake.pt')
def my_view(request):
    try:
        #one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
        one = "abc"
    except DBAPIError:
        return Response("Database error", content_type='text/plain', status_int=500)
    return {'one': one, 'project': 'tilaushallinta'}