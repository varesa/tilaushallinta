from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from datetime import date, timedelta

from tilaushallinta.models import DBSession, Huolto, Huoltosopimus


NORMALIZE_THRESHOLD = 200


@view_config(route_name='admin_normalize_reminders')
def view_admin_normalize_reminders(request):
    contracts = DBSession.query(Huoltosopimus).all()

    for contract in contracts:
        """:type contract: Huoltosopimus"""

        print(contract)

        if contract.tyyppi_ke:
            while date.today() - contract.ke_next_date > timedelta(days=NORMALIZE_THRESHOLD):
                contract.advance_date(Huolto.TYYPPI_KE)

        if contract.tyyppi_sy:
            while date.today() - contract.sy_next_date > timedelta(days=NORMALIZE_THRESHOLD):
                contract.advance_date(Huolto.TYYPPI_SY)

        if contract.tyyppi_tk:
            while date.today() - contract.tk_next_date > timedelta(days=NORMALIZE_THRESHOLD):
                contract.advance_date(Huolto.TYYPPI_TK)

    return HTTPFound('/huollot')
