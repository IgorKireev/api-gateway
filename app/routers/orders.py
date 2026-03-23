from typing import Annotated

from fastapi import APIRouter, Depends

from app.schemas.request_schema import OrderRequestSchema
from app.service.orders import OrderService
from app.dependencies import order_service_dependency


router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)


@router.get("/orders")
async def get_orders(
    order_service: Annotated[OrderService, Depends(order_service_dependency)],
):
    return await order_service.get_orders()


@router.post("/")
async def create_order(
    request: OrderRequestSchema,
    order_service: Annotated[OrderService, Depends(order_service_dependency)],
):
    return await order_service.create(request)
