import uuid
from datetime import datetime
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Query, Path
from fastapi.middleware.cors import CORSMiddleware

from models import (
    YieldCurveResponse,
    ComputeJobRequest,
    ComputeJobSubmissionResponse,
    ComputeJobResultResponse,
    PricingRequest,
    PricingResponse,
    CashFlowPoint,
    HealthCheckResponse
)
from data import (
    BONDS_YIELD_CURVE_DATA,
    COMPUTE_JOBS_STORE,
    HEALTH_TELEMETRY_DATA
)

app = FastAPI(
    title="Fixed Income Analytics Compute Microservice",
    description="High-performance compute engine microservices for Fixed Income Markets & Risk Analytics.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for cross-origin browser clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------------------------------------------------------------------
# Endpoint 1: Bond Yield Curve & Risk Analytics
# ----------------------------------------------------------------------
@app.get(
    "/api/v1/analytics/fixed-income/bonds/{isin}/yield-curve",
    response_model=YieldCurveResponse,
    summary="Get Bond Yield Curve & Risk Analytics",
    tags=["Fixed Income Analytics"]
)
def get_bond_yield_curve(
    isin: str = Path(..., description="12-character ISIN code", example="US912828C497"),
    curve_type: str = Query("treasury", description="Curve benchmark type"),
    as_of_date: Optional[str] = Query(None, description="Calculation date YYYY-MM-DD")
) -> YieldCurveResponse:
    """
    Retrieve yield curve calculations, duration, convexity, and benchmark spread analysis for a fixed-income bond.
    """
    formatted_isin = isin.upper()
    if formatted_isin in BONDS_YIELD_CURVE_DATA:
        data = BONDS_YIELD_CURVE_DATA[formatted_isin].copy()
    else:
        # Fallback realistic bond data for any valid ISIN string passed in demo
        data = {
            "isin": formatted_isin,
            "bond_name": f"Corporate Bond ({formatted_isin[:4]} Senior Notes)",
            "currency": "USD",
            "as_of_date": as_of_date or "2026-08-17",
            "yield_to_maturity_percent": 5.120,
            "modified_duration": 5.85,
            "macaulay_duration": 6.01,
            "convexity": 42.10,
            "benchmark_spread_bps": 85.0,
            "yield_curve_points": [
                {"tenor": "1Y", "rate_percent": 5.25},
                {"tenor": "2Y", "rate_percent": 4.95},
                {"tenor": "5Y", "rate_percent": 5.05},
                {"tenor": "10Y", "rate_percent": 5.120}
            ]
        }
    
    if as_of_date:
        data["as_of_date"] = as_of_date

    return YieldCurveResponse(**data)


# ----------------------------------------------------------------------
# Endpoint 2: Submit Portfolio Risk Compute Job
# ----------------------------------------------------------------------
@app.post(
    "/api/v1/analytics/compute-jobs",
    response_model=ComputeJobSubmissionResponse,
    status_code=201,
    summary="Submit Portfolio Risk Compute Job",
    tags=["Compute Platform"]
)
def submit_compute_job(request: ComputeJobRequest) -> ComputeJobSubmissionResponse:
    """
    Submits a financial compute job for portfolio risk analysis (Monte Carlo VaR, Stress Testing, DV01).
    """
    job_uuid = f"job-analytics-{uuid.uuid4().hex[:5]}"
    now_str = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    submission_data = {
        "job_id": job_uuid,
        "portfolio_id": request.portfolio_id,
        "status": "QUEUED",
        "created_at": now_str,
        "cluster_node": "grid-node-ny4-88.analytics.internal",
        "estimated_runtime_seconds": 1.85,
        "poll_url": f"/api/v1/analytics/compute-jobs/{job_uuid}"
    }

    # Store in memory for retrieval by Endpoint 3
    COMPUTE_JOBS_STORE[job_uuid] = {
        "job_id": job_uuid,
        "portfolio_id": request.portfolio_id,
        "status": "COMPLETED",
        "created_at": now_str,
        "completed_at": now_str,
        "execution_time_seconds": 1.64,
        "metrics": {
            "value_at_risk_99_usd": 2850000.0,
            "expected_shortfall_usd": 3520000.0,
            "dv01_usd": 54200.0,
            "net_portfolio_value_usd": 175000000.0
        },
        "stress_test_loss_usd": {
            "rates_up_100bps": -4200000.0,
            "rates_down_100bps": 4500000.0,
            "credit_spread_widening_50bps": -2100000.0
        },
        "compute_grid_stats": {
            "cpu_cores_utilized": 64,
            "gpu_acceleration": True,
            "memory_peak_mb": 4096,
            "node_id": "grid-node-ny4-88.analytics.internal"
        }
    }

    return ComputeJobSubmissionResponse(**submission_data)


# ----------------------------------------------------------------------
# Endpoint 3: Fetch Compute Job Status and Results
# ----------------------------------------------------------------------
@app.get(
    "/api/v1/analytics/compute-jobs/{job_id}",
    response_model=ComputeJobResultResponse,
    summary="Get Compute Job Result",
    tags=["Compute Platform"]
)
def get_compute_job_result(
    job_id: str = Path(..., description="Unique job ID identifier", example="job-analytics-98421")
) -> ComputeJobResultResponse:
    """
    Fetch the execution status and computed quantitative risk result metrics for a submitted analytics job.
    """
    if job_id in COMPUTE_JOBS_STORE:
        res = COMPUTE_JOBS_STORE[job_id]
    else:
        # Provide deterministic hardcoded demo result if an unknown job_id is requested
        res = {
            "job_id": job_id,
            "portfolio_id": "PORT-DEMO-FI",
            "status": "COMPLETED",
            "completed_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "execution_time_seconds": 1.50,
            "metrics": {
                "value_at_risk_99_usd": 1950000.0,
                "expected_shortfall_usd": 2400000.0,
                "dv01_usd": 32000.0,
                "net_portfolio_value_usd": 100000000.0
            },
            "stress_test_loss_usd": {
                "rates_up_100bps": -2500000.0,
                "rates_down_100bps": 2700000.0,
                "credit_spread_widening_50bps": -1200000.0
            },
            "compute_grid_stats": {
                "cpu_cores_utilized": 32,
                "gpu_acceleration": True,
                "memory_peak_mb": 2048,
                "node_id": "grid-node-ny4-12.analytics.internal"
            }
        }

    return ComputeJobResultResponse(**res)


# ----------------------------------------------------------------------
# Endpoint 4: Fixed Income Pricing Engine & Cash Flow Schedule
# ----------------------------------------------------------------------
@app.post(
    "/api/v1/analytics/fixed-income/pricing",
    response_model=PricingResponse,
    summary="Calculate Bond Pricing & Cash Flow Sensitivity",
    tags=["Fixed Income Analytics"]
)
def calculate_bond_pricing(request: PricingRequest) -> PricingResponse:
    """
    Calculates clean/dirty pricing, accrued interest, cash flow schedules, and yield sensitivity analysis.
    """
    # Deterministic price calculation formula
    base_price = 1000.0 * (1.0 + (request.coupon_rate_percent - request.yield_to_maturity_percent) * 0.045)
    clean_price = round(base_price, 2)
    dirty_price = clean_price  # Settlement on coupon date
    
    # Calculate price sensitivity under rate shifts (+50 bps and -50 bps)
    shift_down = round(clean_price * (1.0 + 0.050 * 0.0438), 2)
    shift_up = round(clean_price * (1.0 - 0.050 * 0.0438), 2)
    
    # Generate realistic cash flow schedule
    cash_flows = [
        CashFlowPoint(
            payment_date="2027-02-17",
            coupon_amount=22.50,
            principal_amount=0.0,
            total_cash_flow=22.50,
            present_value=22.03
        ),
        CashFlowPoint(
            payment_date="2027-08-17",
            coupon_amount=22.50,
            principal_amount=0.0,
            total_cash_flow=22.50,
            present_value=21.57
        ),
        CashFlowPoint(
            payment_date="2031-08-17",
            coupon_amount=22.50,
            principal_amount=1000.0,
            total_cash_flow=1022.50,
            present_value=832.14
        )
    ]

    return PricingResponse(
        clean_price=clean_price,
        dirty_price=dirty_price,
        accrued_interest=0.0,
        modified_duration=4.38,
        pv01=round(clean_price * 0.000438, 3),
        price_sensitivity={
            "base_price": clean_price,
            "price_shift_up_50bps": shift_up,
            "price_shift_down_50bps": shift_down
        },
        cash_flow_schedule=cash_flows
    )


# ----------------------------------------------------------------------
# Endpoint 5: System Telemetry & Compute Grid Health
# ----------------------------------------------------------------------
@app.get(
    "/api/v1/analytics/health",
    response_model=HealthCheckResponse,
    summary="Compute Platform Health Telemetry",
    tags=["System Telemetry"]
)
def get_health_telemetry(
    verbose: bool = Query(False, description="Include detailed sub-cluster telemetry")
) -> HealthCheckResponse:
    """
    Health check and compute platform telemetry endpoint reporting cluster worker nodes, memory utilization, and active model execution engine.
    """
    return HealthCheckResponse(**HEALTH_TELEMETRY_DATA)
