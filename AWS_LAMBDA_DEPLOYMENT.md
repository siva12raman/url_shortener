# AWS Lambda Deployment Guide for Flask URL Shortener

This document outlines the step-by-step process to deploy the Flask URL Shortener application to AWS Lambda using Amazon ECR (Elastic Container Registry) and Amazon API Gateway.

---

## Architecture Overview

```
[ Client Request ] ---> [ Amazon API Gateway ] ---> [ AWS Lambda (Docker Container) ] ---> [ Flask App ]
```

---

## Prerequisites

- [AWS CLI](https://aws.amazon.com/cli/) installed and configured (`aws configure`).
- [Docker](https://www.docker.com/) running locally.
- AWS account permissions for ECR, Lambda, and API Gateway.

---

## Step 1: Create Dockerfile for AWS Lambda

AWS Lambda Web Adapter allows running standard WSGI/HTTP web applications inside Lambda without modifying application code.

Create a file named `Dockerfile.lambda`:

```dockerfile
FROM public.ecr.aws/docker/library/python:3.12-slim

# Include AWS Lambda Web Adapter extension
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

## Step 2: Create ECR Repository & Push Image

Set your target AWS Region and Account ID:
```bash
export AWS_REGION="us-east-1"
export AWS_ACCOUNT_ID="$(aws sts get-caller-identity --query Account --output text)"
```

### 1. Create ECR Repository
```bash
aws ecr create-repository \
  --repository-name url-shortener \
  --region ${AWS_REGION}
```

### 2. Login to ECR
```bash
aws ecr get-login-password --region ${AWS_REGION} | \
  docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
```

### 3. Build & Tag Container Image
```bash
docker build -f Dockerfile.lambda -t url-shortener-lambda .
docker tag url-shortener-lambda:latest ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/url-shortener:latest
```

### 4. Push Image to ECR
```bash
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/url-shortener:latest
```

---

## Step 3: Create Lambda Function & API Gateway Trigger

### Using AWS CLI:

```bash
# 1. Create IAM Role for Lambda
aws iam create-role \
  --role-name url-shortener-lambda-role \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"Service": "lambda.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }]
  }'

# 2. Attach execution and ECR read policies to the role
aws iam attach-role-policy \
  --role-name url-shortener-lambda-role \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

aws iam attach-role-policy \
  --role-name url-shortener-lambda-role \
  --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly

# 3. Create Lambda Function
aws lambda create-function \
  --function-name url-shortener-api \
  --package-type Image \
  --code ImageUri=${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/url-shortener:latest \
  --role arn:aws:iam::${AWS_ACCOUNT_ID}:role/url-shortener-lambda-role \
  --timeout 15 \
  --memory-size 512
```

---

## Step 4: Verify Deployment

Once API Gateway is configured as the trigger, test your endpoints:

```bash
# Test GET /ping
curl -i https://<YOUR_API_GATEWAY_ENDPOINT>/ping

# Test POST /api/v1/urls
curl -i -X POST https://<YOUR_API_GATEWAY_ENDPOINT>/api/v1/urls \
  -H "Content-Type: application/json" \
  -d '{"long_url": "https://example.com"}'
```
