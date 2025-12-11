from pyramid.config import Configurator
from pyramid.renderers import JSON

from src.db import get_session_factory, get_tm_session
from src.services import ServiceContainer
from src.utils import json_serializer
from src.config.errors import register_error_handlers


def init_app(settings=None):

    with Configurator(settings=settings) as config:
        config.include('pyramid_tm')

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

        return config.make_wsgi_app()
