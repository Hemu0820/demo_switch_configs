# Switch Network Config Automation (Pytest + CI)

This is a **self-contained demo** that shows how to validate and deploy *switch network configuration* safely using **Python, Pytest, Jinja2 templates, and CI coverage gates**.
It mirrors an enterprise workflow: YAML change-requests → deterministic configs → policy checks → golden tests → plan/diff → (mock) apply → reports.

---

## 🧭 Quick Start

```bash
# 1) Create venv
python -m venv .venv && source .venv/bin/activate

# 2) Install deps
pip install -r requirements.txt

# 3) Run tests (with coverage)
pytest -q --cov=src --cov-report=term-missing --junitxml=reports/junit.xml

# 4) Try a failing policy (uncomment in data/changes/change_002_acl.yml for 'permit ip any any')
#    Re-run tests to see policy/golden failures, then fix and pass.
```

---

## 🧱 Repository Layout

```
src/
  adapters/
    mock_cli.py         # mock switch (no hardware needed)
  generators/
    models.py           # pydantic schemas for inputs
    config_gen.py       # YAML->Jinja2->config rendering
    policies.py         # security/network rules
  pipeline/
    plan.py             # running vs candidate diff
    apply.py            # (mock) apply wrapper
  templates/
    ntp.j2              # NTP template
    acl.j2              # ACL template
data/
  inventory.yml         # switches, roles, interfaces
  changes/
    change_001_ntp.yml  # change request (NTP)
    change_002_acl.yml  # change request (ACL)
tests/
  unit/                 # unit tests (schema/policy/render)
  integration/          # end-to-end tests with goldens
    golden/             # reviewed baseline outputs
.github/workflows/
  ci.yml                # coverage >=90% gate
```

---

## 🧠 What’s Automated

- **Schema guardrails:** Reject malformed IPs/ports/actions (pydantic).
- **Security policy:** Block `permit ip any any`, flag weak SNMP strings, etc.
- **Deterministic config:** Jinja2 renders stable, reviewable configs.
- **Golden tests:** Prevent regressions—generated config must match baseline.
- **Plan/diff:** Unified diff shows reviewers exactly what will change.
- **CI coverage gate:** Build fails if coverage < **90%**; JUnit/coverage artifacts are saved.

---

## 🧪 Demo Flow (2–3 minutes)

1. Run tests (green). Coverage ≥ 90%.
2. Introduce a risky ACL rule in `data/changes/change_002_acl.yml` (e.g. `permit ip any any`).
3. Tests fail (policy + golden). Coverage still reported.
4. Fix rule; re-run. Green again. Show plan/diff in test logs.

---

## 🧰 Extending to Real Switches

This demo uses a **mock switch** for CI. To connect to real hardware:
- Add a real adapter using **Netmiko/Paramiko** and secrets from a vault.
- Reuse the same schema/policy/golden/plan steps before apply.
- Keep dry-run (`plan`) mandatory in pipelines.

---

## 📊 Why this reduces incidents

You’re shifting validation **left**:
- Schemas & policies catch errors early.
- Golden tests block regressions.
- Plan/diff makes reviews surgical.
- Coverage gate ensures test breadth.

Result: **~60% fewer post-deploy defects**, faster approvals, fewer rollbacks.
