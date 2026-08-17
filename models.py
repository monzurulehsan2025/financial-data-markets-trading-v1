from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


# ----------------------------------------------------------------------
# 1. Bond Yield Curve Analytics Models
# ----------------------------------------------------------------------
class YieldCurvePoint(BaseModel):
    tenor: str = Field(..., example="10Y")
    rate_percent: float = Field(..., example="4.25")

class YieldCurveResponse(BaseModel):
    isin: str = Field(..., example="US912828C497")
    bond_name: str = Field(..., example="US Treasury N/B 4.125% 2033")
    currency: str = Field(..., example="USD")
    as_of_date: str = Field(..., example="2026-08-17")
    yield_to_maturity_percent: float = Field(..., example="4.285")
    modified_duration: float = Field(..., example="7.42")
    macaulay_duration: float = Field(..., example="7.58")
    convexity: float = Field(..., example="68.45")
    benchmark_spread_bps: float = Field(..., example="14.5")
    yield_curve_points: List[YieldCurvePoint]


# ----------------------------------------------------------------------
# 2. Portfolio Risk Compute Job Submission Models
# ----------------------------------------------------------------------
class ComputeJobRequest(BaseModel):
    portfolio_id: str = Field(..., example="PORT-FI-9902")
    model_name: str = Field(..., example="MonteCarlo_VaR_Engine_v4")
    simulation_iterations: int = Field(..., example=100000)
    confidence_level: float = Field(..., example=0.99)
    metrics: List[str] = Field(..., example=["VaR", "ExpectedShortfall", "DV01"])
    stress_scenario: Optional[str] = Field("2008_Lehman_Crash", example="2008_Lehman_Crash")

class ComputeJobSubmissionResponse(BaseModel):
    job_id: str = Field(..., example="job-analytics-98421")
    portfolio_id: str = Field(..., example="PORT-FI-9902")
    status: str = Field(..., example="QUEUED")
    created_at: str = Field(..., example="2026-08-17T12:40:00Z")
    cluster_node: str = Field(..., example="grid-node-ny4-88.analytics.internal")
    estimated_runtime_seconds: float = Field(..., example=1.85)
    poll_url: str = Field(..., example="/api/v1/analytics/compute-jobs/job-analytics-98421")


# ----------------------------------------------------------------------
# 3. Portfolio Risk Compute Job Status/Result Models
# ----------------------------------------------------------------------
class ComputeJobResultResponse(BaseModel):
    job_id: str = Field(..., example="job-analytics-98421")
    portfolio_id: str = Field(..., example="PORT-FI-9902")
    status: str = Field(..., example="COMPLETED")
    completed_at: str = Field(..., example="2026-08-17T12:40:02Z")
    execution_time_seconds: float = Field(..., example=1.64)
    metrics: Dict[str, float] = Field(
        ...,
        example={
            "value_at_risk_99_usd": 2450000.0,
            "expected_shortfall_usd": 3120000.0,
            "dv01_usd": 48500.0,
            "net_portfolio_value_usd": 150000000.0
        }
    )
    stress_test_loss_usd: Dict[str, float] = Field(
        ...,
        example={
            "rates_up_100bps": -3850000.0,
            "rates_down_100bps": 4100000.0,
            "credit_spread_widening_50bps": -1950000.0
        }
    )
    compute_grid_stats: Dict[str, Any] = Field(
        ...,
        example={
            "cpu_cores_utilized": 64,
            "gpu_acceleration": True,
            "memory_peak_mb": 4096
        }
    )


# ----------------------------------------------------------------------
# 4. Bond Pricing & Sensitivity Request/Response Models
# ----------------------------------------------------------------------
class PricingRequest(BaseModel):
    face_value: float = Field(1000.0, example=1000.0)
    coupon_rate_percent: float = Field(..., example=4.5)
    payment_frequency_per_year: int = Field(2, example=2)
    settlement_date: str = Field(..., example="2026-08-17")
    maturity_date: str = Field(..., example="2031-08-17")
    yield_to_maturity_percent: float = Field(..., example=4.25)
    rate_shift_bps: float = Field(50.0, example=50.0)

class CashFlowPoint(BaseModel):
    payment_date: str
    coupon_amount: float
    principal_amount: float
    total_cash_flow: float
    present_value: float

class PricingResponse(BaseModel):
    clean_price: float = Field(..., example=1011.24)
    dirty_price: float = Field(..., example=1011.24)
    accrued_interest: float = Field(..., example=0.0)
    modified_duration: float = Field(..., example=4.38)
    pv01: float = Field(..., example=0.443)
    price_sensitivity: Dict[str, float] = Field(
        ...,
        example={
            "base_price": 1011.24,
            "price_shift_up_50bps": 989.45,
            "price_shift_down_50bps": 1033.62
        }
    )
    cash_flow_schedule: List[CashFlowPoint]


# ----------------------------------------------------------------------
# 5. System & Compute Grid Health Telemetry Models
# ----------------------------------------------------------------------
class HealthCheckResponse(BaseModel):
    status: str = Field("HEALTHY", example="HEALTHY")
    service: str = Field("fixed-income-analytics-compute-platform", example="fixed-income-analytics-compute-platform")
    version: str = Field("1.0.0", example="1.0.0")
    cpp_analytics_engine_version: str = Field("v4.2.1-native", example="v4.2.1-native")
    cluster_nodes_active: int = Field(128, example=128)
    memory_usage_percent: float = Field(42.5, example=42.5)
    queue_depth: int = Field(3, example=3)
    uptime_seconds: int = Field(864000, example=864000)
