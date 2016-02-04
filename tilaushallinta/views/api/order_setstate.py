#
# This source code is licensed under the terms of the
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2016
#

from pyramid.view import view_config
from pyramid.response import Response

from tilaushallinta.models import DBSession
from tilaushallinta.models import Tilaus
from tilaushallinta.models.huoltosopimus import Huoltosopimus


@view_config(route_name='order_setstate')
def view_order_setstate(request):
    order_id = request.matchdict['id']
    newstate = request.POST['newstate']

    order = DBSession.query(Tilaus).filter_by(id=order_id).first()
    order.tila = newstate

    return Response('OK')
