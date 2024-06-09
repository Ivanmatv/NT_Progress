from __future__ import annotations

import asyncio
import decimal
import uuid
from typing import TYPE_CHECKING

from . import enums

from server.models import server_messages, client_messages, base

if TYPE_CHECKING:
    import fastapi
    from server.ntpro_server import NTProServer


async def subscribe_market_data_processor(
        server: NTProServer,
        websocket: fastapi.WebSocket,
        message: client_messages.SubscribeMarketData,
):
    # Simulating market data update task
    subscription_id = uuid.uuid4()
    task = asyncio.create_task(send_market_data_updates(
        server,
        websocket,
        subscription_id,
        message.instrument)
                               )
    server.connections[websocket.client].subscriptions.append(task)

    return server_messages.SuccessInfo(subscription_id=subscription_id)


async def unsubscribe_market_data_processor(
        server: NTProServer,
        websocket: fastapi.WebSocket,
        message: client_messages.UnsubscribeMarketData,
):
    for task in server.connections[websocket.client].subscriptions:
        if not task.done() and task.get_name() == str(message.subscription_id):
            task.cancel()
            break

    return server_messages.SuccessInfo(subscription_id=message.subscription_id)


async def place_order_processor(
        server: NTProServer,
        websocket: fastapi.WebSocket,
        message: client_messages.PlaceOrder,
):
    # Simulate order placement and return execution report
    order_id = uuid.uuid4()
    order_status = enums.OrderStatus.active
    return server_messages.ExecutionReport(
        order_id=order_id,
        order_status=order_status
    )


async def send_market_data_updates(
    server: NTProServer,
    websocket: fastapi.WebSocket,
    subscription_id: uuid.UUID,
    instrument: enums.Instrument
):
    while True:
        await asyncio.sleep(1)
        quotes = [
                 base.Quote(bid=decimal.Decimal("1.1000"),
                 offer=decimal.Decimal("1.1002"),
                 min_amount=decimal.Decimal("1000"),
                 max_amount=decimal.Decimal("10000"))
        ]
        update = server_messages.MarketDataUpdate(
            subscription_id=subscription_id,
            instrument=instrument,
            quotes=quotes
        )
        await server.send(update, websocket)
