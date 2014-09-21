#
# This source code is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014
#

from pyramid.view import view_config

from ..models import DBSession
from ..models import Kohde


@view_config(route_name='kohteet_list', renderer='../templates/kohde_list.pt')
def view_kohteet_list(request):
    kohteet = DBSession.query(Kohde).order_by(Kohde.uuid.desc()).all()

    latest = []
    lastid = None

    for kohde in kohteet:
        if kohde.id is not lastid:
            latest.append(kohde)
            lastid = kohde.id
    latest.reverse()
    return {"kohteet": latest}


@view_config(route_name='kohteet_details', renderer='../templates/kohde_details.pt')
def view_order_details(request):
    id = request.matchdict['id']
    kohde = DBSession.query(Kohde).filter_by(id=id).order_by(Kohde.uuid.desc()).first()

    return {'kohde': kohde, 'kohde_uuid': kohde.uuid}