# BMI Health Check — Lambda container demo

FastAPI service that calculates BMI and exposes a `/health` endpoint, packaged as a container image and run on **AWS Lambda** (container image) behind a **Function URL**.

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/health` | Liveness: `{ "status": "ok" }` |
| `GET` | `/bmi?height_cm=175&weight_kg=70` | BMI via query params |
| `POST` | `/bmi` | BMI via JSON body `{ "height_cm", "weight_kg" }` |

Response includes `bmi` (1 decimal) and `category`: `underweight` \| `normal` \| `overweight` \| `obese`.

## Local development

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r app/requirements.txt -r requirements-dev.txt
PYTHONPATH=. pytest -q
uvicorn app.main:app --reload --port 8080
```

Docker (requires Docker daemon):

```bash
docker build -t bmi-health-check .
docker run --rm -p 8080:8080 bmi-health-check
curl -s localhost:8080/health
curl -s 'localhost:8080/bmi?height_cm=175&weight_kg=70'
```

## AWS deploy (us-east-2)

Resources: ECR repo, Lambda (image), Function URL (`NONE` auth for demo), CloudWatch Logs.

### One-time: GitHub Actions OIDC role

Create an IAM role trusted by `token.actions.githubusercontent.com` for `repo:excelcloudOps/bmi-health-check:*`, with permissions to manage ECR, Lambda, IAM pass-role for the Lambda execution role, and CloudWatch Logs.

Set repo secret:

| Secret | Value |
| --- | --- |
| `AWS_IAM_ROLE_ARN` | ARN of the GitHub Actions deploy role |

### CI/CD

Push to `main` (or run **Build and Deploy** manually):

1. Pytest
2. Ensure ECR exists (Terraform target)
3. Build/push image tagged with `github.sha` + `latest`
4. Terraform apply Lambda + Function URL

### Manual bootstrap (CLI)

```bash
cd terraform
terraform init
terraform apply -target=aws_ecr_repository.app -target=aws_ecr_lifecycle_policy.app -auto-approve

ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
REGION=us-east-2
aws ecr get-login-password --region "$REGION" | docker login --username AWS --password-stdin "$ACCOUNT.dkr.ecr.$REGION.amazonaws.com"
docker build -t bmi-health-check .
docker tag bmi-health-check:latest "$ACCOUNT.dkr.ecr.$REGION.amazonaws.com/bmi-health-check:latest"
docker push "$ACCOUNT.dkr.ecr.$REGION.amazonaws.com/bmi-health-check:latest"

terraform apply -var="image_tag=latest" -auto-approve
terraform output function_url
```

## Project layout

```text
app/                 FastAPI app + BMI logic
tests/               unit tests
Dockerfile           Lambda Web Adapter + uvicorn
terraform/           ECR, IAM, Lambda, Function URL
.github/workflows/   test + deploy
```
