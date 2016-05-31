#
# This source code is licensed under the terms of the
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2016
#

import datetime
import json

from tilaushallinta.models import Tilaus, Tilaaja, Kohde


class CustomJSONEncoder(json.JSONEncoder):
    def encode_tilaus(self, obj):
        order = obj
        """:type: tilaushallinta.models.Tilaus"""
        d = {
            'id': order.id,
            'id2': order.date.strftime("%y%m%d-%H%M"),
            'date': order.date,
            'reference': order.viitenumero,
            'tila': order.tila,
            'tilaaja': self.default(order.tilaaja),
            'kohde': self.default(order.kohde)
        }
        return d
    
    def encode_tilaaja(self, obj):
        tilaaja = obj
        """:type: tilaushallinta.models.Tilaaja"""
        d = {
            'nimi': tilaaja.nimi,
            'yritys': tilaaja.yritys,

            'osoite': tilaaja.osoite,
            'postinumero': tilaaja.postinumero,
            'postitoimipaikka': tilaaja.postitoimipaikka
        }
        return d

    def encode_kohde(self, obj):
        kohde = obj
        """:type: tilaushallinta.models.Kohde"""
        d = {
            'nimi': kohde.nimi,
            'yritys': kohde.yritys,

            'osoite': kohde.osoite,
            'postinumero': kohde.postinumero,
            'postitoimipaikka': kohde.postitoimipaikka
        }
        return d

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()

        if isinstance(obj, Tilaus):
            return self.encode_tilaus(obj)
        if isinstance(obj, Tilaaja):
            return self.encode_tilaaja(obj)
        if isinstance(obj, Kohde):
            return self.encode_kohde(obj)

        return json.JSONEncoder.default(self, obj)
