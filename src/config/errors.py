from pyramid.httpexceptions import HTTPBadRequest
from pydantic import ValidationError as PydanticValidationError
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


def pydantic_error_view(exc, request):
    request.response.status_code = 400
    errors = []
    for e in exc.errors():
        errors.append(f"{e['loc'][-1]}: {e['msg']}")

    return {
        "status": "error",
        "code": 400,
        "message": "Validation Failed",
        "details": errors
    }


def register_error_handlers(config):
    config.add_view(app_error_view, context=AppError, renderer='json')
    config.add_view(bad_request_view, context=HTTPBadRequest, renderer='json')
    config.add_view(pydantic_error_view,
                    context=PydanticValidationError, renderer='json')
    config.add_view(generic_error_view, context=Exception, renderer='json')
