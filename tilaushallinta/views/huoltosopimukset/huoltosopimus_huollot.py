#
# This source code is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2015
#


from pyramid.view import view_config

from tilaushallinta.models import DBSession
from tilaushallinta.models import Huolto


@view_config(route_name='huoltosopimus_huollot', renderer='../../templates/huoltosopimus/huolto_list.pt')
def view_huollot_list(request):
    huollot_auki = DBSession.query(Huolto).filter(Huolto.tila != (Huolto.TILA_VALMIS)).order_by(Huolto.date.desc()).all()
    huollot_valmiit = DBSession.query(Huolto).filter(Huolto.tila == (Huolto.TILA_VALMIS)).order_by(Huolto.date.desc()).all()
    return {"huollot_auki": huollot_auki, "huollot_valmiit": huollot_valmiit}