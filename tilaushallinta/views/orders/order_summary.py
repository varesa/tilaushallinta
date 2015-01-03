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

    luokka1 = False
    luokka2 = False
    luokka3 = False
    for raportti in tilaus.paivaraportit:
            if raportti.hintaluokka == 1:
                    if not luokka1:
                            luokka1 = {'tunnit': 0.0, 'matkat': 0.0, 'muut': 0.0}
                    luokka1['tunnit'] += raportti.tunnit
                    luokka1['matkat'] += raportti.matkat
                    luokka1['muut']   += raportti.muut
            if raportti.hintaluokka == 2:
                    if not luokka2:
                            luokka2 = {'tunnit': 0.0, 'matkat': 0.0, 'muut': 0.0}
                    luokka2['tunnit'] += raportti.tunnit
                    luokka2['matkat'] += raportti.matkat
                    luokka2['muut']   += raportti.muut
            if raportti.hintaluokka == 3:
                    if not luokka3:
                            luokka3 = {'tunnit': 0.0, 'matkat': 0.0, 'muut': 0.0}
                    luokka3['tunnit'] += raportti.tunnit
                    luokka3['matkat'] += raportti.matkat
                    luokka3['muut']   += raportti.muut

    return {'tilaus': tilaus, 'luokka1': luokka1, 'luokka2': luokka2, 'luokka3': luokka3}

