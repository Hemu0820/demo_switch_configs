from src.generators.config_gen import render_ntp_from_file, render_acl_from_file

def test_render_ntp_from_file():
    cfg = render_ntp_from_file("data/changes/change_001_ntp.yml")
    assert "ntp server 1.1.1.1 prefer" in cfg
    assert "ntp server 8.8.8.8" in cfg

def test_render_acl_from_file():
    cfg = render_acl_from_file("data/changes/change_002_acl.yml")
    assert "ip access-list extended APP-POLICY" in cfg
