from pyramid.view import view_config

from ..models import DBSession, User

@view_config(route_name='admin', renderer='../templates/admin.pt')
def view_admin(request):
    return {}

@view_config(route_name='admin_users', renderer='../templates/admin_users.pt')
def view_admin_users(request):
    users = DBSession.query(User).order_by(User.uuid.desc()).all()

    latest = []
    lastid = None

    for user in users:
        if user.id is not lastid:
            latest.append(user)
            lastid = user.id
    latest.reverse()
    return {'users': latest}
