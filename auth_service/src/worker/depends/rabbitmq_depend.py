from src.infra.context.app_context import AppContext
from src.infra.schemas.broker.rabbitmq_params import RabbitParams
from faststream.rabbit import RabbitQueue, RabbitExchange, ExchangeType, RabbitMessage
from functools import partial

def rabbit_params() -> RabbitParams:
    return AppContext.broker_params

def target_queue(routing_key: str):
    return RabbitQueue(name=AppContext.broker_params.queue, routing_key=routing_key)

def target_exchange() -> RabbitExchange:
    return RabbitExchange(name=AppContext.broker_params.exchange, type=ExchangeType.TOPIC)

def target_routing_key(routing_key: str):
    def check(msg: RabbitMessage):
        return routing_key == msg.raw_message.routing_key
    
    return partial(check)