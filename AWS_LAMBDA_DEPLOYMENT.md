# AWS Lambda Terraform Deployment Guide for Flask URL Shortener

This repository contains infrastructure as code (IaC) written in **Terraform** to automatically provision and deploy the Flask URL Shortener application on **AWS Lambda** using **Amazon ECR** and **Lambda Function URLs**.

---

## Architecture Overview

```
[ Client Request ] ---> [ Lambda Function URL (HTTPS) ] ---> [ AWS Lambda (ARM64 Container) ] ---> [ Flask App ]
```

### Cost Optimization Highlights ($0.00/mo Free Tier)
- **Lambda Function URL**: Direct HTTPS endpoint with **$0 API Gateway fee**.
- **ARM64 Architecture**: Optimized for Apple Silicon builds & **20% lower compute cost**.
- **128 MB Memory**: Maximizes free compute seconds allowance (3.2M seconds/mo).
- **ECR Lifecycle Policy**: Automatically keeps only the 2 latest container images to prevent storage charges.

---

## Prerequisites

1. **Terraform CLI** installed (`terraform -version`).
2. **AWS CLI** installed and configured (`aws configure`).
3. **Docker** daemon running locally.

---

## Deployment Steps with Terraform

### Step 1: Navigate to the `terraform/` directory
```bash
cd terraform
```

### Step 2: Initialize Terraform
```bash
terraform init
```

### Step 3: Review Infrastructure Plan
```bash
terraform plan
```

### Step 4: Apply Infrastructure (Deploys ECR, Container Image, IAM, Lambda, Function URL)
```bash
terraform apply -auto-approve
```

---

## Terraform Outputs

Upon completion, Terraform will output your live HTTPS Function URL:

```text
Outputs:

ecr_repository_url  = "340752803392.dkr.ecr.us-east-1.amazonaws.com/url-shortener"
function_url        = "https://abcdefg12345.lambda-url.us-east-1.on.aws/"
lambda_function_name = "url-shortener-api"
```

---

## Testing the Endpoints

```bash
# Test GET /ping
curl -i https://<YOUR_FUNCTION_URL>/ping

# Test POST /api/v1/urls
curl -i -X POST https://<YOUR_FUNCTION_URL>/api/v1/urls \
  -H "Content-Type: application/json" \
  -d '{"long_url": "https://example.com"}'
```

---

## Destroying Infrastructure

To tear down all created AWS resources:

```bash
cd terraform
terraform destroy -auto-approve
```
