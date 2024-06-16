from __future__ import annotations

import abc
import asyncio
import decimal
import uuid

import pydantic

from typing import TypeVar
from .client_messages import (
    PlaceOrder,
    SubscribeMarketData,
    UnsubscribeMarketData
)
from .server_messages import (
    ErrorInfo,
    ExecutionReport,
    MarketDataUpdate,
    SuccessInfo
)
from server.enums import ClientMessageType, ServerMessageType


def snake_to_camel(snake_str: str) -> str:
    if snake_str == "":
        return snake_str

    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


class Envelope(pydantic.BaseModel, abc.ABC):
    class Config:
        extra = pydantic.Extra.forbid
        alias_generator = snake_to_camel
        allow_population_by_field_name = True

    message_type: ClientMessageType | ServerMessageType
    message: dict

    @abc.abstractmethod
    def get_parsed_message(self):
        pass


class Message(pydantic.BaseModel, abc.ABC):
    class Config:
        frozen = True
        extra = pydantic.Extra.forbid

    @abc.abstractmethod
    def get_type(self):
        pass


class ClientEnvelope(Envelope):
    def get_parsed_message(self):
        return _CLIENT_MESSAGE_TYPE_BY_CLASS.inverse[self.message_type].parse_obj(self.message)


class ServerEnvelope(Envelope):
    def get_parsed_message(self):
        return _SERVER_MESSAGE_TYPE_BY_CLASS.inverse[self.message_type].parse_obj(self.message)


class ClientMessage(Message):
    def get_type(self):
        return _CLIENT_MESSAGE_TYPE_BY_CLASS[self.__class__]


class ServerMessage(Message):
    def get_type(self):
        return _SERVER_MESSAGE_TYPE_BY_CLASS[self.__class__]


class Connection(pydantic.BaseModel):
    class Config:
        arbitrary_types_allowed = True

    subscriptions: list[asyncio.Task] = []
    orders: dict[uuid.UUID, dict] = {}


class Quote(pydantic.BaseModel):
    bid: decimal.Decimal
    offer: decimal.Decimal
    min_amount: decimal.Decimal
    max_amount: decimal.Decimal


MessageT = TypeVar('MessageT', bound=Message)


_CLIENT_MESSAGE_TYPE_BY_CLASS = dict.bidict({
    SubscribeMarketData: ClientMessageType.subscribe_market_data,
    UnsubscribeMarketData: ClientMessageType.unsubscribe_market_data,
    PlaceOrder: ClientMessageType.place_order,
})

_SERVER_MESSAGE_TYPE_BY_CLASS = dict.bidict({
    SuccessInfo: ServerMessageType.success,
    ErrorInfo: ServerMessageType.error,
    ExecutionReport: ServerMessageType.execution_report,
    MarketDataUpdate: ServerMessageType.market_data_update,
})
