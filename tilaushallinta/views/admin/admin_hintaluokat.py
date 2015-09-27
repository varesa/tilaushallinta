#
# This source code is licensed under the terms of the
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2015
#

from pyramid.view import view_config

from tilaushallinta.models import DBSession, Hintaluokka, HuoltoHintaluokka, LisatoimenpideHintaluokka

from tilaushallinta.views.utils import string_to_float_or_zero


@view_config(route_name='admin_hintaluokat', renderer='tilaushallinta.templates:admin/admin_hintaluokat.pt')
def view_admin_hintaluokat(request):
    if "data" in request.POST.keys():
        if request.POST['data'] == "tilaus":
            for i in (1, 2, 3):
                luokka = DBSession.query(Hintaluokka).filter_by(hintaluokka=i).first()
                luokka.tunnit = string_to_float_or_zero(request.POST['tilaus_' + str(i) + '_tunnit'])
                luokka.matkat = string_to_float_or_zero(request.POST['tilaus_' + str(i) + '_matkat'])
                luokka.muut = string_to_float_or_zero(request.POST['tilaus_' + str(i) + '_muut'])
        
        if request.POST['data'] == "huolto":
            for i in (1, 2, 3):
                luokka = DBSession.query(HuoltoHintaluokka).filter_by(hintaluokka=i).first()
                luokka.ek = string_to_float_or_zero(request.POST['huolto_' + str(i) + '_ek'])
                luokka.ke = string_to_float_or_zero(request.POST['huolto_' + str(i) + '_ke'])
                luokka.sy = string_to_float_or_zero(request.POST['huolto_' + str(i) + '_sy'])
                luokka.tk = string_to_float_or_zero(request.POST['huolto_' + str(i) + '_tk'])
                
        if request.POST['data'] == "toimenpide":
            for i in (1, 2, 3):
                luokka = DBSession.query(LisatoimenpideHintaluokka).filter_by(hintaluokka=i).first()
                luokka.tunnit = string_to_float_or_zero(request.POST['toimenpide_' + str(i) + '_tunnit'])
                luokka.matkat = string_to_float_or_zero(request.POST['toimenpide_' + str(i) + '_matkat'])
                luokka.muut = string_to_float_or_zero(request.POST['toimenpide_' + str(i) + '_muut'])

    tilausluokat = DBSession.query(Hintaluokka).all()
    tilausluokat_dict = {}
    for luokka in tilausluokat:
        tilausluokat_dict[luokka.hintaluokka] = luokka

    huoltoluokat = DBSession.query(HuoltoHintaluokka).all()
    huoltoluokat_dict = {}
    for luokka in huoltoluokat:
        huoltoluokat_dict[luokka.hintaluokka] = luokka

    toimenpideluokat = DBSession.query(LisatoimenpideHintaluokka).all()
    toimenpideluokat_dict = {}
    for luokka in toimenpideluokat:
        toimenpideluokat_dict[luokka.hintaluokka] = luokka

    return {
        'tilausluokat': tilausluokat_dict,
        'huoltoluokat': huoltoluokat_dict,
        'toimenpideluokat': toimenpideluokat_dict
    }
