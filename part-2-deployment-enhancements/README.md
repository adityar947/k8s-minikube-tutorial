
# Part 2: Enhancing Your Kubernetes Deployment with Configs, Health Checks & Rolling Updates
**Published in DevOps & Kubernetes | By Aditya Ranjan**

In Part 1, we successfully deployed a simple Flask web app to a local Kubernetes cluster using Minikube. It was a great start—but we barely scratched the surface of what Kubernetes can do.

In this part, we’ll level up by adding configuration management, health checks, and zero-downtime updates. These are best practices that prepare you for real-world deployments.

## ⚙️ Step 6: Add ConfigMap for Environment Variables

Hardcoding values into your app is bad practice. Kubernetes lets you inject config via ConfigMaps.

### 📄 app.py (updated)
```python
import os
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    message = os.getenv("GREETING", "Hello, Kubernetes!")
    return message

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

Rebuild the Docker image (inside Minikube’s Docker daemon):

```bash
eval $(minikube docker-env)
docker build -t hello-k8s:v2 .
```

### 📄 configmap.yaml
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: hello-config
data:
  GREETING: "👋 Hello from a ConfigMap!"
```

Apply it:

```bash
kubectl apply -f configmap.yaml
```

### 📄 deployment.yaml (updated)
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
        image: hello-k8s:v2
        ports:
        - containerPort: 5000
        env:
        - name: GREETING
          valueFrom:
            configMapKeyRef:
              name: hello-config
              key: GREETING
```

Apply the update:

```bash
kubectl apply -f deployment.yaml
kubectl rollout status deployment hello-deployment
```

Check your app:

```bash
minikube service hello-deployment --url
```

You should now see:

```
👋 Hello from a ConfigMap!
```

## ❤️ Step 7: Add Liveness and Readiness Probes

Kubernetes can automatically restart your app if it crashes or becomes unresponsive.

### 📄 deployment.yaml (partial snippet)
```yaml
livenessProbe:
  httpGet:
    path: /
    port: 5000
  initialDelaySeconds: 5
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /
    port: 5000
  initialDelaySeconds: 3
  periodSeconds: 5
```

Apply it again:

```bash
kubectl apply -f deployment.yaml
```

To see probe statuses:

```bash
kubectl describe pod <pod-name>
```

## 🔁 Step 8: Do a Rolling Update

Let’s simulate a new version.

### 📄 app.py (update)
```python
# Return a versioned message
return "👋 Hello from version 3!"
```

Rebuild and tag:

```bash
docker build -t hello-k8s:v3 .
```

Update the image in your deployment YAML:

```yaml
image: hello-k8s:v3
```

Apply it:

```bash
kubectl apply -f deployment.yaml
kubectl rollout status deployment hello-deployment
```

This update happens without downtime—zero interruptions to users.

## 🧼 Cleanup

When you’re done experimenting:

```bash
kubectl delete service hello-deployment
kubectl delete deployment hello-deployment
kubectl delete configmap hello-config
minikube stop
```

## 📦 What’s Next?

In Part 3, we’ll add:

- Ingress with custom domain routing
- TLS/SSL using cert-manager
- Secrets for sensitive data
- Monitoring with Prometheus and Grafana
