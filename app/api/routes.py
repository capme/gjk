from app.api.resources.attack import Attack, Attacks


def init_routes(api):
    """routes"""
    api.add_resource(Attacks, '/attacks')
    api.add_resource(Attack, '/attack/', '/attack/<int:_id>')
