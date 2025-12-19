from pyramid.config import Configurator
from pyramid.renderers import JSON
from pyramid.events import NewRequest
from src.db import get_session_factory, get_tm_session
from src.services import ServiceContainer
from src.utils import json_serializer
from src.config.errors import register_error_handlers
from src.middleware import RateLimitMiddleware
from src.config.settings import app_settings


def add_cors_headers_response_callback(event):
    def cors_headers(request, response):
        frontend_url = app_settings.FRONTEND_URL

        response.headers.update({
            'Access-Control-Allow-Origin': frontend_url,
            'Access-Control-Allow-Methods': 'POST,GET,DELETE,PUT,OPTIONS',
            'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Max-Age': '1728000',
        })
    event.request.add_response_callback(cors_headers)


def init_app(settings=None):
    with Configurator(settings=settings) as config:
        config.include('pyramid_tm')

        config.add_subscriber(add_cors_headers_response_callback, NewRequest)

        config.add_route('cors-options-preflight',
                         '/{catch_all:.*}', request_method='OPTIONS')
        config.add_view(
            lambda r: '',
            route_name='cors-options-preflight',
            renderer='string'
        )

        sf = get_session_factory(config.get_settings())
        config.add_request_method(
            lambda r: get_tm_session(sf, r.tm),
            'dbsession',
            reify=True
        )

        config.add_request_method(
            lambda r: ServiceContainer(r.dbsession),
            'services',
            reify=True
        )

        json_renderer = JSON()
        json_renderer.add_adapter(object, lambda o, r: json_serializer(o))
        config.add_renderer('json', json_renderer)

        register_error_handlers(config)

        config.include('src.routes')
        config.scan('src.views')

        app = config.make_wsgi_app()

    app = RateLimitMiddleware(app)

    return app
