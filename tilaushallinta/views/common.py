#
# This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Author: Esa Varemo
#

from pyramid.events import subscriber
from pyramid.events import BeforeRender
from pyramid.security import authenticated_userid

from ..models import DBSession, User

@subscriber(BeforeRender)
def add_login_status(event):
    userid = authenticated_userid(event['request'])
    if userid:
        event['logged_in'] = True
        event['user'] = DBSession.query(User).filter_by(email=userid).first()
    else:
        event['logged_in'] = False
        event['user'] = None