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

import json
from tilaushallinta.utils import CustomJSONEncoder


@view_config(route_name='order_list_json')
def view_orders_list_json(request):
    orders = DBSession.query(Tilaus).all()

    result = json.dumps(orders, cls=CustomJSONEncoder)

    return Response(result)

