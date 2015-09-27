#
# This source code is licensed under the terms of the
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2015
#

from pyramid.view import view_config

from tilaushallinta.models import DBSession, Huolto, LisatoimenpideHintaluokka


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

    if huolto.tyyppi == huolto.TYYPPI_EK:
        huolto_total = huolto.hintaluokka.ek
    elif huolto.tyyppi == huolto.TYYPPI_KE:
        huolto_total = huolto.hintaluokka.ke
    elif huolto.tyyppi == huolto.TYYPPI_SY:
        huolto_total = huolto.hintaluokka.sy
    elif huolto.tyyppi == huolto.TYYPPI_TK:
        huolto_total = huolto.hintaluokka.tk

    toimenpiteet_total = get_toimenpiteet_total(huolto.lisatoimenpiteet)

    grand_total = huolto_total + toimenpiteet_total

    hintaluokat = DBSession.query(LisatoimenpideHintaluokka).all()
    hl_keyed = {}
    for hl in hintaluokat:
        hl_keyed[hl.hintaluokka] = hl

    return {
        'huolto': huolto, 'date_start': date_start, 'date_end': date_end, 'hintaluokat': hl_keyed,
        'toimenpiteet_total': toimenpiteet_total, 'huolto_total': huolto_total,
        'grand_total': grand_total
        }
