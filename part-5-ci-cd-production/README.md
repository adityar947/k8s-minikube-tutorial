# 🚀 Part 5: From Local to Production — Kubernetes Best Practices & CI/CD with Minikube

![GitHub Actions](https://img.shields.io/github/actions/workflow/status/yourusername/k8s-minikube-tutorial/ci.yml)
![License](https://img.shields.io/github/license/yourusername/k8s-minikube-tutorial)
![GitHub Repo stars](https://img.shields.io/github/stars/yourusername/k8s-minikube-tutorial?style=social)

Published in DevOps & Kubernetes | By [Your Name]

---

We’ve come a long way:

✅ Deployed a Flask app on Kubernetes (Minikube)  
✅ Used ConfigMaps, Secrets, Ingress, TLS  
✅ Integrated Prometheus & Grafana for observability  

Now, let’s bridge the gap between local experimentation and real-world production by covering:

- Kubernetes deployment best practices  
- CI/CD pipeline using GitHub Actions  
- How to migrate from Minikube to the cloud  

---

## ✅ Step 22: Kubernetes Deployment Best Practices Checklist

### 🔐 1. Use Secrets (never hardcoded secrets)
- Store sensitive values (API keys, DB passwords) in Kubernetes Secrets
- Avoid checking secrets into Git

### 🛡️ 2. Resource Requests and Limits
```yaml
resources:
  requests:
    cpu: "100m"
    memory: "128Mi"
  limits:
    cpu: "500m"
    memory: "256Mi"
```

### ♻️ 3. Liveness & Readiness Probes
- Helps Kubernetes restart your container or wait until it’s ready

### 📦 4. Immutable Image Tags
- Avoid `latest`; use versioned, immutable tags (e.g. `hello-k8s:v3`)

### 🔍 5. Logging and Monitoring
- Use `stdout/stderr` for logs
- Expose Prometheus metrics via `/metrics`

### 📁 6. Use Helm Charts (or Kustomize)
- Simplifies deployment, templating, and versioning

### 📡 7. Ingress & HTTPS
- Expose app via Ingress
- Use cert-manager or external DNS for TLS certs

---

## 🔄 Step 23: CI/CD with GitHub Actions for Kubernetes

Automate Docker build, push, and Kubernetes deploy on every commit.

### 💡 Assumptions:
- You have a remote cluster (or Minikube with `kubectl` on GitHub runner)
- You're using DockerHub or GHCR
- GitHub Secrets:
  - `DOCKER_USERNAME`
  - `DOCKER_PASSWORD`
  - `KUBE_CONFIG` (base64-encoded)

### 📄 `.github/workflows/deploy.yaml`
```yaml
name: Deploy to Kubernetes

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout Code
      uses: actions/checkout@v3

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3

    - name: Login to Docker Hub
      run: echo "${{ secrets.DOCKER_PASSWORD }}" | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin

    - name: Build and Push Image
      run: |
        docker build -t ${{ secrets.DOCKER_USERNAME }}/hello-k8s:${{ github.sha }} .
        docker push ${{ secrets.DOCKER_USERNAME }}/hello-k8s:${{ github.sha }}

    - name: Set up kubectl
      run: |
        echo "${{ secrets.KUBE_CONFIG }}" | base64 -d > kubeconfig
        export KUBECONFIG=$PWD/kubeconfig
        kubectl config current-context

    - name: Deploy to Kubernetes
      run: |
        kubectl set image deployment/hello-deployment hello=${{ secrets.DOCKER_USERNAME }}/hello-k8s:${{ github.sha }}
        kubectl rollout status deployment/hello-deployment
```

Tip: Use Helm or Kustomize in CI/CD for complex deployments.

---

## ☁️ Step 24: Moving from Minikube to Cloud

### 🔄 Export Manifests
```bash
kubectl get all -o yaml > complete-backup.yaml
```
Clean up IPs, UIDs, etc.

### 🏁 Choose a Cloud Platform:

#### GKE (Google Cloud)
```bash
gcloud container clusters create ...
```

#### EKS (Amazon)
```bash
eksctl create cluster
```

#### AKS (Azure)
```bash
az aks create ...
```

### 🔌 Connect your kubectl
```bash
gcloud container clusters get-credentials ...
```
Then reuse the same manifests from Minikube.

---

## 🧠 Final Thoughts

You built a local production-grade Kubernetes setup with:

- Minikube
- Prometheus & Grafana
- Ingress + TLS
- CI/CD

That’s a huge achievement. 🚀

---

## 📚 Series Recap

| Part | Title | What You Learned |
|------|-------|------------------|
| 1 | Local Deployment | Minikube, Docker, basic Deployment & Service |
| 2 | Configuration | ConfigMaps, Secrets, Health Probes |
| 3 | Security & Access | Ingress, TLS, Self-signed certs |
| 4 | Observability | Prometheus, Grafana, app metrics |
| 5 | CI/CD & Best Practices | GitHub Actions, Helm, production readiness |

---

## 🎁 Bonus: Things to Explore Next

- cert-manager for automatic Let’s Encrypt TLS
- Kustomize vs Helm
- ArgoCD or Flux for GitOps
- Pod Security Policies
- HPA (Horizontal Pod Autoscaling)
- Service Mesh (Istio, Linkerd)

---

👏 Thanks for reading this series!

💬 Questions or feedback? Tweet at me [@yourhandle]  
🔖 Bookmark this series as your Kubernetes reference.

---

Happy deploying! ☸️🐳
