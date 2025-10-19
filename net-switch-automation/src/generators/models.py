from pydantic import BaseModel, IPvAnyAddress, conint, constr
from typing import List, Optional

class NTPChange(BaseModel):
    device: str
    servers: List[IPvAnyAddress]
    prefer: Optional[IPvAnyAddress] = None

class ACLRule(BaseModel):
    action: constr(regex=r"^(permit|deny)$")
    src: IPvAnyAddress
    dst: IPvAnyAddress
    proto: constr(regex=r"^(tcp|udp|icmp|ip)$")
    dport: Optional[conint(ge=1, le=65535)] = None
