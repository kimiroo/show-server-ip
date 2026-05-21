from util.query_public_ip import QueryPublicIp

_ip_querier = QueryPublicIp()

def get_ip_querier() -> QueryPublicIp:
    return _ip_querier

async def close_ip_querier():
    await _ip_querier.close_client()
