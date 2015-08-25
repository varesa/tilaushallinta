#
# This source code is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2015
#

import datetime

from pyramid.view import view_config

from tilaushallinta.models import DBSession
from tilaushallinta.models.huoltosopimus import Huoltosopimus

from tilaushallinta.views.shared.update_tilaaja_kohde import update_kohde, update_tilaaja


def update_perustiedot(request):
    update_tilaaja(request.POST)
    update_kohde(request.POST)

    sopimus_id = request.matchdict['sopimus']
    sopimus = DBSession.query(Huoltosopimus).filter_by(id=sopimus_id).first()

    sopimus.muut_yhteysh = request.POST['muut_yhteysh']


@view_config(route_name='huoltosopimus_details', renderer='../../templates/huoltosopimus/huoltosopimus_details.pt')
def view_huoltosopimus_details(request):
    sopimus_id = request.matchdict['sopimus']
    sopimus = DBSession.query(Huoltosopimus).filter_by(id=sopimus_id).first()

    if 'data' in request.POST.keys():
        if request.POST['data'] == 'perustiedot':
            update_perustiedot(request)

    return {'huoltosopimus': sopimus}
