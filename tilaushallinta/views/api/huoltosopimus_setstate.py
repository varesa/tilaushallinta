#
# This source code is licensed under the terms of the
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2015
#

from pyramid.view import view_config
from pyramid.response import Response
from tilaushallinta.models.maintenancejob import MaintenanceJob

from tilaushallinta.models import DBSession
from tilaushallinta.models import Tilaus
from tilaushallinta.models.huoltosopimus import Huoltosopimus


@view_config(route_name='huoltosopimus_setstate')
def view_huoltosopimus_setstate(request):
    sopimus_id = request.matchdict['id']
    newstate = request.POST['newstate']

    sopimus = DBSession.query(Huoltosopimus).filter_by(id=sopimus_id).first()
    sopimus.tila = newstate

    return Response('OK')


@view_config(route_name='huolto_setstate')
def view_huoltos_setstate(request):
    huolto_id = request.matchdict['id']
    newstate = request.POST['newstate']

    sopimus = DBSession.query(MaintenanceJob).filter_by(id=huolto_id).first()
    sopimus.tila = newstate

    return Response('OK')
