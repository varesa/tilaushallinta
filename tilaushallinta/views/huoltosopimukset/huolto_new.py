#
# This source code is licensed under the terms of the 
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2015
#

import datetime

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from tilaushallinta.models import DBSession, Huoltosopimus, Huolto


@view_config(route_name='huolto_new')
def view_huolto_new(request):
    sopimus_id = request.matchdict['sopimus']
    sopimus = DBSession.query(Huoltosopimus).filter_by(id=sopimus_id).first()

    huolto_tyyppi = request.matchdict['tyyppi']

    huolto = Huolto(date=datetime.datetime.now(),
                    tila=Huolto.TILA_UUSI, tyyppi=huolto_tyyppi,
                    huoltosopimus=sopimus)
    huolto_id = DBSession.query(Huolto).order_by(Huolto.id.desc()).first().id
    print(huolto.id)
    return HTTPFound(location="/huoltosopimukset/" + str(sopimus_id) + "/huolto/" + str(huolto_id))

