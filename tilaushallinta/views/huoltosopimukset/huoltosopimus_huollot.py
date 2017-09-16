#
# This source code is licensed under the terms of the
# s Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2016
#

import datetime
from operator import itemgetter

from pyramid.view import view_config

from tilaushallinta.models import DBSession
from tilaushallinta.models import Huolto
from tilaushallinta.models.huoltosopimus import Huoltosopimus
from tilaushallinta.views.shared.utils import get_closest_date

STATUS_NONE = 0
STATUS_CLOSE = 1
STATUS_LATE = 2

REMINDER_DAYS_BEFORE = 30


def get_status(contract, type):
    """
    Get the next scheduled date for a specific maintenance type
    and whether it is late or not.

    :param contract: Maintenance contract to check the status of
    :type contract: Huoltosopimus
    :param type: Type of the maintenance job to check
    :type type: int
    :return: Status of the maintenance job
    :rtype: int
    """

    if type == Huolto.TYYPPI_KE:
        if not contract.ke_next_date:
            contract.ke_next_date = contract.ke_starting_date

        remind_date = contract.ke_next_date - datetime.timedelta(days=REMINDER_DAYS_BEFORE)

        if datetime.date.today() > remind_date:
            if datetime.date.today() > contract.ke_next_date:
                return STATUS_LATE, contract.ke_next_date
            else:
                return STATUS_CLOSE, contract.ke_next_date
        else:
            return STATUS_NONE, contract.ke_next_date

    if type == Huolto.TYYPPI_SY:
        if not contract.sy_next_date:
            contract.sy_next_date = contract.sy_starting_date

        remind_date = contract.sy_next_date - datetime.timedelta(days=REMINDER_DAYS_BEFORE)

        if datetime.date.today() > remind_date:
            if datetime.date.today() > contract.sy_next_date:
                return STATUS_LATE, contract.sy_next_date
            else:
                return STATUS_CLOSE, contract.sy_next_date
        else:
            return STATUS_NONE, contract.sy_next_date

    if type == Huolto.TYYPPI_TK:
        if not contract.tk_next_date:
            contract.tk_next_date = contract.tk_starting_date

        remind_date = contract.tk_next_date - datetime.timedelta(days=REMINDER_DAYS_BEFORE)

        if datetime.date.today() > remind_date:
            if datetime.date.today() > contract.tk_next_date:
                return STATUS_LATE, contract.tk_next_date
            else:
                return STATUS_CLOSE, contract.tk_next_date
        else:
            return STATUS_NONE, contract.tk_next_date


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

    huollot_tulevat = sorted(huollot_tulevat, key=itemgetter("date"))


    huollot_auki = DBSession.query(Huolto)\
        .filter(Huolto.tila != Huolto.TILA_VALMIS).order_by(Huolto.date.desc()).all()
    huollot_valmiit = DBSession.query(Huolto)\
        .filter(Huolto.tila == Huolto.TILA_VALMIS).order_by(Huolto.date.desc()).all()

    return {"huollot_tulevat": huollot_tulevat, "huollot_auki": huollot_auki, "huollot_valmiit": huollot_valmiit}
