#  Production ML API Deployment with Docker & AWS EC2

This repository demonstrates how to **package a Machine Learning API using Docker** and **deploy it to AWS EC2 in production**.

The focus of this project is **production readiness**.

---

##  What This Project Covers

- Dockerizing a FastAPI-based ML inference service
- Creating a **production Dockerfile**
- Building and tagging Docker images
- Pushing images to Docker Hub
- Deploying and running containers on **AWS EC2**
- Exposing the API securely over the internet

---

##  ML Application Overview

The API serves a simple **Linear Regression model** using `scikit-learn`.

- Input: numeric value
- Output: predicted value
- Purpose: demonstrate ML inference in a production environment

The ML logic is intentionally simple so the focus remains on **deployment and infrastructure**.

---

##  Project Structure

```

docker-ml-deployment/
├── app.py
├── requirements.txt
├── Dockerfile
└── README.md
```

---

##  Production Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
```

Why this Dockerfile is production-ready:

No live reload (--reload removed)

Application code copied into the image

Multiple workers for concurrency

Slim base image for smaller size

---

## 🏗️ Build Production Image Locally
```
docker build -t ml-api:prod .
```

##  Test Image Locally (Production Mode)
```
docker run -d --name ml-prod-test -p 8000:8000 ml-api:prod
```

Test:

```
curl http://localhost:8000/
```

Stop test container after verification.

##  Push Image to Docker Hub

```
docker login
docker tag ml-api:prod YOUR_DOCKERHUB_USERNAME/ml-api:v1
docker push YOUR_DOCKERHUB_USERNAME/ml-api:v1
```


This makes the image available for cloud deployment.

##  Deploy to AWS EC2

1️ Launch EC2 Instance

Ubuntu 22.04 LTS

Instance type: t2.medium or t3.micro

Open ports:

SSH (22) – your IP

TCP (8000) – public access

2️ Connect to EC2
```
ssh -i ml-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

3️ Install Docker on EC2
```
sudo apt-get update
sudo apt-get install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ubuntu
```

Re-login after adding user to docker group.

4️ Run the Production Container
```
docker pull YOUR_DOCKERHUB_USERNAME/ml-api:v1

docker run -d \
  --name ml-api-production \
  --restart unless-stopped \
  -p 8000:8000 \
  YOUR_DOCKERHUB_USERNAME/ml-api:v1
```

##  Access Deployed API

Root: http://YOUR_EC2_PUBLIC_IP:8000/

Swagger UI: http://YOUR_EC2_PUBLIC_IP:8000/docs

Prediction endpoint: /predict

Your ML API is now live on the internet 


## 🏁 Summary

This project demonstrates an end-to-end production workflow:

ML API → Docker image → Docker Hub → AWS EC2
