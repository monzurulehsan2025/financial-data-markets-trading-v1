from typing import Dict, Any

# ----------------------------------------------------------------------
# Hardcoded Realistic Financial Data for Fixed Income Analytics Platform
# ----------------------------------------------------------------------

BONDS_YIELD_CURVE_DATA: Dict[str, Dict[str, Any]] = {
    "US912828C497": {
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
            {"tenor": "3M", "rate_percent": 5.22},
            {"tenor": "6M", "rate_percent": 5.10},
            {"tenor": "1Y", "rate_percent": 4.85},
            {"tenor": "2Y", "rate_percent": 4.45},
            {"tenor": "5Y", "rate_percent": 4.20},
            {"tenor": "10Y", "rate_percent": 4.285},
            {"tenor": "30Y", "rate_percent": 4.52}
        ]
    },
    "US912810TD00": {
        "isin": "US912810TD00",
        "bond_name": "US Treasury N/B 3.875% 2029",
        "currency": "USD",
        "as_of_date": "2026-08-17",
        "yield_to_maturity_percent": 4.150,
        "modified_duration": 4.35,
        "macaulay_duration": 4.44,
        "convexity": 22.80,
        "benchmark_spread_bps": 8.0,
        "yield_curve_points": [
            {"tenor": "3M", "rate_percent": 5.22},
            {"tenor": "6M", "rate_percent": 5.10},
            {"tenor": "1Y", "rate_percent": 4.85},
            {"tenor": "2Y", "rate_percent": 4.45},
            {"tenor": "5Y", "rate_percent": 4.150},
            {"tenor": "10Y", "rate_percent": 4.285},
            {"tenor": "30Y", "rate_percent": 4.52}
        ]
    },
    "GB00BNNGP668": {
        "isin": "GB00BNNGP668",
        "bond_name": "UK Treasury Gilt 3.75% 2038",
        "currency": "GBP",
        "as_of_date": "2026-08-17",
        "yield_to_maturity_percent": 4.620,
        "modified_duration": 9.85,
        "macaulay_duration": 10.07,
        "convexity": 118.30,
        "benchmark_spread_bps": 32.1,
        "yield_curve_points": [
            {"tenor": "1Y", "rate_percent": 4.90},
            {"tenor": "5Y", "rate_percent": 4.40},
            {"tenor": "10Y", "rate_percent": 4.55},
            {"tenor": "15Y", "rate_percent": 4.620},
            {"tenor": "30Y", "rate_percent": 4.80}
        ]
    }
}


COMPUTE_JOBS_STORE: Dict[str, Dict[str, Any]] = {
    "job-analytics-98421": {
        "job_id": "job-analytics-98421",
        "portfolio_id": "PORT-FI-9902",
        "status": "COMPLETED",
        "created_at": "2026-08-17T12:38:00Z",
        "completed_at": "2026-08-17T12:38:02Z",
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
            "gpu_acceleration": True,
            "memory_peak_mb": 4096,
            "node_id": "grid-node-ny4-88.analytics.internal"
        }
    },
    "job-analytics-98422": {
        "job_id": "job-analytics-98422",
        "portfolio_id": "PORT-GLOBAL-CORP-401",
        "status": "COMPLETED",
        "created_at": "2026-08-17T12:39:10Z",
        "completed_at": "2026-08-17T12:39:12Z",
        "execution_time_seconds": 2.10,
        "metrics": {
            "value_at_risk_99_usd": 5100000.0,
            "expected_shortfall_usd": 6400000.0,
            "dv01_usd": 92000.0,
            "net_portfolio_value_usd": 320000000.0
        },
        "stress_test_loss_usd": {
            "rates_up_100bps": -8200000.0,
            "rates_down_100bps": 8600000.0,
            "credit_spread_widening_50bps": -4300000.0
        },
        "compute_grid_stats": {
            "cpu_cores_utilized": 128,
            "gpu_acceleration": True,
            "memory_peak_mb": 8192,
            "node_id": "grid-node-ldn1-12.analytics.internal"
        }
    }
}


HEALTH_TELEMETRY_DATA: Dict[str, Any] = {
    "status": "HEALTHY",
    "service": "fixed-income-analytics-compute-platform",
    "version": "1.0.0",
    "cpp_analytics_engine_version": "v4.2.1-native",
    "cluster_nodes_active": 128,
    "memory_usage_percent": 42.5,
    "queue_depth": 3,
    "uptime_seconds": 864000
}
