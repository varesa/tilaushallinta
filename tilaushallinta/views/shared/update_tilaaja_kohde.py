#
# This source code is licensed under the terms of the
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2015
#

from tilaushallinta.models import DBSession, Tilaaja, Kohde


def update_tilaaja(post_data):
    tilaaja_id = post_data['tilaaja_id']
    tilaaja = DBSession.query(Tilaaja).filter_by(id=tilaaja_id).first()

    tilaaja.nimi = post_data['tilaaja_nimi']
    tilaaja.yritys = post_data['tilaaja_yritys']
    tilaaja.ytunnus = post_data['tilaaja_ytunnus']
    tilaaja.osoite = post_data['tilaaja_osoite']
    tilaaja.postitoimipaikka = post_data['tilaaja_postitoimipaikka']
    tilaaja.postinumero = post_data['tilaaja_postinumero']
    tilaaja.puhelin = post_data['tilaaja_puhelin']
    tilaaja.email = post_data['tilaaja_email']


def update_kohde(post_data):
    kohde_id = post_data['kohde_id']
    kohde = DBSession.query(Kohde).filter_by(id=kohde_id).first()

    kohde.nimi = post_data['kohde_nimi']
    kohde.yritys = post_data['kohde_yritys']
    kohde.ytunnus = post_data['kohde_ytunnus']
    kohde.osoite = post_data['kohde_osoite']
    kohde.postitoimipaikka = post_data['kohde_postitoimipaikka']
    kohde.postinumero = post_data['kohde_postinumero']
    kohde.puhelin = post_data['kohde_puhelin']
    kohde.email = post_data['kohde_email']
    kohde.slaskutus = post_data['kohde_slaskutus']
