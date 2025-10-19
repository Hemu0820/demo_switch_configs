from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import yaml
from .models import NTPChange, ACLRule

env = Environment(loader=FileSystemLoader("src/templates"), trim_blocks=True, lstrip_blocks=True)

def load_yaml(path: str):
    return yaml.safe_load(Path(path).read_text())

def render_ntp_from_file(path: str) -> str:
    data = load_yaml(path)
    change = NTPChange(**data)
    tpl = env.get_template("ntp.j2")
    return tpl.render(servers=[str(s) for s in change.servers], prefer=str(change.prefer) if change.prefer else None)

def render_acl_from_file(path: str) -> str:
    data = load_yaml(path)
    rules = [ACLRule(**r) for r in data.get("rules", [])]
    tpl = env.get_template("acl.j2")
    return tpl.render(rules=[r.model_dump() for r in rules])
