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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)