#
# This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Author: Esa Varemo
#

from pyramid.view import view_config
from pyramid.response import Response

from sqlalchemy import Table
from sqlalchemy.exc import NoSuchTableError

from ..models import Base, DBSession

@view_config(route_name='db', renderer='../templates/db_database.pt')
def view_db(request):
    models = []
    for table in Base.metadata.tables.keys():
        count = DBSession.execute(Table(table, Base.metadata, autoload=True).count()).scalar()
        models.append({'name': table, 'count': count})
    return {'models': models}

@view_config(route_name='db_model', renderer='../templates/db_model.pt')
def view_db_model(request):
    try:
        model = request.matchdict['name']

        table = Table(model, Base.metadata, autoload=True)
        select = table.select()

        rows = DBSession.execute(select).fetchall()

        return {'model': model, 'rows': rows}
    except NoSuchTableError:
        return Response("Virheellinen kysely")

@view_config(route_name='db_model_row', renderer='../templates/db_row.pt')
def view_db_model_row(request):
    try:
        model = request.matchdict['name']
        id = request.matchdict['id']

        table = Table(model, Base.metadata, autoload=True)
        select = table.select('id='+id)

        rows = DBSession.execute(select).fetchall()

        return {'model': model, 'rows': rows}
    except NoSuchTableError:
        return Response("Virheellinen kysely")
