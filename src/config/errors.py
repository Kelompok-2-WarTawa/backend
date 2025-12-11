from pyramid.httpexceptions import HTTPBadRequest
from src.utils import AppError


def app_error_view(exc, request):
    request.response.status_code = exc.status_code
    payload = {"status": "error",
               "code": exc.status_code, "message": exc.message}
    if getattr(exc, 'details', None):
        payload["details"] = exc.details
    return payload


def bad_request_view(exc, request):
    request.response.status_code = 400
    return {"status": "error", "code": 400, "message": "Invalid JSON/Parameters"}


def generic_error_view(exc, request):
    request.response.status_code = 500
    print(f"CRITICAL: {exc}")
    return {"status": "error", "code": 500, "message": "Internal Server Error"}


def register_error_handlers(config):
    config.add_view(app_error_view, context=AppError, renderer='json')
    config.add_view(bad_request_view, context=HTTPBadRequest, renderer='json')
    # config.add_view(generic_error_view, context=Exception, renderer='json')
