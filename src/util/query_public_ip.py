import os
import sys
import asyncio
import httpx

from util.schema.ip_response import IpData, IpResponse

class QueryPublicIp:
    def __init__(self):
        debug_str = os.getenv('DEBUG', 'false')
        debug = True if debug_str.lower() == 'true' else False

        self.debug = debug

        self.client = httpx.AsyncClient(timeout=5.0)

    async def query_public_ip(self) -> IpResponse:
        tasks = [
            self._fetch_ip_from_api('https://api4.ipify.org?format=json'),
            self._fetch_ip_from_api('https://api6.ipify.org?format=json')
        ]

        ipv4, ipv6 = await asyncio.gather(*tasks)

        is_success = ipv4 is not None or ipv6 is not None

        return IpResponse(
            result='success' if is_success else 'fail',
            data=IpData(ipv4=ipv4, ipv6=ipv6)
        )

    async def _fetch_ip_from_api(self, api_url: str) -> str | None:
        try:
            response = await self.client.get(api_url, timeout=5.0)
            response.raise_for_status()

            if not response.text:
                return None

            data: dict = response.json()
            return data.get('ip')

        except Exception as e:
            if self.debug:
                print(f'[ERROR] Error fetching ip from \'{api_url}\': {e}', file=sys.stderr)
            return None

    async def close_client(self):
        await self.client.aclose()