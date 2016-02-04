#
# This source code is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2016
#

from pyramid.view import view_config

from ..models import DBSession
from ..models import Kohde


@view_config(route_name='kohteet_list', renderer='tilaushallinta.templates:kohteet/kohde_list.pt')
def view_kohteet_list(request):
    kohteet = DBSession.query(Kohde).all()
    return {"kohteet": kohteet}


@view_config(route_name='kohteet_details', renderer='tilaushallinta.templates:kohteet/kohde_details.pt')
def view_kohde_details(request):
    id = request.matchdict['id']
    kohde = DBSession.query(Kohde).filter_by(id=id).first()

    return {'kohde': kohde, 'kohde_id': kohde.id} # TODO: check if kohde_id is required
