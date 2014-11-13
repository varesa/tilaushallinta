#
# This source code is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014
#

from pyramid.view import view_config

from ..models import DBSession
from ..models import Kohde

from .utils import get_latest_ids


@view_config(route_name='kohteet_list', renderer='../templates/kohde_list.pt')
def view_kohteet_list(request):
    kohteet = get_latest_ids(DBSession.query(Kohde).all())
    return {"kohteet": kohteet}


@view_config(route_name='kohteet_details', renderer='../templates/kohde_details.pt')
def view_order_details(request):
    id = request.matchdict['id']
    kohde = DBSession.query(Kohde).filter_by(id=id).order_by(Kohde.uuid.desc()).first()

    return {'kohde': kohde, 'kohde_uuid': kohde.uuid}