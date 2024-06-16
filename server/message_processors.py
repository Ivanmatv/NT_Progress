from __future__ import annotations

import asyncio
import decimal
import uuid

from typing import TYPE_CHECKING
from server.models import server_messages
from server.models.base import Quote
from enums import OrderStatus

if TYPE_CHECKING:
    import fastapi

    from server.models import client_messages
    from server.ntpro_server import NTProServer


async def subscribe_market_data_processor(
        server: NTProServer,
        websocket: fastapi.WebSocket,
        message: client_messages.SubscribeMarketData,
):
    from server.models import server_messages

    subscription_id = uuid.uuid4()
    connection = server.connections[websocket.client]

    async def send_quotes():
        while True:
            # Simulate sending market data updates
            await websocket.send_json(server_messages.ServerEnvelope(
                message_type=server_messages.ServerMessageT.market_data_update,
                message=server_messages.MarketDataUpdate(
                    subscription_id=subscription_id,
                    instrument=message.instrument,
                    quotes=[
                        Quote(
                            bid=decimal.Decimal('1.1000'),
                            offer=decimal.Decimal('1.2000'),
                            min_amount=decimal.Decimal('1000'),
                            max_amount=decimal.Decimal('10000'),
                        )
                    ]
                ).dict()
            ).dict())
            await asyncio.sleep(1)  # Simulate data update interval

    task = asyncio.create_task(send_quotes())
    connection.subscriptions.append(task)

    return server_messages.SuccessInfo(subscription_id=subscription_id)


async def unsubscribe_market_data_processor(
        server: NTProServer,
        websocket: fastapi.WebSocket,
        message: client_messages.UnsubscribeMarketData,
):
    connection = server.connections[websocket.client]
    for task in connection.subscriptions:
        task.cancel()

    connection.subscriptions = []

    return server_messages.SuccessInfo()


async def place_order_processor(
        server: NTProServer,
        websocket: fastapi.WebSocket,
        message: client_messages.PlaceOrder,
):
    from server.models import server_messages

    order_id = uuid.uuid4()
    connection = server.connections[websocket.client]

    order = {
        "instrument": message.instrument,
        "side": message.side,
        "amount": message.amount,
        "price": message.price,
        "status": OrderStatus.active,
    }

    connection.orders[order_id] = order

    # Simulate order execution
    await asyncio.sleep(1)
    order["status"] = OrderStatus.filled

    return server_messages.ExecutionReport(order_id=order_id, order_status=order["status"])
