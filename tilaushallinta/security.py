#
# This source code is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014
#

from .models import DBSession, User


def get_user_groups(userid, request):
    user = DBSession.query(User).filter_by(email=userid).first()
    if user:
        groups = []
        if user.admin:
            groups.append('group:admin')
        return groups