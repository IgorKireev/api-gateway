from collections.abc import Sequence
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from app.models.orders import Order, ShoppingAddress, Customer, Item


class OrderRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_orders(self) -> Sequence[Order]:
        orders = await self.session.execute(select(Order))
        return orders.scalars().all()

    async def get_order(self, order_id: uuid.UUID) -> Order | None:
        query = select(Order).filter(Order.order_id == order_id)
        order = await self.session.execute(query)
        return order.scalars().one_or_none()

    async def create_entity(
        self,
        entity: Order | ShoppingAddress | Customer | Item,
    ) -> Order | ShoppingAddress | Customer | Item:
        self.session.add(entity)
        await self.session.flush()
        await self.session.refresh(entity)
        return entity

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
