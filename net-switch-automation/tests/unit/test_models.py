import pytest
from src.generators.models import NTPChange, ACLRule

def test_ntp_schema_valid():
    c = NTPChange(device="sw01", servers=["1.1.1.1", "8.8.8.8"], prefer="1.1.1.1")
    assert str(c.prefer) in [str(s) for s in c.servers]

def test_ntp_schema_invalid_ip():
    with pytest.raises(Exception):
        NTPChange(device="sw01", servers=["bad.ip"])  # invalid

def test_acl_schema_valid():
    rule = ACLRule(action="permit", proto="tcp", src="10.0.0.0", dst="10.1.0.0", dport=443)
    assert rule.dport == 443
