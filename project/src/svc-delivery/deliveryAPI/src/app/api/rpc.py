from aio_pika import connect_robust, IncomingMessage, Message
from api import delivery
from api.models import  DeliverySchema
import json
import os


RABBITMQ_HOST = "192.168.101.10"
RABBITMQ_PORT = 31833

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT"))


RABBITMQ_PUBLISH_ORDER_QUEUE = 'orderChangeState'
RABBITMQ_CONSUME_RESERVE_DELIVERY_QUEUE = 'deliveryReserve' 


async def callback( message: IncomingMessage):
    async with message.process():
      
        print(f" Received message: {message.body.decode()}")

        try:
            msg = json.loads(message.body.decode())
        except Exception as e:
            print('MESSAGE PARSE ERROR: ' + str(e))

        # Пытаемся забронировать время доставки
        res = await delivery.reserve_delivery(DeliverySchema(id_order= msg['order_id'], dtime=msg['dtime']) )
        print(res)
        if 'error' in res:    delivery_status = 'Delivery Error'
        else:                 delivery_status = 'Delivery Succes'
            
        await publish(RABBITMQ_PUBLISH_ORDER_QUEUE ,  json.dumps({"order_id":msg['order_id'],'status': delivery_status}))
               
                            

async def consume():
    connection = await connect_robust(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)
    queue = await channel.declare_queue(RABBITMQ_CONSUME_RESERVE_DELIVERY_QUEUE)
    await queue.consume(callback)



async def publish(target_queue, message):
    print("MESSAGE FOR PUBLISH", message)
    connection = await connect_robust(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
    channel = await connection.channel()
    queue = await channel.declare_queue(target_queue)
    await channel.default_exchange.publish(Message(body=message.encode()),
                                                     routing_key=target_queue)



 
  