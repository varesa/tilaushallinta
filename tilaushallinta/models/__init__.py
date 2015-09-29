#
# This source code is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2015
#

from sqlalchemy.orm import configure_mappers
from sqlalchemy_continuum import make_versioned

from .meta import Base, DBSession


make_versioned()

from .kohde import Kohde
from .vkk import Vesikalustekartoitus, VKK_Asunto, VKK_Huone, VKK_Kaluste
from .tilaaja import Tilaaja
from .tilaus import Tilaus, Tavara, Paivaraportti
from .users import User
from .hintaluokka import Hintaluokka, HuoltoHintaluokka, LisatoimenpideHintaluokka
from .huoltosopimus import Huoltosopimus
from .maintenancejob import MaintenanceJob, MaintenanceReport, Lisatoimenpide
from .laiteluettelo import Laite, Laiteluettelo

configure_mappers()
