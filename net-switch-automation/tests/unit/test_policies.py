from src.generators.policies import no_any_any_permit, snmp_is_secure

def test_policy_blocks_any_any():
    cfg = """ip access-list extended APP-POLICY
 permit ip any any
"""
    assert no_any_any_permit(cfg) is False

def test_snmp_not_public():
    cfg = "snmp-server community private RO\n"
    assert snmp_is_secure(cfg) is True
