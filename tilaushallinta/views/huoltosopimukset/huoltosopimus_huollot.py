#
# This source code is licensed under the terms of the
# s Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2016
#

from pyramid.view import view_config

from tilaushallinta.models import DBSession
from tilaushallinta.models import Huolto
from tilaushallinta.models.huoltosopimus import Huoltosopimus

from tilaushallinta.views.utils import check_next_date_in_30d, get_next_date


@view_config(route_name='huoltosopimus_huollot', renderer='tilaushallinta.templates:huoltosopimus/huolto_list.pt')
def view_huollot_list(request):
    huollot_tulevat = []
    for contract in DBSession.query(Huoltosopimus).all():
        if contract.tyyppi_ke and check_next_date_in_30d(contract.ke_starting_date, 12):
            huollot_tulevat.append({"tyyppi": Huolto.TYYPPI_KE, "date": get_next_date(contract.ke_starting_date, 12),
                                    "contract": contract})
        if contract.tyyppi_sy and check_next_date_in_30d(contract.sy_starting_date, 12):
            huollot_tulevat.append({"tyyppi": Huolto.TYYPPI_SY, "date": get_next_date(contract.sy_starting_date, 12),
                                    "contract": contract})
        if contract.tyyppi_tk and check_next_date_in_30d(contract.tk_starting_date, contract.tk_interval_months):
            huollot_tulevat.append({"tyyppi": Huolto.TYYPPI_TK, "contract": contract,
                                    "date": get_next_date(contract.sy_starting_date, contract.tk_interval_months)})

    huollot_auki = DBSession.query(Huolto).filter(Huolto.tila != Huolto.TILA_VALMIS).order_by(Huolto.date.desc()).all()
    huollot_valmiit = DBSession.query(Huolto).filter(Huolto.tila == Huolto.TILA_VALMIS).order_by(Huolto.date.desc()).all()
    return {"huollot_tulevat": huollot_tulevat, "huollot_auki": huollot_auki, "huollot_valmiit": huollot_valmiit}
