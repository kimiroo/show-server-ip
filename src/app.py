from typing import TYPE_CHECKING

from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates

from lifespan import lifespan
from util.deps import get_ip_querier

from util.static_files_with_cache import StaticFilesWithCache
from util.schema.ip_response import IpResponse
from util.schema.health_response import HealthResponse

if TYPE_CHECKING:
    from util.query_public_ip import QueryPublicIp

app = FastAPI(
    title='Server Static IP',
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
    lifespan=lifespan
)

templates = Jinja2Templates(directory='templates')

app.mount(
    '/static',
    StaticFilesWithCache(directory='static', cache_timeout=31536000),
    name='static'
)

@app.get('/api/v1/server-ip', response_model=IpResponse)
async def get_server_ip(ip_querier: QueryPublicIp = Depends(get_ip_querier)):
    return await ip_querier.query_public_ip()

@app.get('/api/v1/health', response_model=HealthResponse)
def health():
    return HealthResponse(status='alive')

@app.get('/')
def read_root(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})
