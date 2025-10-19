import re

def no_any_any_permit(cfg: str) -> bool:
    """Disallow 'permit ip any any'"""
    return not re.search(r"\bpermit\s+ip\s+any\s+any\b", cfg)

def snmp_is_secure(cfg: str) -> bool:
    """Example weak SNMP string check"""
    return "snmp-server community public" not in cfg
