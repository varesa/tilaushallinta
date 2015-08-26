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
from tilaushallinta.models.laiteluettelo import Laiteluettelo, Laite


@view_config(route_name='huolto_new')
def view_huolto_new(request):
    sopimus_id = request.matchdict['sopimus']
    sopimus = DBSession.query(Huoltosopimus).filter_by(id=sopimus_id).first()

    huolto_tyyppi = request.matchdict['tyyppi']


    laiteluettelo = Laiteluettelo(date=datetime.datetime.now(),
                                  huoltosopimus=sopimus)
    huolto_last = DBSession.query(Huolto).filter_by(huoltosopimus=sopimus).order_by(Huolto.date.desc()).first()
    if huolto_last:
        for laite in huolto_last.laiteluettelo.laitteet:
            laiteluettelo.laitteet.append(Laite(date=laite.date, nimi=laite.nimi, tyyppitiedot=laite.tyyppitiedot,
                                                valmistusvuosi=laite.valmistusvuosi, maara=laite.maara,
                                                tyyppi=laite.tyyppi))

    huolto = Huolto(date=datetime.datetime.now(),
                    tila=Huolto.TILA_UUSI, tyyppi=huolto_tyyppi,
                    huoltosopimus=sopimus, laiteluettelo=laiteluettelo)
    huolto_id = DBSession.query(Huolto).order_by(Huolto.id.desc()).first().id
    print(huolto.id)
    return HTTPFound(location="/huoltosopimukset/" + str(sopimus_id) + "/huolto/" + str(huolto_id))

