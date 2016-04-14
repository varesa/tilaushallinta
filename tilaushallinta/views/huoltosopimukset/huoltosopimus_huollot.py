#
# This source code is licensed under the terms of the
# s Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2016
#

import datetime

from pyramid.view import view_config

from tilaushallinta.models import DBSession
from tilaushallinta.models import Huolto
from tilaushallinta.models.huoltosopimus import Huoltosopimus

from tilaushallinta.views.utils import check_next_date_in_30d, get_next_date, get_closest_date

STATUS_NONE = 0
STATUS_CLOSE = 1
STATUS_LATE = 2


def get_status(contract, type):
    if type == Huolto.TYYPPI_KE:
        starting_date = contract.ke_starting_date
        interval = 12
    if type == Huolto.TYYPPI_SY:
        starting_date = contract.sy_starting_date
        interval = 12
    if type == Huolto.TYYPPI_TK:
        starting_date = contract.tk_starting_date
        interval = contract.tk_interval_months

    closest = get_closest_date(starting_date, interval)
    now = datetime.date.today()

    for maintenance in contract.huollot:
        if abs((maintenance.date - datetime.datetime.now()).days) < (30 * interval / 2):
            return STATUS_NONE, closest  # Already completed, no action required

    distance = (closest - now).days
    if distance < 0:
        return STATUS_LATE, closest

    if distance < 30:
        return STATUS_CLOSE, closest
    else:
        return STATUS_NONE, closest


@view_config(route_name='huoltosopimus_huollot', renderer='tilaushallinta.templates:huoltosopimus/huolto_list.pt')
def view_huollot_list(request):
    huollot_tulevat = []

    for contract in DBSession.query(Huoltosopimus).all():
        if contract.tyyppi_ke:
            status, date = get_status(contract, Huolto.TYYPPI_KE)
            if status == STATUS_CLOSE:
                huollot_tulevat.append({"tyyppi": Huolto.TYYPPI_KE, "date": date, "late": False,
                                        "contract": contract})
            elif status == STATUS_LATE:
                huollot_tulevat.append({"tyyppi": Huolto.TYYPPI_KE, "date": date, "late": True,
                                        "contract": contract})
        if contract.tyyppi_sy:
            status, date = get_status(contract, Huolto.TYYPPI_SY)
            if status == STATUS_CLOSE:
                huollot_tulevat.append({"tyyppi": Huolto.TYYPPI_SY, "date": date, "late": False,
                                        "contract": contract})
            elif status == STATUS_LATE:
                huollot_tulevat.append({"tyyppi": Huolto.TYYPPI_SY, "date": date, "late": True,
                                        "contract": contract})
        if contract.tyyppi_tk:
            status, date = get_status(contract, Huolto.TYYPPI_TK)
            if status == STATUS_CLOSE:
                huollot_tulevat.append({"tyyppi": Huolto.TYYPPI_TK, "date": date, "late": False,
                                        "contract": contract})
            elif status == STATUS_LATE:
                huollot_tulevat.append({"tyyppi": Huolto.TYYPPI_TK, "date": date, "late": True,
                                        "contract": contract})

    huollot_auki = DBSession.query(Huolto)\
        .filter(Huolto.tila != Huolto.TILA_VALMIS).order_by(Huolto.date.desc()).all()
    huollot_valmiit = DBSession.query(Huolto)\
        .filter(Huolto.tila == Huolto.TILA_VALMIS).order_by(Huolto.date.desc()).all()

    return {"huollot_tulevat": huollot_tulevat, "huollot_auki": huollot_auki, "huollot_valmiit": huollot_valmiit}
