# Fixed Income Analytics & Compute Microservice

An enterprise-grade Python backend microservice implementing a high-performance **Fixed Income Analytics & Risk Compute Platform**.

This service supports quantitative model execution (Monte Carlo VaR, Stress Testing, Yield Curve construction, and Bond Pricing) along with real-time telemetry for grid compute worker nodes.

---

## 🏛️ Platform Architecture

The platform architecture features:
* **Financial Model Compute Engine**: High-performance risk calculations (Monte Carlo VaR, Expected Shortfall, DV01) and fixed-income analytics (yield curves, pricing, duration).
* **Modern Python Microservices**: Clean, robust microservice APIs serving internal and external financial services clients.
* **Telemetry & Grid Infrastructure**: Real-time monitoring of microservice health, memory load, and grid compute worker nodes.

---

## 🚀 Quickstart Guide

### Prerequisites
* Python 3.9+
* `pip`

### 1. Installation
Clone or navigate to the project root directory and install dependencies:

```bash
pip install -r requirements.txt
```

### 2. Run the API Server
Start the local server using `uvicorn`:

```bash
uvicorn main:app --reload --port 8000
```

The interactive OpenAPI / Swagger documentation will be available at:
* **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### 3. Run Automated Unit Tests
```bash
pytest test_main.py
```

---

## 📡 RESTful API Endpoints & Concrete JSON Payloads

The backend provides 5 core RESTful API endpoints. Below are the exact HTTP specs and pretty-printed JSON request and response payloads.

---

### Endpoint 1: Get Bond Yield Curve & Risk Analytics
* **HTTP Method**: `GET`
* **Path**: `/api/v1/analytics/fixed-income/bonds/{isin}/yield-curve`
* **Description**: Returns yield curve tenor points, yield-to-maturity, modified duration, macaulay duration, convexity, and benchmark spread metrics for a fixed-income security (e.g. US Treasury).

#### Request Example
* **URL**: `/api/v1/analytics/fixed-income/bonds/US912828C497/yield-curve?curve_type=treasury&as_of_date=2026-08-17`
* **Body**: `None (GET Request)`

#### Response JSON (`200 OK`)
```json
{
  "isin": "US912828C497",
  "bond_name": "US Treasury N/B 4.125% 2033",
  "currency": "USD",
  "as_of_date": "2026-08-17",
  "yield_to_maturity_percent": 4.285,
  "modified_duration": 7.42,
  "macaulay_duration": 7.58,
  "convexity": 68.45,
  "benchmark_spread_bps": 14.5,
  "yield_curve_points": [
    {
      "tenor": "3M",
      "rate_percent": 5.22
    },
    {
      "tenor": "6M",
      "rate_percent": 5.1
    },
    {
      "tenor": "1Y",
      "rate_percent": 4.85
    },
    {
      "tenor": "2Y",
      "rate_percent": 4.45
    },
    {
      "tenor": "5Y",
      "rate_percent": 4.2
    },
    {
      "tenor": "10Y",
      "rate_percent": 4.285
    },
    {
      "tenor": "30Y",
      "rate_percent": 4.52
    }
  ]
}
```

---

### Endpoint 2: Submit Portfolio Risk Compute Job
* **HTTP Method**: `POST`
* **Path**: `/api/v1/analytics/compute-jobs`
* **Description**: Submits a high-performance quantitative risk simulation job (e.g., 100,000 Monte Carlo iterations, Value-at-Risk, Expected Shortfall, Stress Testing) to the compute cluster.

#### Request JSON
```json
{
  "portfolio_id": "PORT-FI-9902",
  "model_name": "MonteCarlo_VaR_Engine_v4",
  "simulation_iterations": 100000,
  "confidence_level": 0.99,
  "metrics": [
    "VaR",
    "ExpectedShortfall",
    "DV01"
  ],
  "stress_scenario": "2008_Lehman_Crash"
}
```

#### Response JSON (`201 Created`)
```json
{
  "job_id": "job-analytics-98421",
  "portfolio_id": "PORT-FI-9902",
  "status": "QUEUED",
  "created_at": "2026-08-17T12:40:00Z",
  "cluster_node": "grid-node-ny4-88.analytics.internal",
  "estimated_runtime_seconds": 1.85,
  "poll_url": "/api/v1/analytics/compute-jobs/job-analytics-98421"
}
```

---

### Endpoint 3: Get Compute Job Status & Risk Results
* **HTTP Method**: `GET`
* **Path**: `/api/v1/analytics/compute-jobs/{job_id}`
* **Description**: Retrieves the status, execution telemetry, and calculated quantitative metrics (VaR 99%, Expected Shortfall, DV01, Stress Test Losses) for a submitted compute job.

#### Request Example
* **URL**: `/api/v1/analytics/compute-jobs/job-analytics-98421`
* **Body**: `None (GET Request)`

#### Response JSON (`200 OK`)
```json
{
  "job_id": "job-analytics-98421",
  "portfolio_id": "PORT-FI-9902",
  "status": "COMPLETED",
  "completed_at": "2026-08-17T12:40:02Z",
  "execution_time_seconds": 1.64,
  "metrics": {
    "value_at_risk_99_usd": 2450000.0,
    "expected_shortfall_usd": 3120000.0,
    "dv01_usd": 48500.0,
    "net_portfolio_value_usd": 150000000.0
  },
  "stress_test_loss_usd": {
    "rates_up_100bps": -3850000.0,
    "rates_down_100bps": 4100000.0,
    "credit_spread_widening_50bps": -1950000.0
  },
  "compute_grid_stats": {
    "cpu_cores_utilized": 64,
    "gpu_acceleration": true,
    "memory_peak_mb": 4096,
    "node_id": "grid-node-ny4-88.analytics.internal"
  }
}
```

---

### Endpoint 4: Calculate Bond Pricing & Cash Flow Sensitivity
* **HTTP Method**: `POST`
* **Path**: `/api/v1/analytics/fixed-income/pricing`
* **Description**: Evaluates clean price, dirty price, accrued interest, duration, PV01, cash flow discount schedule, and parallel rate shift sensitivities (+/- 50 bps).

#### Request JSON
```json
{
  "face_value": 1000.0,
  "coupon_rate_percent": 4.5,
  "payment_frequency_per_year": 2,
  "settlement_date": "2026-08-17",
  "maturity_date": "2031-08-17",
  "yield_to_maturity_percent": 4.25,
  "rate_shift_bps": 50.0
}
```

#### Response JSON (`200 OK`)
```json
{
  "clean_price": 1011.24,
  "dirty_price": 1011.24,
  "accrued_interest": 0.0,
  "modified_duration": 4.38,
  "pv01": 0.443,
  "price_sensitivity": {
    "base_price": 1011.24,
    "price_shift_up_50bps": 989.45,
    "price_shift_down_50bps": 1033.62
  },
  "cash_flow_schedule": [
    {
      "payment_date": "2027-02-17",
      "coupon_amount": 22.5,
      "principal_amount": 0.0,
      "total_cash_flow": 22.5,
      "present_value": 22.03
    },
    {
      "payment_date": "2027-08-17",
      "coupon_amount": 22.5,
      "principal_amount": 0.0,
      "total_cash_flow": 22.5,
      "present_value": 21.57
    },
    {
      "payment_date": "2031-08-17",
      "coupon_amount": 22.5,
      "principal_amount": 1000.0,
      "total_cash_flow": 1022.5,
      "present_value": 832.14
    }
  ]
}
```

---

### Endpoint 5: Compute Platform Health Telemetry
* **HTTP Method**: `GET`
* **Path**: `/api/v1/analytics/health`
* **Description**: Returns health metrics, native C++ analytics engine version, active compute grid nodes, memory load, and queue depth for monitoring service SLA.

#### Request Example
* **URL**: `/api/v1/analytics/health?verbose=true`
* **Body**: `None (GET Request)`

#### Response JSON (`200 OK`)
```json
{
  "status": "HEALTHY",
  "service": "fixed-income-analytics-compute-platform",
  "version": "1.0.0",
  "cpp_analytics_engine_version": "v4.2.1-native",
  "cluster_nodes_active": 128,
  "memory_usage_percent": 42.5,
  "queue_depth": 3,
  "uptime_seconds": 864000
}
```

---

## 🛠️ Tech Stack & Directory Structure

```
.
├── main.py            # FastAPI application routes & endpoints logic
├── models.py          # Pydantic data schemas for requests and responses
├── data.py            # Hardcoded concrete financial datasets & telemetry
├── test_main.py       # Pytest unit tests for all 5 endpoints
├── requirements.txt   # Dependencies (fastapi, uvicorn, pydantic, pytest, httpx)
└── README.md          # Comprehensive documentation with JSON examples
```
