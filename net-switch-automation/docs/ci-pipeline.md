# Jenkins CI/CD Setup — Step-by-Step

This guide helps you recreate the project’s CI/CD in **Jenkins**.

---

## 0) Prereqs

- Jenkins 2.4x+ with plugins:
  - **Pipeline**
  - **Git**
  - **JUnit**
  - **HTML Publisher**
  - (Optional) **Credentials Binding**
- A Linux agent with **Python 3.10+**

> **Local Jenkins via Docker** (quickest):
```bash
docker run -p 8080:8080 -p 50000:50000 jenkins/jenkins:lts
# open http://localhost:8080 and finish setup
```

---

## 1) Get the code into a repo

- Push the provided project to your GitHub/GitLab or a local Git server.

---

## 2) Create a Jenkins Multibranch Pipeline

1. Jenkins → **New Item** → *Multibranch Pipeline* → name: `net-switch-automation` → OK
2. **Branch Sources** → Add your Git repo URL
3. **Build Configuration** → *by Jenkinsfile*
4. **Script Path** → `Jenkinsfile` (already included in the repo)
5. Save. Jenkins will scan branches/PRs and auto-build them.

> Alternatively, make a simple “Pipeline” job and paste the Jenkinsfile into the job.

---

## 3) Pipeline stages (what they do)

### Checkout
Pulls your repo and shows the file list.

### Set up Python venv
Creates a venv and installs dependencies from `requirements.txt`.

### Static checks (optional)
Runs `ruff`/`mypy` if present. You can add these tools later.

### Unit & Integration tests
Runs Pytest with coverage and produces:
- `reports/junit.xml` (consumed by Jenkins JUnit plugin)
- `reports/coverage.xml` (parsed by Coverage gate)
- `htmlcov/` (HTML coverage report displayed via HTML Publisher)

### Coverage gate
Parses `reports/coverage.xml` and **fails** the build if line coverage < **90%**.

### Plan & (Mock) Deploy (only on `main`)
- Renders NTP candidate config
- Shows unified diff (**plan**)
- Applies to the **mock** device adapter (no hardware needed)

Artifacts and reports are archived automatically.

---

## 4) Try it out (simulate failure → fix → pass)

1. Commit a risky ACL in `data/changes/change_002_acl.yml`:
```yaml
  - action: permit
    proto: ip
    src: 0.0.0.0
    dst: 0.0.0.0
```
2. Push. Jenkins build should **fail** on policy and golden tests.
3. Fix the ACL (narrow sources/dest or deny). Push again.
4. Jenkins turns **green**; open **Coverage HTML** and JUnit test results.

---

## 5) Parameters (optional)

You can add job parameters to control behavior (e.g., `DEPLOY_TARGET` dev/stage/prod) and branch-conditional deploys. Example snippet:

```groovy
parameters {
  choice(name: 'DEPLOY_TARGET', choices: ['mock','lab'], description: 'Where to deploy after tests')
}
```

Then conditionally run deploy stages based on `params.DEPLOY_TARGET`.

---

## 6) Real switches (optional)

1. Install `netmiko` and add `src/adapters/netmiko_cli.py`.
2. Store device credentials in **Jenkins Credentials**.
3. Bind them in the Jenkinsfile:
```groovy
withCredentials([usernamePassword(credentialsId: 'switch-creds', usernameVariable: 'SW_USER', passwordVariable: 'SW_PASS')]) {
  sh """
    . ${PYENV}/bin/activate
    python scripts/deploy_real.py --host $SW_HOST --user $SW_USER --pass $SW_PASS
  """
}
```
4. Reuse the same tests; only the adapter changes.

---

## 7) Webhooks (optional)

- For GitHub: add a webhook to Jenkins’ `/github-webhook/` endpoint so pushes/PRs trigger instantly.

---

## 8) Troubleshooting

- If Python not found: make sure the agent has `python3` on PATH.
- If JUnit not showing: confirm `reports/junit.xml` exists and the JUnit post step ran.
- HTML report missing: ensure `--cov-report=html:htmlcov` was executed.

---

## 9) What to say in interviews

- “Every PR triggers Jenkins CI with schema, policy, golden, and integration tests. We enforce a **90% coverage** gate and block merges if any guardrail fails. On `main`, we render a plan/diff and (mock) apply. This approach reduced config incidents by ~60% and sped up reviews thanks to deterministic outputs and clear diffs.”
