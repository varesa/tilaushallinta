#
# This source code is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2015
#

from pyramid.view import view_config

from tilaushallinta.models import DBSession
from tilaushallinta.models.huoltosopimus import Huoltosopimus


@view_config(route_name='huoltosopimus_list', renderer='tilaushallinta.templates:maintenance_contract/maintenance_contract_list.pt')
def view_huoltosopimukset_list(request):
    huoltosopimukset = DBSession.query(Huoltosopimus).order_by(Huoltosopimus.date.desc()).all()
    return {"huoltosopimukset": huoltosopimukset}
