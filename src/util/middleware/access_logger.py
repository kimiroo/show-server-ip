import logging

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

log = logging.getLogger('access_log')

class AccessLogger(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Handle request
        response = await call_next(request)

        client_ip = request.client.host if request.client else '-'
        method = request.method

        path = request.url.path
        if request.url.query:
            path += f'?{request.url.query}'

        status_code = response.status_code
        content_length = response.headers.get('content-length', '-')

        referer = request.headers.get('referer', '-')
        user_agent = request.headers.get('user-agent', '-')

        log.info(
            '%s - "%s %s %s" %s %s "%s" "%s"',
            client_ip, method, path, request.scope.get('http_version', 'HTTP/1.1'),
            status_code, content_length, referer, user_agent
        )

        return response