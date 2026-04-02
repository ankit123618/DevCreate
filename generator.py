import os

def write_file(filename, content):
    with open(filename, "w") as f:
        f.write(content)

def generate_all(project_type):
    os.makedirs(".github/workflows", exist_ok=True)

    if project_type == "node":
        port = "3000"
    elif project_type == "python":
        port = "8000"
    else:
        port = "8080"

    dockerfile = f"""FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt || true
EXPOSE {port}
CMD ["python", "app.py"]
"""

    compose = f"""version: '3'
services:
  app:
    build: .
    ports:
      - "{port}:{port}"
"""

    deployment = f"""apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: app
        image: myapp:latest
        ports:
        - containerPort: {port}
"""

    service = f"""apiVersion: v1
kind: Service
metadata:
  name: app-service
spec:
  type: NodePort
  selector:
    app: myapp
  ports:
    - port: 80
      targetPort: {port}
"""

    github = """name: CI
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build Docker Image
        run: docker build -t myapp .
"""

    write_file("Dockerfile", dockerfile)
    write_file("docker-compose.yml", compose)
    write_file("deployment.yaml", deployment)
    write_file("service.yaml", service)
    write_file(".github/workflows/ci.yml", github)
