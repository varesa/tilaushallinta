#
# This source code is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2015
#

import datetime

from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound


from tilaushallinta.models import DBSession
from tilaushallinta.models import Huoltosopimus
from tilaushallinta.views.misc.tilaaja_kohde import get_tilaaja_from_r, get_kohde_from_r


@view_config(route_name='huoltosopimus_new', renderer='../../templates/huoltosopimus/huoltosopimus_new.pt')
def view_huoltosopimus_new(request):
    """
    View method that shows the ordering form
    :param request: pyramid request
    :return: None
    """
    return {}


@view_config(route_name='huoltosopimus_submit')
def view_huoltosopimus_submit(request):
    """
    View method that the form is POSTed to
    :param request: Pyramid request
    :type request: pyramid.request.Request
    :return: None
    """
    try:
        tilaaja = get_tilaaja_from_r(request)
        kohde = get_kohde_from_r(request)

        tyyppi_ek = 'huolto_ek' in request.POST.keys()
        tyyppi_ke = 'huolto_ke' in request.POST.keys()
        tyyppi_sy = 'huolto_sy' in request.POST.keys()
        tyyppi_tk = 'huolto_tk' in request.POST.keys()

        tilaus = Huoltosopimus(date=datetime.datetime.now(),
                               tilaaja=tilaaja, kohde=kohde,
                               muut_yhteysh=request.POST['muut_yhteysh'],
                               tyo=request.POST['tyo'],
                               tyyppi_ek=tyyppi_ek, tyyppi_ke=tyyppi_ke,
                               tyyppi_sy=tyyppi_sy, tyyppi_tk=tyyppi_tk,
                               viitenumero=request.POST['viitenumero'])
        DBSession.add(tilaus)

        return HTTPFound('/texts/tilattu')
    except KeyError:
        return Response("Virhe käsiteltäessä lomaketta")