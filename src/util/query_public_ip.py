import logging
import asyncio
import httpx

from util.schema.ip_response import IpData, IpResponse
from util.const import DISABLE_IPV6

log = logging.getLogger('query_public_ip')

class QueryPublicIp:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=5.0)

    async def query_public_ip(self) -> IpResponse:
        tasks = [self._fetch_ip_from_api('https://api4.ipify.org?format=json')]

        if not DISABLE_IPV6:
            tasks.append(self._fetch_ip_from_api('https://api6.ipify.org?format=json'))

        results = await asyncio.gather(*tasks)

        ipv4 = results[0]
        ipv6 = results[1] if not DISABLE_IPV6 else None
        is_success = any(res is not None for res in results)

        if not is_success:
            log.warning('Failed to fetch both IPv4 and IPv6 addresses.')

        return IpResponse(
            result='success' if is_success else 'fail',
            data=IpData(ipv4=ipv4, ipv6=ipv6)
        )

    async def _fetch_ip_from_api(self, api_url: str) -> str | None:
        try:
            response = await self.client.get(api_url, timeout=5.0)
            response.raise_for_status()

            if not response.text:
                log.warning('Empty response from %s', api_url)
                return None

            data: dict = response.json()
            ip = data.get('ip')

            log.debug('Successfully fetched IP %s from %s', ip, api_url)

            return ip

        except Exception as e:
            log.warning('Error fetching ip from \'%s\': %s', api_url, e)
            return None

    async def close_client(self):
        await self.client.aclose()