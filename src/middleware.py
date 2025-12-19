import time
from pyramid.httpexceptions import HTTPTooManyRequests


class RateLimitMiddleware:
    def __init__(self, app):
        self.app = app
        self.requests = {}
        self.LIMIT = 100
        self.WINDOW = 60

    def __call__(self, environ, start_response):
        x_forwarded = environ.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded:
            ip = x_forwarded.split(',')[0].strip()
        else:
            ip = environ.get('REMOTE_ADDR')

        now = time.time()

        if ip not in self.requests:
            self.requests[ip] = []

        self.requests[ip] = [
            t for t in self.requests[ip] if now - t < self.WINDOW]

        if len(self.requests[ip]) >= self.LIMIT:
            res = HTTPTooManyRequests(
                json={"error": "Too many requests. Chill out."})
            return res(environ, start_response)

        self.requests[ip].append(now)

        return self.app(environ, start_response)
