"""
Prometheus metrics instrumentation for FastAPI application.

This module defines all custom metrics for monitoring the accident prediction API.
It includes counters for operations, gauges for current state, histograms for distributions,
and error tracking with labels.
"""

import time
from prometheus_client import Counter, Gauge, Histogram, generate_latest
from prometheus_fastapi_instrumentator import Instrumentator, metrics
from functools import wraps

# Business Metrics - Counters for CRUD operations
predictions_total = Counter(
    'predictions_total',
    'Total number of predictions made',
    ['model_version', 'success']
)

health_checks_total = Counter(
    'health_checks_total',
    'Total number of health check requests'
)

# HTTP Errors Counter with labels
http_errors_total = Counter(
    'http_errors_total',
    'Total HTTP errors segmented by type',
    ['error_type', 'status_code']
)

# Application State Gauges
app_uptime_seconds = Gauge(
    'app_uptime_seconds',
    'Application uptime in seconds since startup'
)

active_connections = Gauge(
    'active_connections',
    'Number of active connections'
)

# Business Logic Histograms
prediction_confidence_histogram = Histogram(
    'prediction_confidence_histogram',
    'Distribution of prediction confidence scores',
    buckets=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99, 1.0]
)

age_histogram = Histogram(
    'age_histogram',
    'Distribution of user ages in predictions',
    buckets=[10, 15, 18, 25, 35, 45, 55, 65, 75, 85, 95]
)

speed_histogram = Histogram(
    'speed_histogram',
    'Distribution of speed limits in predictions',
    buckets=[10, 20, 30, 40, 50, 60, 70, 80, 90, 110, 130, 150]
)

# Database Query Performance
db_query_duration_seconds = Histogram(
    'db_query_duration_seconds',
    'Duration of database queries in seconds',
    buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
)

# Model Performance Metrics
model_prediction_duration_seconds = Histogram(
    'model_prediction_duration_seconds',
    'Time taken for model predictions in seconds',
    buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0]
)

model_accuracy_gauge = Gauge(
    'model_accuracy_gauge',
    'Current model accuracy (if available)'
)

# Initialize uptime tracking
_start_time = time.time()

def update_uptime():
    """Update the uptime gauge."""
    app_uptime_seconds.set(time.time() - _start_time)

# Decorator for timing functions
def time_metric(histogram_metric):
    """Decorator to time function execution and record in histogram."""
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                return result
            finally:
                duration = time.time() - start_time
                histogram_metric.observe(duration)
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                duration = time.time() - start_time
                histogram_metric.observe(duration)
        
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    return decorator

# Error tracking functions
def track_http_error(error_type: str, status_code: int):
    """Track HTTP errors with type and status code."""
    http_errors_total.labels(error_type=error_type, status_code=status_code).inc()

def track_prediction(success: bool, model_version: str = "1.0"):
    """Track prediction attempts and successes."""
    predictions_total.labels(model_version=model_version, success=str(success)).inc()

# Business logic tracking
def track_age(age: float):
    """Record age distribution for predictions."""
    age_histogram.observe(age)

def track_speed(speed: float):
    """Record speed distribution for predictions."""
    speed_histogram.observe(speed)

def track_confidence(confidence: float):
    """Record prediction confidence distribution."""
    prediction_confidence_histogram.observe(confidence)

# Initialize FastAPI instrumentator with minimal configuration
instrumentator = Instrumentator(
    excluded_handlers=["/metrics"],
    env_var_name="ENABLE_METRICS",
)

# Add default metrics
instrumentator.add(metrics.default())

def setup_metrics(app):
    """Setup Prometheus metrics for FastAPI application."""
    instrumentator.instrument(app).expose(app)
