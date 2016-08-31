#
# This source code is licensed under the terms of the
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2016
#

import random
import os

from pyramid.view import view_config

from tilaushallinta.models import DBSession, Tilaaja, Kohde


# Column indexes in CSV file
COMPANY  = 0
NAME     = 1
ADDRESS  = 2
CITY     = 3
PHONE_NO = 4


def anonymize_entity(ent, data):
    """
    Anonymize an entity, either a person or a company
    :param ent: Entity to be anonymized
    :type ent: Tilaaja or Kohde
    :return: None
    """
    if len(ent.nimi):
        ent.nimi = data[NAME]
    if len(ent.yritys):
        ent.yritys = data[COMPANY]
    if len(ent.osoite):
        ent.osoite = data[ADDRESS]
    if len(ent.postitoimipaikka):
        ent.postitoimipaikka = data[CITY]
    if len(ent.puhelin):
        ent.puhelin = data[PHONE_NO]

    if len(ent.email):
        ent.email = ""
    if len(ent.ytunnus):
        ent.ytunnus = ""


@view_config(route_name='admin_anonymize', renderer='../../templates/admin/admin_master.pt')
def view_admin_anonymize(request):
    """
    Replace all sensitive customer data in the database with generic sample data. Useful for converting production data
    to publicly demo-able. Commented out by default as a safety
    """
    """arr = []
    with open("tilaushallinta/views/admin/anon.csv", "r") as data:
        for line in data.readlines():
            arr.append(line.split('|'))

    for tilaaja in DBSession.query(Tilaaja).all():
        data = random.choice(arr)
        anonymize_entity(tilaaja, data)

    for kohde in DBSession.query(Kohde).all():
        data = random.choice(arr)
        anonymize_entity(kohde, data)
        kohde.slaskutus = "" """

    return {}
