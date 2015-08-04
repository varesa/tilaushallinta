#
# This source code is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2015
#


from pyramid.view import view_config

from tilaushallinta.models import DBSession
from tilaushallinta.models import Tilaus


@view_config(route_name='order_list', renderer='../../templates/orders/order_list.pt')
def view_tilaukset_list(request):
    #tilaukset = DBSession.query(Tilaus).order_by(Tilaus.date.desc()).all()
    tilaukset_auki = DBSession.query(Tilaus).filter(Tilaus.tila != (Tilaus.TILA_VALMIS)).order_by(Tilaus.date.desc()).all()
    tilaukset_valmiit = DBSession.query(Tilaus).filter(Tilaus.tila == (Tilaus.TILA_VALMIS)).order_by(Tilaus.date.desc()).all()
    return {"tilaukset_auki": tilaukset_auki, "tilaukset_valmiit": tilaukset_valmiit}