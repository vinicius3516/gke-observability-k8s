from datetime import datetime
from typing import Dict, List

from fastapi import FastAPI, Request, Response, status
from fastapi.responses import PlainTextResponse
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest, REGISTRY

from .models import HealthResponse, OrderIn, OrderOut
from .metrics import (
    RequestTimer,
    ORDERS_CREATED_TOTAL,
    ORDERS_COMPLETED_TOTAL,
    ORDERS_IN_PROGRESS,
    ORDERS_VALUE_SUM,
)

app = FastAPI(title="Observability Training App", version="1.0.0")

# "Banco" em memória para fins de treino
ORDERS: Dict[int, OrderOut] = {}
_next_id = 1


def _next_order_id() -> int:
    global _next_id
    oid = _next_id
    _next_id += 1
    return oid


def _route_from_request(request: Request) -> str:
    # tenta obter path parametrizado (ex.: /order/{id})
    route = getattr(request.scope.get("route"), "path", None)
    return route or request.url.path


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    method = request.method
    route = _route_from_request(request)

    with RequestTimer(method=method, route=route) as rt:
        response: Response = await call_next(request)
        rt.set_status(response.status_code)
        return response


@app.get("/health", response_model=HealthResponse, tags=["infra"])
def health():
    return HealthResponse(status="ok", timestamp=datetime.utcnow())


@app.get("/metrics", response_class=PlainTextResponse, include_in_schema=False)
def metrics():
    # Exposição das métricas no formato Prometheus
    data = generate_latest(REGISTRY)
    return PlainTextResponse(content=data.decode("utf-8"), media_type=CONTENT_TYPE_LATEST)


@app.post("/order", response_model=OrderOut, status_code=status.HTTP_201_CREATED, tags=["orders"])
def create_order(payload: OrderIn):
    """Cria um pedido e atualiza métricas de negócio."""
    oid = _next_order_id()
    order = OrderOut(
        id=oid,
        created_at=datetime.utcnow(),
        items=payload.items,
        total_amount=payload.total_amount,
        status="created",
    )
    ORDERS[oid] = order

    # Métricas de negócio
    ORDERS_CREATED_TOTAL.inc()
    ORDERS_IN_PROGRESS.inc()
    ORDERS_VALUE_SUM.inc(payload.total_amount)

    return order


@app.get("/orders", response_model=List[OrderOut], tags=["orders"])
def list_orders():
    return list(ORDERS.values())


@app.post("/order/{order_id}/complete", response_model=OrderOut, tags=["orders"])
def complete_order(order_id: int):
    order = ORDERS.get(order_id)
    if not order:
        # 404 também será contabilizado pelo middleware
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status != "completed":
        order.status = "completed"
        ORDERS_COMPLETED_TOTAL.inc()
        ORDERS_IN_PROGRESS.dec()

    return order

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
