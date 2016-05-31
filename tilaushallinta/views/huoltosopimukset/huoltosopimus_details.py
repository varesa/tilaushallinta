#
# This source code is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2016
#

import datetime

from pyramid.view import view_config
from pyramid.response import Response

from tilaushallinta.models import DBSession
from tilaushallinta.models.huoltosopimus import Huoltosopimus

from tilaushallinta.views.shared.update_tilaaja_kohde import update_kohde, update_tilaaja


def update_perustiedot(request):
    update_tilaaja(request.POST)
    update_kohde(request.POST)

    sopimus_id = request.matchdict['sopimus']
    sopimus = DBSession.query(Huoltosopimus).filter_by(id=sopimus_id).first()

    sopimus.muut_yhteysh = request.POST['muut_yhteysh']


@view_config(route_name='huoltosopimus_details', renderer='tilaushallinta.templates:huoltosopimus/huoltosopimus_details.pt')
def view_huoltosopimus_details(request):
    sopimus_id = request.matchdict['sopimus']
    sopimus = DBSession.query(Huoltosopimus).filter_by(id=sopimus_id).first()
    """:type: tilaushallinta.models.Huoltosopimus"""

    if 'data' in request.POST.keys():
        if request.POST['data'] == 'perustiedot':
            update_perustiedot(request)

        if request.POST['data'] == 'jobs':
            tyyppi_ke = 'huolto_ke' in request.POST.keys()
            if tyyppi_ke:
                try:
                    ke_starting_date = datetime.datetime.strptime(request.POST['huolto_ke_starting_date'],
                                                                  "%d.%m.%Y").date()
                except ValueError:
                    return Response("Error parsing date")
            else:
                ke_starting_date = None

            tyyppi_sy = 'huolto_sy' in request.POST.keys()
            if tyyppi_sy:
                try:
                    sy_starting_date = datetime.datetime.strptime(request.POST['huolto_sy_starting_date'],
                                                                  "%d.%m.%Y").date()
                except ValueError:
                    return Response("Error parsing date")
            else:
                sy_starting_date = None

            tyyppi_tk = 'huolto_tk' in request.POST.keys()
            if tyyppi_tk:
                tk_interval_months = float(request.POST['huolto_tk_interval_months'])
                try:
                    tk_starting_date = datetime.datetime.strptime(request.POST['huolto_tk_starting_date'],
                                                                  "%d.%m.%Y").date()
                except ValueError:
                    return Response("Error parsing date")
            else:
                tk_interval_months = None
                tk_starting_date = None

            sopimus.tyyppi_ke = tyyppi_ke
            sopimus.ke_starting_date = ke_starting_date
            sopimus.tyyppi_sy = tyyppi_sy
            sopimus.sy_starting_date = sy_starting_date
            sopimus.tyyppi_tk = tyyppi_tk
            sopimus.tk_starting_date = tk_starting_date
            sopimus.tk_interval_months = tk_interval_months

    return {'huoltosopimus': sopimus}
