# 🚀 Deploying a Simple App to Kubernetes with Minikube

![GitHub Repo stars](https://img.shields.io/github/stars/adityar947/k8s-minikube-tutorial?style=social)
![GitHub last commit](https://img.shields.io/github/last-commit/adityar947/k8s-minikube-tutorial)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/adityar947/k8s-minikube-tutorial/ci.yml)

Welcome to this hands-on, beginner-to-intermediate level tutorial series designed to teach you how to deploy, manage, secure, and monitor an application on a **Kubernetes cluster using Minikube**.

This repository is structured into 5 progressive parts, each building upon the previous one, helping you evolve a basic app deployment into a production-grade pipeline — all from your local development machine.

---

## 🌟 Project Goals

By the end of this tutorial series, you'll be able to:

- Set up a local Kubernetes cluster using Minikube
- Deploy and expose applications on Kubernetes
- Use ConfigMaps, Secrets, and Probes
- Configure Ingress and TLS certificates
- Monitor your app with Prometheus & Grafana
- Implement rolling updates and rollback strategies
- Transition your setup toward production-readiness
- Integrate CI/CD pipelines using GitHub Actions

---

## 📁 Repository Structure

```
k8s-minikube-tutorial/
├── part1-zero-to-cluster/
├── part2-deployment-enhancements/
├── part3-ingress-tls-secrets/
├── part4-monitoring-prometheus-grafana/
├── part5-ci-cd-production/
└── README.md
```

---

## 🛠 Prerequisites

| Tool     | Version (Recommended) | Install Link |
|----------|-----------------------|--------------|
| Docker   | 20.x+                 | [Install Docker](https://www.docker.com/) |
| kubectl  | 1.27+                 | [Install kubectl](https://kubernetes.io/docs/tasks/tools/) |
| Minikube | 1.30+                 | [Install Minikube](https://minikube.sigs.k8s.io/) |
| Git      | Any                   | [Install Git](https://git-scm.com/) |

---

## 🚀 Getting Started

```bash
git clone https://github.com/yourusername/k8s-minikube-tutorial.git
cd k8s-minikube-tutorial/part1-zero-to-cluster
```

---

## 🧩 Tutorial Breakdown

### 🧱 Part 1: From Zero to Local Cluster

- Install Minikube and kubectl
- Start a local Kubernetes cluster
- Containerize a sample app using Docker
- Deploy the app to Kubernetes
- Expose it using a NodePort service

### ⚙️ Part 2: Enhancing Your Deployment

- Use ConfigMaps and Secrets
- Add Readiness and Liveness Probes
- Apply rolling updates and test rollback scenarios
- Use `kubectl rollout`

### 🌐 Part 3: Securing and Routing Your App

- Install NGINX Ingress Controller
- Set up custom domains
- Secure traffic using TLS certificates
- Use Kubernetes Secrets

### 📈 Part 4: Monitoring with Prometheus & Grafana

- Deploy Prometheus Operator
- Configure ServiceMonitor
- Deploy Grafana and import dashboards

### 🚢 Part 5: From Local to Production

- Kubernetes deployment best practices
- Resource limits, pod anti-affinity
- CI/CD pipeline with GitHub Actions

---

## 🔐 Security Notes

Do **not** use self-signed certs or in-cluster secrets in production. Use:

- cert-manager with Let’s Encrypt
- External secret managers (Vault, Sealed Secrets)
- RBAC policies with least privilege

---

## 📌 Troubleshooting

**Minikube won’t start?**

```bash
minikube delete
minikube start --driver=docker
```

**Can’t access NodePort service?**

```bash
minikube tunnel
```

**Ingress not working?**

```bash
minikube addons enable ingress
```

---

## 🙋 FAQ

- **Q:** Can I run this on Windows/Mac?  
  **A:** Yes. WSL2 recommended for Windows.

- **Q:** Will this scale to real production?  
  **A:** Yes, practices can be adapted to GKE, EKS, AKS.

- **Q:** Is this good for beginners?  
  **A:** Absolutely.

---

## 🤝 Contributing

```bash
git checkout -b my-improvements
# make changes
git commit -am "Improved docs"
git push origin my-improvements
```

Then open a Pull Request.

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙌 Acknowledgements

- Kubernetes Docs
- Minikube Maintainers
- Prometheus & Grafana Teams

---

Happy shipping! ☸️🐳
