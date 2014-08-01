from pyramid.security import Allow, Authenticated, Everyone

class Root(object):
    __acl__ = [
        (Allow, Everyone,       'open'),
        (Allow, Authenticated,  'authenticated'),
        (Allow, 'g:admin',      'admin')
    ]

    def __init__(self, request):
        self.request = request