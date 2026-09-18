---
description: Steps to deploy Flask URL Shortener app to AWS Lambda using Container Images and ECR
---

# Deploy Flask URL Shortener to AWS Lambda

This workflow describes how to package and deploy the Flask URL Shortener application to AWS Lambda using container images (Amazon ECR) and API Gateway.

## Prerequisites

1. **AWS CLI** installed and configured (`aws configure`).
2. **Docker** running locally.
3. AWS IAM permissions for ECR, Lambda, and API Gateway.

---

## Step 1: Adapt Dockerfile for AWS Lambda Web Adapter

AWS Lambda Web Adapter enables running standard HTTP web applications (like Flask with Gunicorn) on AWS Lambda without code changes.

Create `Dockerfile.lambda` (or update `Dockerfile`):

```dockerfile
FROM public.ecr.aws/docker/library/python:3.12-slim
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.8.4 /lambda-adapter /opt/extensions/lambda-adapter

ENV PORT=5001 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5001
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers", "1", "app:app"]
```

---

## Step 2: Create Amazon ECR Repository

```bash
aws ecr create-repository \
  --repository-name url-shortener \
  --region us-east-1
```

---

## Step 3: Build, Tag, and Push Docker Image to ECR

Replace `<AWS_ACCOUNT_ID>` and `<REGION>` with your AWS Account ID and region (e.g. `us-east-1`):

```bash
# 1. Authenticate Docker with ECR
aws ecr get-login-password --region <REGION> | docker login --username AWS --password-stdin <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com

# 2. Build image
docker build -f Dockerfile.lambda -t url-shortener-lambda .

# 3. Tag image for ECR
docker tag url-shortener-lambda:latest <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/url-shortener:latest

# 4. Push image to ECR
docker push <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/url-shortener:latest
```

---

## Step 4: Create AWS Lambda Function

1. Open **AWS Lambda Console** -> **Create function**.
2. Select **Container image**.
3. Function name: `url-shortener-api`.
4. Container image URI: Select `<AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/url-shortener:latest`.
5. Click **Create function**.

---

## Step 5: Configure API Gateway Trigger

1. In the Lambda function page, click **Add trigger**.
2. Select **API Gateway**.
3. Choose **Create an API** -> **HTTP API**.
4. Security: **Open** (or configure JWT/IAM as required).
5. Click **Add**.

---

## Step 6: Test the Lambda Endpoint

Once API Gateway is created, copy the API endpoint URL (e.g., `https://<api-id>.execute-api.<region>.amazonaws.com`):

```bash
# Ping endpoint
curl https://<api-id>.execute-api.<region>.amazonaws.com/ping

# Create short URL endpoint
curl -X POST https://<api-id>.execute-api.<region>.amazonaws.com/api/v1/urls \
  -H "Content-Type: application/json" \
  -d '{"long_url": "https://example.com"}'
```
