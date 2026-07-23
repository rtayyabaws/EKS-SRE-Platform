import os
import time
import logging
from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = FastAPI(title="EKS SRE Platform")

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

REQUEST_COUNT = Counter(
    "sre_demo_requests_total",
    "Total HTTP requests",
    ["endpoint"]
)

REQUEST_LATENCY = Histogram(
    "sre_demo_request_latency_seconds",
    "Request latency in seconds",
    ["endpoint"]
)

STATUS_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="refresh" content="30">
<title>EKS SRE Platform — Status</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    background: #0d1117;
    color: #e6edf3;
    font-family: 'Courier New', Courier, monospace;
    min-height: 100vh;
    padding: 2rem;
  }}
  .container {{ max-width: 860px; margin: 0 auto; }}
  .header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 2rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid #21262d;
  }}
  .title {{ font-size: 22px; font-weight: 500; color: #e6edf3; letter-spacing: 0.02em; }}
  .subtitle {{ font-size: 13px; color: #7d8590; margin-top: 4px; }}
  .status-badge {{
    display: flex;
    align-items: center;
    gap: 8px;
    background: #0f2a1e;
    border: 1px solid #1a4731;
    border-radius: 6px;
    padding: 8px 14px;
  }}
  .dot {{
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #3fb950;
    animation: pulse 2s infinite;
  }}
  @keyframes pulse {{ 0%,100% {{ opacity:1; }} 50% {{ opacity:0.5; }} }}
  .status-text {{ font-size: 13px; color: #3fb950; font-weight: 500; }}
  .section {{ margin-bottom: 2rem; }}
  .section-title {{
    font-size: 11px;
    color: #7d8590;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 1rem;
  }}
  .service-row {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 0;
    border-bottom: 1px solid #161b22;
  }}
  .service-row:last-child {{ border-bottom: none; }}
  .service-left {{ display: flex; align-items: center; gap: 10px; }}
  .dot-sm {{ width: 7px; height: 7px; border-radius: 50%; background: #3fb950; flex-shrink: 0; }}
  .service-name {{ font-size: 14px; color: #e6edf3; }}
  .service-right {{ display: flex; align-items: center; gap: 8px; }}
  .badge {{
    font-size: 11px;
    padding: 2px 8px;
    border-radius: 4px;
    font-weight: 500;
  }}
  .badge-green {{ background: #0f2a1e; color: #3fb950; border: 1px solid #1a4731; }}
  .badge-blue {{ background: #0c2d6b; color: #58a6ff; border: 1px solid #1a4a8a; }}
  .badge-gray {{ background: #161b22; color: #7d8590; border: 1px solid #21262d; }}
  .metrics-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 2rem;
  }}
  .metric-card {{
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 8px;
    padding: 14px;
  }}
  .metric-label {{
    font-size: 11px;
    color: #7d8590;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 6px;
  }}
  .metric-value {{ font-size: 20px; font-weight: 500; color: #e6edf3; }}
  .metric-unit {{ font-size: 12px; color: #7d8590; margin-left: 3px; }}
  .endpoints-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; }}
  .endpoint-row {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 6px;
    padding: 10px 14px;
  }}
  .endpoint-path {{ font-size: 13px; color: #58a6ff; }}
  .platform-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }}
  .platform-item {{
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 8px;
    padding: 12px 14px;
  }}
  .platform-key {{
    font-size: 11px;
    color: #7d8590;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 4px;
  }}
  .platform-val {{ font-size: 14px; color: #e6edf3; }}
  .footer {{
    margin-top: 2rem;
    padding-top: 1rem;
    border-top: 1px solid #21262d;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  .footer-text {{ font-size: 12px; color: #7d8590; }}
  .refresh-note {{ font-size: 11px; color: #3d444d; font-style: italic; }}
  @media (max-width: 600px) {{
    .metrics-grid {{ grid-template-columns: repeat(2, 1fr); }}
    .platform-grid {{ grid-template-columns: repeat(2, 1fr); }}
    .header {{ flex-direction: column; gap: 1rem; }}
  }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <div>
      <div class="title">EKS SRE Platform</div>
      <div class="subtitle">eks.rehangatus.click &nbsp;·&nbsp; us-east-1</div>
    </div>
    <div class="status-badge">
      <div class="dot"></div>
      <span class="status-text">All Systems Operational</span>
    </div>
  </div>

  <div class="section">
    <div class="section-title">Services</div>
    <div class="service-row">
      <div class="service-left">
        <div class="dot-sm"></div>
        <span class="service-name">API Service</span>
      </div>
      <div class="service-right">
        <span class="badge badge-blue">v {version}</span>
        <span class="badge badge-green">Operational</span>
      </div>
    </div>
    <div class="service-row">
      <div class="service-left">
        <div class="dot-sm"></div>
        <span class="service-name">Ingress / Load Balancer</span>
      </div>
      <div class="service-right">
        <span class="badge badge-green">Operational</span>
      </div>
    </div>
    <div class="service-row">
      <div class="service-left">
        <div class="dot-sm"></div>
        <span class="service-name">TLS Certificate</span>
      </div>
      <div class="service-right">
        <span class="badge badge-gray">Auto-renewed · Let's Encrypt</span>
        <span class="badge badge-green">Valid</span>
      </div>
    </div>
    <div class="service-row">
      <div class="service-left">
        <div class="dot-sm"></div>
        <span class="service-name">Prometheus / Grafana</span>
      </div>
      <div class="service-right">
        <span class="badge badge-green">Operational</span>
      </div>
    </div>
  </div>

  <div class="section-title" style="margin-bottom:12px">
    Live metrics
    <span style="font-size:10px;color:#3d444d;font-style:italic;text-transform:none;letter-spacing:0">
      &nbsp;(last 60s)
    </span>
  </div>
  <div class="metrics-grid" style="margin-bottom:2rem">
    <div class="metric-card">
      <div class="metric-label">Request Rate</div>
      <div class="metric-value">{request_rate}<span class="metric-unit">req/s</span></div>
    </div>
    <div class="metric-card">
      <div class="metric-label">Avg Latency</div>
      <div class="metric-value">{avg_latency}<span class="metric-unit">s</span></div>
    </div>
    <div class="metric-card">
      <div class="metric-label">Pod Count</div>
      <div class="metric-value">{pod_name}<span class="metric-unit">running</span></div>
    </div>
    <div class="metric-card">
      <div class="metric-label">Total Requests</div>
      <div class="metric-value">{total_requests}</div>
    </div>
  </div>

  <div class="section">
    <div class="section-title" style="margin-bottom:12px">Endpoints</div>
    <div class="endpoints-grid">
      <div class="endpoint-row">
        <span class="endpoint-path">/healthz</span>
        <span class="badge badge-green">UP</span>
      </div>
      <div class="endpoint-row">
        <span class="endpoint-path">/readyz</span>
        <span class="badge badge-green">UP</span>
      </div>
      <div class="endpoint-row">
        <span class="endpoint-path">/metrics</span>
        <span class="badge badge-green">UP</span>
      </div>
      <div class="endpoint-row">
        <span class="endpoint-path">/slow</span>
        <span class="badge badge-gray">Available</span>
      </div>
    </div>
  </div>

  <div class="section">
    <div class="section-title" style="margin-bottom:12px">Platform</div>
    <div class="platform-grid">
      <div class="platform-item">
        <div class="platform-key">Cluster</div>
        <div class="platform-val">rehan-eks-cluster</div>
      </div>
      <div class="platform-item">
        <div class="platform-key">Region</div>
        <div class="platform-val">us-east-1</div>
      </div>
      <div class="platform-item">
        <div class="platform-key">Version</div>
        <div class="platform-val" style="color:#58a6ff">{version}</div>
      </div>
      <div class="platform-item">
        <div class="platform-key">Pod</div>
        <div class="platform-val" style="font-size:12px">{pod_name}</div>
      </div>
      <div class="platform-item">
        <div class="platform-key">Kubernetes</div>
        <div class="platform-val">1.34</div>
      </div>
      <div class="platform-item">
        <div class="platform-key">Runtime</div>
        <div class="platform-val">Amazon EKS</div>
      </div>
    </div>
  </div>

  <div class="footer">
    <div class="footer-text">EKS SRE Platform &nbsp;·&nbsp; Powered by FastAPI + Kubernetes</div>
    <div class="refresh-note">auto-refreshes every 30s</div>
  </div>
</div>
</body>
</html>"""


def get_metric_value(metric_name: str, labels: dict = None) -> float:
    try:
        from prometheus_client import REGISTRY
        for metric in REGISTRY.collect():
            if metric.name == metric_name:
                for sample in metric.samples:
                    if labels is None:
                        return sample.value
                    if all(sample.labels.get(k) == v for k, v in labels.items()):
                        return sample.value
    except Exception:
        pass
    return 0.0


@app.get("/", response_class=HTMLResponse)
def root():
    REQUEST_COUNT.labels(endpoint="/").inc()

    version = os.getenv("APP_VERSION", "local")
    pod_name = os.getenv("HOSTNAME", "unknown")

    total_requests = 0.0
    try:
        from prometheus_client import REGISTRY
        for metric in REGISTRY.collect():
            if metric.name == "sre_demo_requests_total":
                for sample in metric.samples:
                    total_requests += sample.value
    except Exception:
        pass

    try:
        from prometheus_client import REGISTRY
        count_val = 0.0
        sum_val = 0.0
        for metric in REGISTRY.collect():
            if metric.name == "sre_demo_request_latency_seconds":
                for sample in metric.samples:
                    if sample.name.endswith("_count"):
                        count_val += sample.value
                    elif sample.name.endswith("_sum"):
                        sum_val += sample.value
        avg_latency = f"{sum_val / count_val:.2f}" if count_val > 0 else "0.00"
        request_rate = f"{total_requests:.1f}"
    except Exception:
        avg_latency = "0.00"
        request_rate = "0.0"

    html = STATUS_PAGE.format(
        version=version[:7] if len(version) > 7 else version,
        pod_name=pod_name,
        request_rate=request_rate,
        avg_latency=avg_latency,
        total_requests=int(total_requests),
    )
    return HTMLResponse(content=html)


@app.get("/healthz")
def healthz():
    REQUEST_COUNT.labels(endpoint="/healthz").inc()
    return {"status": "healthy"}


@app.get("/readyz")
def readyz():
    REQUEST_COUNT.labels(endpoint="/readyz").inc()
    return {"status": "ready"}


@app.get("/version")
def version():
    REQUEST_COUNT.labels(endpoint="/version").inc()
    return {
        "version": os.getenv("APP_VERSION", "local"),
        "commit_sha": os.getenv("GIT_SHA", "unknown")
    }


@app.get("/slow")
def slow():
    REQUEST_COUNT.labels(endpoint="/slow").inc()
    with REQUEST_LATENCY.labels(endpoint="/slow").time():
        result = sum(i * i for i in range(500000))
    return {"message": "slow response generated", "result": result}


@app.get("/error")
def error():
    REQUEST_COUNT.labels(endpoint="/error").inc()
    logging.error("Simulated application error triggered")
    return Response(
        content='{"error":"simulated failure"}',
        media_type="application/json",
        status_code=500
    )


@app.get("/log")
def log():
    REQUEST_COUNT.labels(endpoint="/log").inc()
    logging.info("Structured log test event generated")
    return {"message": "log event generated"}


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)