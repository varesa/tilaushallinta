#
# This source code is licensed under the terms of the
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2017
#

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from tilaushallinta.models import DBSession, Huoltosopimus, Huolto


@view_config(route_name='huolto_cancel_reminder')
def view_huolto_cancel_reminder(request):
    contract_id = request.matchdict['contract']
    contract = DBSession.query(Huoltosopimus).filter_by(id=contract_id).first()
    """:type contract: Huoltosopimus"""

    maintenance_type = request.matchdict['type']

    if maintenance_type == Huolto.TYYPPI_muu:
        msg = request.POST['muu_selite']
    else:
        msg = ""

    if maintenance_type == Huolto.TYYPPI_KE:
        contract.advance_date(Huolto.TYYPPI_KE)
    elif maintenance_type == Huolto.TYYPPI_SY:
        contract.advance_date(Huolto.TYYPPI_SY)
    elif maintenance_type == Huolto.TYYPPI_TK:
        contract.advance_date(Huolto.TYYPPI_TK)

    return HTTPFound(location="/huollot")
