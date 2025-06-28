
# Part 4: Monitoring Your Kubernetes App with Prometheus & Grafana in Minikube
**Published in DevOps & Kubernetes | By Aditya Ranjan**

In previous parts, we deployed a secure, configurable app in Kubernetes using Minikube. But no app is truly production-ready without proper monitoring.

In this part, we’ll explore:

- Deploying Prometheus and Grafana using the Kubernetes community Helm charts
- Visualizing resource usage (CPU, memory, etc.)
- Setting up basic app metrics and a dashboard

Let’s get started.

## 🔧 Step 15: Install Helm (If You Haven’t Already)

Helm is the package manager for Kubernetes.

Install Helm:

```bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

Verify it:

```bash
helm version
```

## 📦 Step 16: Add Prometheus and Grafana Helm Repos

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```

## 📈 Step 17: Install Prometheus Stack

Install Prometheus (which includes Grafana) in a dedicated namespace:

```bash
kubectl create namespace monitoring
helm install kube-prometheus-stack prometheus-community/kube-prometheus-stack --namespace monitoring
```

This installs:

- Prometheus
- Alertmanager
- Node Exporters
- Grafana (pre-configured!)

## 🌐 Step 18: Access Grafana Dashboard

Since we’re on Minikube, use port-forwarding:

```bash
kubectl port-forward -n monitoring svc/kube-prometheus-stack-grafana 3000:80
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

🔐 **Default login**:
- Username: `admin`
- Password: `prom-operator`

Change the password after login.

## 📋 Step 19: View Node and Pod Metrics

Grafana is already set up with default dashboards. From the left menu:

- Go to **Dashboards → Manage**
- Open:
  - Kubernetes / Compute Resources / Pod
  - Kubernetes / Networking / Pod Networking

You’ll see real-time resource metrics for your app pods!

## 📊 Step 20: Expose Custom Metrics from Flask

Install `prometheus_client`:

```bash
pip install prometheus_client
```

Update your `app.py`:

```python
from flask import Flask
from prometheus_client import Counter, generate_latest
import os

app = Flask(__name__)

GREETING = os.getenv("GREETING", "Hello, Kubernetes!")
visits = Counter('hello_requests_total', 'Total Hello Requests')

@app.route('/')
def hello():
    visits.inc()
    return GREETING

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': 'text/plain'}
```

Rebuild the image:

```bash
docker build -t hello-k8s:metrics .
```

Update the deployment image in `deployment.yaml`:

```yaml
image: hello-k8s:metrics
```

Re-apply your deployment.

## 📡 Step 21: Configure Prometheus to Scrape Flask Metrics

Add annotations to your pod spec in `deployment.yaml`:

```yaml
annotations:
  prometheus.io/scrape: "true"
  prometheus.io/path: "/metrics"
  prometheus.io/port: "5000"
```

Re-apply and confirm your app is being scraped:

```bash
kubectl get endpoints
```

Then in Grafana:

- Add a new dashboard
- Use Prometheus query:
```promql
hello_requests_total
```

Visualize how many times your app has been hit!

## 🧼 Cleanup

If you want to remove the monitoring stack:

```bash
helm uninstall kube-prometheus-stack -n monitoring
kubectl delete namespace monitoring
```

## ✅ Summary

You now have a fully observable app on Kubernetes:

✅ Prometheus scrapes resource and app metrics  
✅ Grafana visualizes everything  
✅ Flask exposes custom metrics  
✅ Zero cloud resources used — all local!

## 🧭 Coming Up in Part 5

In the final part of this series, we’ll wrap it all up with:

- Kubernetes best practices checklist
- CI/CD pipeline for automatic deploys
- Tips for going from local (Minikube) to cloud (GKE, EKS, AKS)
