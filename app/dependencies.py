from typing import TypeVar, Type, Callable
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.accessor import get_session
from app.service.orders import OrderService
from app.repository.orders import OrderRepository

T = TypeVar("T")


def get_repository(repo_class: Type[T]) -> Callable:
    def _get_repository(session: AsyncSession = Depends(get_session)) -> T:
        return repo_class(session)

    return _get_repository


def get_service(service_class: Type[T], repo_class) -> Callable:
    def _get_service(
        repository=Depends(get_repository(repo_class)),
    ) -> T:
        return service_class(repository)

    return _get_service


order_service_dependency = get_service(OrderService, OrderRepository)
