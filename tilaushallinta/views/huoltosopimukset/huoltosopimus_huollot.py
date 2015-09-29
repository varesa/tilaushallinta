#
# This source code is licensed under the terms of the
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2015
#


from pyramid.view import view_config

from tilaushallinta.models import DBSession
from tilaushallinta.models import MaintenanceJob


@view_config(route_name='huoltosopimus_huollot', renderer='tilaushallinta.templates:maintenance_contract/maintenance_job/maintenance_job_list.pt')
def view_huollot_list(request):
    huollot_auki = DBSession.query(MaintenanceJob).filter(MaintenanceJob.tila != (MaintenanceJob.TILA_VALMIS)).order_by(MaintenanceJob.date.desc()).all()
    huollot_valmiit = DBSession.query(MaintenanceJob).filter(MaintenanceJob.tila == (MaintenanceJob.TILA_VALMIS)).order_by(MaintenanceJob.date.desc()).all()
    return {"huollot_auki": huollot_auki, "huollot_valmiit": huollot_valmiit}