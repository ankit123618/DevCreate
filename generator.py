import os

def write_file(filename, content):
    os.makedirs(os.path.dirname(filename), exist_ok=True) if "/" in filename else None
    with open(filename, "w") as f:
        f.write(content)

def generate_all(project_type):
    port = "8080"

    if project_type == "node":
        port = "3000"
        base = "node:18"
        run_cmd = '["npm","start"]'
    elif project_type == "python":
        port = "8000"
        base = "python:3.10-slim"
        run_cmd = '["python","app.py"]'
    elif project_type == "java":
        base = "openjdk:17"
        run_cmd = '["java","-jar","app.jar"]'
    elif project_type in ["c","cpp"]:
        base = "gcc:latest"
        run_cmd = '["./app"]'
    else:
        base = "alpine"
        run_cmd = '["sh"]'

    dockerfile = f"""FROM {base}
WORKDIR /app
COPY . .
RUN if [ -f requirements.txt ]; then pip install -r requirements.txt; fi || true
RUN if [ -f package.json ]; then npm install; fi || true
RUN if ls *.c 1> /dev/null 2>&1; then gcc *.c -o app; fi || true
RUN if ls *.cpp 1> /dev/null 2>&1; then g++ *.cpp -o app; fi || true
EXPOSE {port}
CMD {run_cmd}
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
