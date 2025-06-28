
# 🚀 Deploying a Simple App to Kubernetes with Minikube – Part 1: From Zero to Local Cluster
**Published in DevOps & Kubernetes | By Aditya Ranjan**

## 🌱 Introduction
If you're just beginning your Kubernetes journey, Minikube is the perfect place to start. It lets you run a local Kubernetes cluster on your machine—no cloud account or credit card needed.

In this series, I’ll walk you through deploying a simple app to Kubernetes using Minikube. Whether you're a developer trying Kubernetes for the first time or just brushing up, this guide will give you a strong foundation.

## 🧰 What You’ll Need
Before diving in, make sure you have the following:

- 🧑‍💻 A computer with macOS, Linux, or Windows
- ✅ Docker installed and running
- ✅ kubectl installed
- ✅ Minikube installed

You can verify your installations:
```bash
docker --version
kubectl version --client
minikube version
```

## 🔧 Step 1: Start Minikube
Let’s spin up a local Kubernetes cluster using Minikube.

```bash
minikube start
```

Verify it’s working:
```bash
kubectl get nodes
```

## 🌍 Step 2: Create a Simple App

### 2.1 Create the app
Create a folder and add the following files:

**📄 app.py**
```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, Kubernetes!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

**📄 requirements.txt**
```
flask
```

**📄 Dockerfile**
```Dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
```

## 🐳 Step 3: Build the Docker Image

Point Docker to Minikube’s Docker daemon:
```bash
eval $(minikube docker-env)
```

Build the image:
```bash
docker build -t hello-k8s .
```

Verify the image:
```bash
docker images
```

## ☸️ Step 4: Deploy to Kubernetes

### 4.1 Create a Deployment YAML

**📄 deployment.yaml**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: hello
  template:
    metadata:
      labels:
        app: hello
    spec:
      containers:
      - name: hello
        image: hello-k8s:latest
        image: hello-k8s:latest
        ports:
        - containerPort: 5000
```

Apply the deployment:
```bash
kubectl apply -f deployment.yaml
```

Check pods:
```bash
kubectl get pods
```

## 🔌 Step 5: Expose the App with a Service

Expose the deployment:
```bash
kubectl expose deployment hello-deployment --type=NodePort --port=5000
```

Get the service URL:
```bash
minikube service hello-deployment --url
```

Open it in your browser to see:
```
Hello, Kubernetes!
```

## 🎉 Congrats!
You’ve just deployed a containerized app to Kubernetes on your local machine.

## 🧭 What’s Next?
In the next part of this series, we’ll explore:

- Creating ConfigMaps and Secrets
- Adding health checks
- Updating the deployment without downtime
- Using kubectl port-forward and logs

Stay tuned! 🚀
