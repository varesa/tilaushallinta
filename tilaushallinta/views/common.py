#
# This source code is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014
#

from pyramid.events import subscriber
from pyramid.events import BeforeRender
from pyramid.security import authenticated_userid

from ..models import DBSession, User

@subscriber(BeforeRender)
def add_login_status(event):
    userid = authenticated_userid(event['request'])
    if userid:
        event['session_logged_in'] = True
        event['session_user'] = DBSession.query(User).filter_by(email=userid).first()
    else:
        event['session_logged_in'] = False
        event['session_user'] = None