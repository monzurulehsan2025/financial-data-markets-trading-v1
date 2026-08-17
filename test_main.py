import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_endpoint_1_get_bond_yield_curve():
    """Test Endpoint 1: GET /api/v1/analytics/fixed-income/bonds/{isin}/yield-curve"""
    response = client.get("/api/v1/analytics/fixed-income/bonds/US912828C497/yield-curve")
    assert response.status_code == 200
    data = response.json()
    assert data["isin"] == "US912828C497"
    assert data["currency"] == "USD"
    assert "yield_curve_points" in data
    assert len(data["yield_curve_points"]) > 0
    assert "modified_duration" in data


def test_endpoint_2_submit_compute_job():
    """Test Endpoint 2: POST /api/v1/analytics/compute-jobs"""
    payload = {
        "portfolio_id": "PORT-TEST-9900",
        "model_name": "MonteCarlo_VaR_Engine_v4",
        "simulation_iterations": 100000,
        "confidence_level": 0.99,
        "metrics": ["VaR", "ExpectedShortfall", "DV01"],
        "stress_scenario": "2008_Lehman_Crash"
    }
    response = client.post("/api/v1/analytics/compute-jobs", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "job_id" in data
    assert data["status"] == "QUEUED"
    assert data["portfolio_id"] == "PORT-TEST-9900"


def test_endpoint_3_get_compute_job_result():
    """Test Endpoint 3: GET /api/v1/analytics/compute-jobs/{job_id}"""
    response = client.get("/api/v1/analytics/compute-jobs/job-analytics-98421")
    assert response.status_code == 200
    data = response.json()
    assert data["job_id"] == "job-analytics-98421"
    assert data["status"] == "COMPLETED"
    assert "metrics" in data
    assert "value_at_risk_99_usd" in data["metrics"]
    assert "stress_test_loss_usd" in data


def test_endpoint_4_calculate_bond_pricing():
    """Test Endpoint 4: POST /api/v1/analytics/fixed-income/pricing"""
    payload = {
        "face_value": 1000.0,
        "coupon_rate_percent": 4.5,
        "payment_frequency_per_year": 2,
        "settlement_date": "2026-08-17",
        "maturity_date": "2031-08-17",
        "yield_to_maturity_percent": 4.25,
        "rate_shift_bps": 50.0
    }
    response = client.post("/api/v1/analytics/fixed-income/pricing", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "clean_price" in data
    assert "dirty_price" in data
    assert "price_sensitivity" in data
    assert "cash_flow_schedule" in data


def test_endpoint_5_get_health_telemetry():
    """Test Endpoint 5: GET /api/v1/analytics/health"""
    response = client.get("/api/v1/analytics/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "HEALTHY"
    assert data["service"] == "fixed-income-analytics-compute-platform"
    assert "cluster_nodes_active" in data


def test_endpoint_1_get_bond_yield_curve_with_custom_date_fallback():
    """Test Endpoint 1: GET /api/v1/analytics/fixed-income/bonds/{isin}/yield-curve with custom as_of_date query parameter"""
    test_isin = "US999999X999"
    custom_date = "2026-09-01"
    response = client.get(f"/api/v1/analytics/fixed-income/bonds/{test_isin}/yield-curve?as_of_date={custom_date}")
    assert response.status_code == 200
    data = response.json()
    assert data["isin"] == test_isin
    assert data["as_of_date"] == custom_date
    assert "yield_to_maturity_percent" in data
    assert len(data["yield_curve_points"]) > 0


def test_endpoint_3_get_compute_job_result_demo_fallback():
    """Test Endpoint 3: GET /api/v1/analytics/compute-jobs/{job_id} with non-existent job ID fallback"""
    unknown_job_id = "job-unknown-99999"
    response = client.get(f"/api/v1/analytics/compute-jobs/{unknown_job_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["job_id"] == unknown_job_id
    assert data["status"] == "COMPLETED"
    assert data["portfolio_id"] == "PORT-DEMO-FI"
    assert "metrics" in data
    assert "compute_grid_stats" in data


def test_endpoint_4_calculate_bond_pricing_custom_rate_shift():
    """Test Endpoint 4: POST /api/v1/analytics/fixed-income/pricing with custom rate shift parameter"""
    payload = {
        "face_value": 1000000.0,
        "coupon_rate_percent": 5.0,
        "payment_frequency_per_year": 4,
        "settlement_date": "2026-08-17",
        "maturity_date": "2036-08-17",
        "yield_to_maturity_percent": 4.75,
        "rate_shift_bps": 100.0
    }
    response = client.post("/api/v1/analytics/fixed-income/pricing", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["clean_price"] > 0
    assert "price_shift_up_50bps" in data["price_sensitivity"]
    assert "price_shift_down_50bps" in data["price_sensitivity"]
    assert len(data["cash_flow_schedule"]) > 0



