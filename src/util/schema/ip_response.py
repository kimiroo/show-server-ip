from typing import Literal, Optional
from pydantic import BaseModel

class IpData(BaseModel):
    ipv4: Optional[str] = None
    ipv6: Optional[str] = None

class IpResponse(BaseModel):
    result: Literal['success', 'fail']
    data: IpData