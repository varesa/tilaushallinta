#
# This source code is licensed under the terms of the
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2015
#

import datetime

from pyramid.view import view_config

from tilaushallinta.models import DBSession
from tilaushallinta.models import Huolto
from tilaushallinta.views.huoltosopimukset.huolto_details_laitteet import save_laitteet
from tilaushallinta.views.huoltosopimukset.huolto_details_raportit import add_huoltoraportti, save_huoltoraportit
from tilaushallinta.views.huoltosopimukset.huolto_details_toimenpiteet import add_lisatoimenpide, save_lisatoimenpiteet


def compare_sets(sets):
    difference = False
    for val1, val2 in sets:
        if val1 != val2:
            difference = True
    return difference


@view_config(route_name='huolto_details', renderer='tilaushallinta.templates:maintenance_contract/maintenance_job/maintenance_job_details.pt')
def view_huolto_details(request):
    huolto_id = request.matchdict['huolto']
    huolto = DBSession.query(Huolto).filter_by(id=huolto_id).first()

    if 'data' in request.POST.keys():
        ###########################################
        # Form data sent for updating daily reports
        ###########################################

        if request.POST['data'] == 'huoltoraportti':
            if 'save' in request.POST.keys():
                save_huoltoraportit(request, huolto)
            elif 'add' in request.POST.keys():
                add_huoltoraportti(huolto)

        ###########################################
        # Form data sent for updating Lisatoimenpiteet
        ###########################################

        if request.POST['data'] == 'lisatoimenpiteet':
            if 'save' in request.POST.keys():
                save_lisatoimenpiteet(request, huolto)
            elif 'add' in request.POST.keys():
                add_lisatoimenpide(huolto)

        ############################################
        # Form data sent for updating the items list
        ############################################

        if request.POST['data'] == 'laitteet':
            save_laitteet(request, huolto)

    current_date = datetime.datetime.now()

    return {'huolto': huolto, 'current_date': current_date}
