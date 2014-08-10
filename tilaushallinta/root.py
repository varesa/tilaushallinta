#
# This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Author: Esa Varemo
#

from pyramid.security import Allow, Authenticated, Everyone

class Root(object):
    __acl__ = [
        (Allow, Everyone,       'open'),
        (Allow, Authenticated,  'authenticated'),
        (Allow, 'g:admin',      'admin')
    ]

    def __init__(self, request):
        self.request = request