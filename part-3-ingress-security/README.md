
# Part 3: Securing and Routing Your App — Ingress, TLS & Secrets in Minikube
**Published in DevOps & Kubernetes | By Aditya Ranjan**

In the previous parts, we deployed a simple Flask app, managed configs, health checks, and did zero-downtime updates. Now, we’ll bring in real-world production concepts:

- Routing traffic via Ingress
- Securing traffic with TLS/SSL
- Managing sensitive info with Secrets

Let’s jump in.

## 🚦 Step 9: Enable Ingress Addon in Minikube

Minikube bundles a built-in Ingress controller (based on NGINX). Enable it with:

```bash
minikube addons enable ingress
```

Confirm the ingress controller pods are running:

```bash
kubectl get pods -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx
```

## 🛣 Step 10: Create an Ingress Resource

### 10.1 Update your service to type ClusterIP

If your service was NodePort, revert it to ClusterIP in `service.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: hello-service
spec:
  selector:
    app: hello
  ports:
  - protocol: TCP
    port: 80
    targetPort: 5000
  type: ClusterIP
```

Apply it:

```bash
kubectl apply -f service.yaml
```

### 10.2 Create an Ingress YAML

📄 `ingress.yaml`

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: hello-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: hello.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: hello-service
            port:
              number: 80
```

Apply it:

```bash
kubectl apply -f ingress.yaml
```

## 🌐 Step 11: Edit Hosts File for Local Domain

Get Minikube IP:

```bash
minikube ip
```

Edit `/etc/hosts` and add:

```
<MINIKUBE_IP> hello.local
```

## 🔒 Step 12: Enable TLS with Self-Signed Certificate

### 12.1 Generate TLS Certs

```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout tls.key -out tls.crt -subj "/CN=hello.local/O=hello.local"
```

### 12.2 Create TLS Secret

```bash
kubectl create secret tls hello-tls --cert=tls.crt --key=tls.key
```

### 12.3 Update Ingress with TLS Section

Update `ingress.yaml`:

```yaml
spec:
  tls:
  - hosts:
    - hello.local
    secretName: hello-tls
  rules:
  - host: hello.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: hello-service
            port:
              number: 80
```

Apply it:

```bash
kubectl apply -f ingress.yaml
```

## 🔑 Step 13: Use Secrets for Sensitive Data

### 13.1 Create a Secret YAML

📄 `secret.yaml`

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: api-secret
type: Opaque
data:
  API_KEY: <base64_encoded_api_key>
```

Generate base64 string:

```bash
echo -n "my-secret-key" | base64
```

Apply it:

```bash
kubectl apply -f secret.yaml
```

### 13.2 Use Secret in Deployment

Add to your container environment in `deployment.yaml`:

```yaml
env:
- name: API_KEY
  valueFrom:
    secretKeyRef:
      name: api-secret
      key: API_KEY
```

## 🔎 Step 14: Test HTTPS Access

Open your browser and navigate to:

```
https://hello.local
```

Ignore any browser warnings (self-signed certs are not trusted by browsers by default). You should see your app served over HTTPS!

## 🧹 Cleanup TLS & Ingress

```bash
kubectl delete ingress hello-ingress
kubectl delete secret hello-tls
kubectl delete service hello-service
kubectl delete deployment hello-deployment
minikube stop
```

## 🚀 What’s Next?

In the next part, we’ll explore:

- Monitoring your app with Prometheus and Grafana
- Setting up alerting
- Best practices for Kubernetes observability
