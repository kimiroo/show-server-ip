import logging
from typing import TYPE_CHECKING

from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates

from lifespan import lifespan
from util.deps import get_ip_querier

from util.static_files_with_cache import StaticFilesWithCache
from util.schema.ip_response import IpResponse
from util.schema.health_response import HealthResponse
from util.middleware.access_logger import AccessLogger
from util.const import LOG_LEVEL, LOG_LEVEL_INT, DISABLE_IPV6

if TYPE_CHECKING:
    from util.query_public_ip import QueryPublicIp

logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=LOG_LEVEL,
)

log_format = logging.Formatter(
    '%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

log = logging.getLogger('app')
log.setLevel(LOG_LEVEL)

# Handler for console output
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_format)
log.addHandler(console_handler)

# Logger override
for logger_name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
    uvicorn_logger = logging.getLogger(logger_name)
    uvicorn_logger.handlers.clear()
    uvicorn_logger.addHandler(console_handler)

app = FastAPI(
    title='Server Static IP',
    version='2.0.0',
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
    lifespan=lifespan
)

if LOG_LEVEL_INT > logging.WARNING:
    app.add_middleware(AccessLogger)

templates = Jinja2Templates(directory='templates')

app.mount(
    '/static',
    StaticFilesWithCache(directory='static', cache_timeout=31536000),
    name='static'
)

exclude_fields = {"data": {"ipv6": True}} if DISABLE_IPV6 else None

@app.get('/api/v1/server-ip', response_model=IpResponse, response_model_exclude=exclude_fields)
async def get_server_ip(ip_querier: QueryPublicIp = Depends(get_ip_querier)):
    response =await ip_querier.query_public_ip()

    # Remove ipv6 key if ipv6 is disabled
    dump_params = {}
    if DISABLE_IPV6:
        dump_params['exclude'] = {'data': {'ipv6'}}

    return response.model_dump(**dump_params)

@app.get('/api/v1/health', response_model=HealthResponse)
def health():
    return HealthResponse(status='alive')

@app.get('/')
def read_root(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='index.html',
        context={
            'request': request,
            'disable_ipv6': DISABLE_IPV6
        }
    )
