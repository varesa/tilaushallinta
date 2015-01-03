#
# This source code is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2015
#

from pyramid.view import view_config

from tilaushallinta.models import Tilaus

from ..common import DBSession

@view_config(route_name='order_summary', renderer="../../templates/orders/order_summary.pt")
def view_order_summary(request):
    tilaus_id = request.matchdict['id']
    tilaus = DBSession.query(Tilaus).filter_by(id=tilaus_id).first()
    return {'tilaus': tilaus}
