from pyramid.view import view_config


@view_config(route_name='users_list', request_method='GET', renderer='json')
def list_users(request):
    return request.services.user.get_all()


@view_config(route_name='users_detail', request_method='GET', renderer='json')
def get_user(request):
    user_id = int(request.matchdict['id'])
    return request.services.user.get_by_id(user_id)


@view_config(route_name='users_list', request_method='POST', renderer='json')
def register(request):
    data = request.json_body
    user = request.services.user.create(
        name=data.get('name'),
        email=data.get('email'),
        password=data.get('password')
    )
    request.response.status_code = 201
    return user


@view_config(route_name='users_detail', request_method='PUT', renderer='json')
def update_user(request):
    user_id = int(request.matchdict['id'])
    data = request.json_body
    return request.services.user.update(user_id, data)


@view_config(route_name='users_detail', request_method='DELETE', renderer='json')
def delete_user(request):
    user_id = int(request.matchdict['id'])
    return request.services.user.delete(user_id)


@view_config(route_name='users_login', request_method='POST', renderer='json')
def login(request):
    data = request.json_body
    user = request.services.user.authenticate(
        email=data.get('email'),
        password=data.get('password')
    )
    return {  # JWT WIP (maybe later)
        "message": "Login successful",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role.value
        }
    }
