#
# This source code is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014
#

from pyramid.view import view_config

from ..models import DBSession, Hintaluokka

from .utils import string_to_float_or_zero

@view_config(route_name='admin_hintaluokat', renderer='../templates/admin/admin_hintaluokat.pt')
def view_admin_hintaluokat(request):
    if "data" in request.POST.keys():
        for i in (1,2,3):
            luokka = DBSession.query(Hintaluokka).filter_by(hintaluokka=i).first()
            luokka.tunnit = string_to_float_or_zero(request.POST[str(i) + '_tunnit'])
            luokka.matkat = string_to_float_or_zero(request.POST[str(i) + '_matkat'])

    luokat = DBSession.query(Hintaluokka).all()
    luokat_dict = {}
    for luokka in luokat:
        luokat_dict[luokka.hintaluokka] = luokka

    return {'hintaluokat': luokat_dict}