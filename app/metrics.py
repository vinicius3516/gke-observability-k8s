import time
from typing import Optional

from prometheus_client import (
    Counter,
    Gauge,
    Histogram,
)

# -----------------------------
# Métricas HTTP
# -----------------------------
HTTP_REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "Total de requisições HTTP",
    ["method", "route", "status"],
)

HTTP_REQUEST_DURATION_SECONDS = Histogram(
    "http_request_duration_seconds",
    "Duração das requisições HTTP em segundos",
    ["method", "route", "status"],
    # buckets razoáveis para APIs (ajuste conforme necessidade)
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2, 5, 10),
)

HTTP_IN_PROGRESS = Gauge(
    "http_requests_in_progress",
    "Requisições HTTP em andamento",
    ["method", "route"],
)

# -----------------------------
# Métricas de Negócio
# -----------------------------
ORDERS_CREATED_TOTAL = Counter(
    "orders_created_total",
    "Total de pedidos criados",
)

ORDERS_COMPLETED_TOTAL = Counter(
    "orders_completed_total",
    "Total de pedidos concluídos",
)

ORDERS_IN_PROGRESS = Gauge(
    "orders_in_progress",
    "Pedidos em progresso (não concluídos)",
)

# (Opcional) Valor agregado de pedidos
ORDERS_VALUE_SUM = Counter(
    "orders_value_sum",
    "Soma dos valores (total_amount) dos pedidos criados",
)

# -----------------------------
# Helpers
# -----------------------------
class RequestTimer:
    """Context manager para medir duração e registrar métricas HTTP."""
    def __init__(self, method: str, route: str):
        self.method = method
        self.route = route
        self.start = 0.0
        self.status = "500"

    def __enter__(self):
        HTTP_IN_PROGRESS.labels(self.method, self.route).inc()
        self.start = time.perf_counter()
        return self

    def set_status(self, status_code: int):
        self.status = str(status_code)

    def __exit__(self, exc_type, exc, tb):
        duration = time.perf_counter() - self.start
        HTTP_IN_PROGRESS.labels(self.method, self.route).dec()
        HTTP_REQUESTS_TOTAL.labels(self.method, self.route, self.status).inc()
        HTTP_REQUEST_DURATION_SECONDS.labels(self.method, self.route, self.status).observe(duration)
