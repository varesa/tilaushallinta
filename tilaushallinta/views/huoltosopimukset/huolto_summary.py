#
# This source code is licensed under the terms of the
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2015
#

from pyramid.view import view_config
from models.hintaluokka import LisatoimenpideHintaluokka

from tilaushallinta.models import DBSession, Huolto, Hintaluokka


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


def get_toimenpiteet_total(raportit):
    total = 0.0

    hintaluokat_list = DBSession.query(LisatoimenpideHintaluokka).all()
    hintaluokat_dict = {}
    for hl in hintaluokat_list:
        hintaluokat_dict[hl.hintaluokka] = hl

    for raportti in raportit:
        hintaluokka = hintaluokat_dict[raportti.hintaluokka]
        total += raportti.tunnit * hintaluokka.tunnit
        total += raportti.matkat * hintaluokka.matkat
        total   += raportti.muut * hintaluokka.muut
    return total


@view_config(route_name='huolto_summary', renderer="tilaushallinta.templates:huoltosopimus/huolto_summary.pt")
def view_huolto_summary(request):
    huolto_id = request.matchdict['huolto']
    huolto = DBSession.query(Huolto).filter_by(id=huolto_id).first()

    if len(huolto.huoltoraportit) == 0:
        date_start = None
        date_end = None
    else:
        date_start = sorted(huolto.huoltoraportit, key=lambda raportti: raportti.date)[0].date
        date_end = sorted(huolto.huoltoraportit, key=lambda raportti: raportti.date, reverse=True)[0].date

    """luokka1 = get_quantities(huolto.paivaraportit, 1)
    luokka2 = get_quantities(huolto.paivaraportit, 2)
    luokka3 = get_quantities(huolto.paivaraportit, 3)"""

    toimenpiteet_total = get_toimenpiteet_total(huolto.lisatoimenpiteet)

    """total_tavarat = 0.0
    for tavara in huolto.tavarat:
        total_tavarat += tavara.maara * tavara.hinta

    grand_total = sum(hinnat1.values()) + sum(hinnat2.values()) + sum(hinnat3.values()) + total_tavarat"""

    hintaluokat = DBSession.query(LisatoimenpideHintaluokka).all()
    hl_keyed = {}
    for hl in hintaluokat:
        hl_keyed[hl.hintaluokka] = hl

    return {
            'huolto': huolto, 'date_start': date_start, 'date_end': date_end,
            'hintaluokat': hl_keyed, 'toimenpiteet_total': toimenpiteet_total
            #'luokka1': luokka1, 'luokka2': luokka2, 'luokka3': luokka3,
            #'hinnat1': hinnat1, 'hinnat2': hinnat2, 'hinnat3': hinnat3,
            #'hinta_tavarat': total_tavarat, 'grand_total': grand_total
           }
