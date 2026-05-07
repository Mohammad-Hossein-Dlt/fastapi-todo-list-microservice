from faststream import ExceptionMiddleware, StreamMessage
from faststream.rabbit import RabbitBroker, RabbitQueue, RabbitExchange, ExchangeType
from faststream.types import DecodedMessage
from src.worker.depends.rabbitmq_depend import rabbit_params
from src.infra.exceptions.exceptions import AppBaseException
from typing import Callable, Awaitable
import json

params = rabbit_params()

async def decoder(
    msg: StreamMessage,
    original_decoder: Callable[[StreamMessage], Awaitable[DecodedMessage]],
) -> DecodedMessage:
    
    try:
        body = json.loads(msg.body.decode())
    except:
        body = msg.body.decode()
        
    if isinstance(body, dict) and len(body) == 1:
        k, v = next(iter(body.items()))
        if k in body:
            msg.body = json.dumps(v).encode()

    return await original_decoder(msg)

exc_middleware = ExceptionMiddleware()
@exc_middleware.add_handler(Exception, publish=True)
def base_exc_handler(
    ex: Exception | AppBaseException,
    # message: StreamMessage = Context(),
) -> str:
        
    if isinstance(ex, AppBaseException):
        return ex.model_dump()
    
    return AppBaseException(500, "Internal server error").model_dump()


broker = RabbitBroker(
    url=params.url,
)

queue = RabbitQueue(
    name=params.queue,
    routing_key=params.routing_key,
)

exchange = RabbitExchange(
    name=params.exchange,
    type=ExchangeType.TOPIC,
)

subscriber = broker.subscriber(
    queue=queue,
    exchange=exchange,
    # decoder=decoder,
)

broker.add_middleware(
    exc_middleware,
)