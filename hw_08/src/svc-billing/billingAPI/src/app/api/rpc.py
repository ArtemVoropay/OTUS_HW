from aio_pika import connect_robust, IncomingMessage, Message
from api import billing
from api.models import  RefillSchema
import json
import os

RABBITMQ_HOST = "192.168.101.10"
RABBITMQ_PORT = 31833

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT"))


RABBITMQ_PUBLISH_ORDER_QUEUE = 'orderChangeState'
RABBITMQ_CONSUME_WITHDRAW_QUEUE = 'withdrawMoney' 
RABBITMQ_CONSUME_REFUND_QUEUE = 'refundMoney'

async def callback( message: IncomingMessage):
    async with message.process():
        print(f"Routing Key: {message.routing_key}.  Received message: {message.body.decode()}")
        
        try:
            msg = json.loads(message.body.decode())
        except Exception as e:
            print('MESSAGE PARSE ERROR: ' + str(e))

        if message.routing_key == RABBITMQ_CONSUME_WITHDRAW_QUEUE:  # Оплата заказ
            # Пытаемся списать деньги со счёта
            res = await billing.withdraw(RefillSchema(login= msg['login'],balance=msg['amount']) )
            print(res)
            if 'error' in res:    payment_status = res['error']
            else:                 payment_status = 'Payment Succes'
                
            await publish(RABBITMQ_PUBLISH_ORDER_QUEUE ,  json.dumps({"order_id":msg['order_id'],'status': payment_status}))


        elif message.routing_key == RABBITMQ_CONSUME_REFUND_QUEUE:  # Возврат средств
            res = await billing.refill(RefillSchema(login= msg['login'],balance=msg['amount']) )
            


async def consume():
    connection = await connect_robust(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)
    queue = await channel.declare_queue(RABBITMQ_CONSUME_WITHDRAW_QUEUE)
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



 
  