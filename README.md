# BMI Health Check — Lambda container demo

FastAPI BMI calculator packaged as a container image and deployed to **AWS Lambda** (container image) behind a **Function URL**.

**All build, scan, push, and deploy steps run in GitHub Actions.** There is no local deploy path.

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/health` | Liveness: `{ "status": "ok" }` |
| `GET` | `/bmi?height_cm=175&weight_kg=70` | BMI via query params |
| `POST` | `/bmi` | BMI via JSON body `{ "height_cm", "weight_kg" }` |

Response includes `bmi` (1 decimal) and `category`: `underweight` \| `normal` \| `overweight` \| `obese`.

## CI/CD (fully automated)

Trigger: push to `main` or **Actions → Build and Deploy → Run workflow**.

Pipeline:

1. **Unit tests** (pytest)
2. **Ensure ECR** exists (Terraform)
3. **Build** Docker image (Buildx)
4. **Scan** image with Trivy (fail on CRITICAL/HIGH)
5. **Push** image to ECR (`:sha` + `:latest`)
6. **Deploy** Lambda via Terraform
7. **Smoke test** `/health` and `/bmi` against the Function URL

### Required secret

| Secret | Value |
| --- | --- |
| `AWS_IAM_ROLE_ARN` | `arn:aws:iam::319029038820:role/github-actions-bmi-health-check` |

OIDC trust must allow GitHub’s `repo:org@id/repo@id:...` subject format (already configured).

### Live URL

```text
https://ccgykghnzvmolqnqqg3io6ljdm0dgotw.lambda-url.us-east-2.on.aws/
```

```bash
curl -sS https://ccgykghnzvmolqnqqg3io6ljdm0dgotw.lambda-url.us-east-2.on.aws/health
curl -sS 'https://ccgykghnzvmolqnqqg3io6ljdm0dgotw.lambda-url.us-east-2.on.aws/bmi?height_cm=175&weight_kg=70'
```

## Local development only (optional)

App/tests only — not used for deploy:

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r app/requirements.txt -r requirements-dev.txt
PYTHONPATH=. pytest -q
uvicorn app.main:app --reload --port 8080
```

## Project layout

```text
app/                 FastAPI app + BMI logic
tests/               unit tests
Dockerfile           Lambda Web Adapter + uvicorn
terraform/           ECR, IAM, Lambda, Function URL
.github/workflows/   test → build → scan → push → deploy
infra/               GitHub OIDC IAM policy docs
```
