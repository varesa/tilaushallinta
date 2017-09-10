#
# This source code is licensed under the terms of the 
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2016
#

import datetime

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from tilaushallinta.models import DBSession, Huoltosopimus, Huolto, HuoltoHintaluokka
from tilaushallinta.models.laiteluettelo import Laiteluettelo, Laite


@view_config(route_name='huolto_new')
def view_huolto_new(request):
    contract_id = request.matchdict['contract']
    contract = DBSession.query(Huoltosopimus).filter_by(id=contract_id).first()
    """:type contract: Huoltosopimus"""

    maintenance_type = request.matchdict['type']

    if maintenance_type == Huolto.TYYPPI_muu:
        msg = request.POST['muu_selite']
    else:
        msg = ""

    laiteluettelo = Laiteluettelo(date=datetime.datetime.now(),
                                  huoltosopimus=contract)
    huolto_last = DBSession.query(Huolto).filter_by(huoltosopimus=contract).order_by(Huolto.date.desc()).first()
    if huolto_last:
        for laite in huolto_last.laiteluettelo.laitteet:
            laiteluettelo.laitteet.append(Laite(date=laite.date, nimi=laite.nimi, tyyppitiedot=laite.tyyppitiedot,
                                                valmistusvuosi=laite.valmistusvuosi, maara=laite.maara,
                                                tyyppi=laite.tyyppi))

    hintaluokka = DBSession.query(HuoltoHintaluokka).filter_by(hintaluokka=1).first()

    huolto = Huolto(date=datetime.datetime.now(),
                    tila=Huolto.TILA_UUSI, tyyppi=maintenance_type, tyyppi_muu_selite=msg,
                    hintaluokka=hintaluokka, huoltosopimus=contract, laiteluettelo=laiteluettelo)
    huolto_id = DBSession.query(Huolto).order_by(Huolto.id.desc()).first().id

    contract.advance_date(maintenance_type)

    return HTTPFound(location="/huoltosopimukset/" + str(contract_id) + "/huolto/" + str(huolto_id))
