from aio_pika import connect_robust, IncomingMessage, Message
# from api.models import OrderSchema
from api import stock, db
from api.models import  StockSchema, StockMoveSchema
import json
import os


RABBITMQ_HOST = "192.168.101.10"
RABBITMQ_PORT = 31833

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT"))


RABBITMQ_PUBLISH_ORDER_QUEUE = 'orderChangeState'
RABBITMQ_CONSUME_RESERVE_QUEUE = 'stockReserve' 
RABBITMQ_CONSUME_REFUND_QUEUE = 'stockRefund'


async def callback( message: IncomingMessage):
    async with message.process():
        print(f"Routing Key: {message.routing_key}.  Received message: {message.body.decode()}")

        msg = json.loads(message.body.decode())

        if message.routing_key == RABBITMQ_CONSUME_RESERVE_QUEUE:  # Резервируем товар
            try:
                res = await stock.reserve(StockMoveSchema(id= msg['id_product'], quantity=msg['quantity'], id_order=msg['order_id']) )
                print(res)
                if 'error' in res:
                    reserve_status = res['error']
                else:
                    reserve_status = 'Reserve Stock Succes'
                    
                await publish(RABBITMQ_PUBLISH_ORDER_QUEUE , json.dumps({"order_id":msg['order_id'], 'status': reserve_status}))
                
            except Exception as e:
                print('MESSAGE PARSE ERROR: ' + str(e))
        elif message.routing_key == RABBITMQ_CONSUME_REFUND_QUEUE:
            print("ВОЗВРАТ ТОВАРА НА СКЛАД")
            await stock.refill(StockMoveSchema(id= msg['id_product'], quantity=msg['quantity'], id_order=msg['order_id']))


async def consume():
    connection = await connect_robust(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)

    queue = await channel.declare_queue(RABBITMQ_CONSUME_RESERVE_QUEUE)
    await queue.consume(callback)

    queue = await channel.declare_queue(RABBITMQ_CONSUME_REFUND_QUEUE)
    await queue.consume(callback)


async def publish(target_queue, message):
    print("MESSAGE FOR PUBLISH", message)
    connection = await connect_robust(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
    channel = await connection.channel()
    queue = await channel.declare_queue(target_queue)
    await channel.default_exchange.publish(Message(body=message.encode()),
                                                     routing_key=target_queue)



 
  