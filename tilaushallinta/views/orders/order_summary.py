#
# This source code is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2015
#

from pyramid.view import view_config

from tilaushallinta.models import Tilaus, Hintaluokka

from ..common import DBSession


def get_quantities(raportit, hintaluokka):
    quantities = False
    for raportti in raportit:
        if raportti.hintaluokka == hintaluokka:
            if not quantities:
                quantities = {'tunnit': 0.0, 'matkat': 0.0, 'muut': 0.0}
            quantities['tunnit'] += raportti.tunnit
            quantities['matkat'] += raportti.matkat
            quantities['muut']   += raportti.muut
    return quantities


def get_totals(raportit, hintaluokka_no):
    totals = {'tunnit': 0.0, 'matkat': 0.0, 'muut': 0.0}
    hintaluokka = DBSession.query(Hintaluokka).filter_by(hintaluokka=hintaluokka_no).first()
    for raportti in raportit:
        if raportti.hintaluokka == hintaluokka_no:
            totals['tunnit'] += raportti.tunnit * hintaluokka.tunnit
            totals['matkat'] += raportti.matkat * hintaluokka.matkat
            totals['muut']   += raportti.muut
    return totals


@view_config(route_name='order_summary', renderer="../../templates/orders/order_summary.pt")
def view_order_summary(request):
    tilaus_id = request.matchdict['id']
    tilaus = DBSession.query(Tilaus).filter_by(id=tilaus_id).first()

    if len(tilaus.paivaraportit) == 0:
        date_start = None
        date_end = None
    else:
        date_start = sorted(tilaus.paivaraportit, key=lambda raportti: raportti.date)[0].date
        date_end = sorted(tilaus.paivaraportit, key=lambda raportti: raportti.date, reverse=True)[0].date

    luokka1 = get_quantities(tilaus.paivaraportit, 1)
    luokka2 = get_quantities(tilaus.paivaraportit, 2)
    luokka3 = get_quantities(tilaus.paivaraportit, 3)

    hinnat1 = get_totals(tilaus.paivaraportit, 1)
    hinnat2 = get_totals(tilaus.paivaraportit, 2)
    hinnat3 = get_totals(tilaus.paivaraportit, 3)

    total_tavarat = 0.0
    for tavara in tilaus.tavarat:
        total_tavarat += tavara.maara * tavara.hinta

    grand_total = sum(hinnat1.values()) + sum(hinnat2.values()) + sum(hinnat3.values()) + total_tavarat

    return {
            'tilaus': tilaus, 'date_start': date_start, 'date_end': date_end,
            'luokka1': luokka1, 'luokka2': luokka2, 'luokka3': luokka3,
            'hinnat1': hinnat1, 'hinnat2': hinnat2, 'hinnat3': hinnat3,
            'hinta_tavarat': total_tavarat, 'grand_total': grand_total
           }

