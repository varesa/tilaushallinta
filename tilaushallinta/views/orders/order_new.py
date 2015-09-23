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
from tilaushallinta.models import Tilaus
from tilaushallinta.views.misc.tilaaja_kohde import get_tilaaja_from_r, get_kohde_from_r


@view_config(route_name='order_new', renderer='tilaushallinta.templates:orders/order_new.pt')
def view_order_new(request):
    """
    View method that shows the ordering form
    :param request: pyramid request
    :return: None
    """
    return {}


@view_config(route_name='order_submit')
def view_order_submit(request):
    """
    View method that the ordering form is POSTed to
    :param request: Pyramid request
    :return: None
    """
    try:
        tilaaja = get_tilaaja_from_r(request)
        kohde = get_kohde_from_r(request)

        if ('maksuaika' not in request.POST.keys()) or int(request.POST['maksuaika']) != 7:
            maksuaika = 14
        else:
            maksuaika = int(request.POST['maksuaika'])

        tilaus = Tilaus(date=datetime.datetime.now(),
                        tilaaja=tilaaja, kohde=kohde,
                        muut_yhteysh=request.POST['muut_yhteysh'],
                        tyo=request.POST['tyo'],
                        maksuaika=maksuaika,
                        viitenumero=request.POST['viitenumero'])
        DBSession.add(tilaus)

        return HTTPFound('/texts/tilattu')
    except KeyError:
        return Response("Virhe käsiteltäessä lomaketta")