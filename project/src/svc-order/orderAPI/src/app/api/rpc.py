from aio_pika import connect_robust, IncomingMessage, Message
from api import order, db
import json
import os
import requests




NOTIFY_URL  = "http://arch.homework:31599"
RABBITMQ_HOST = "192.168.101.10"
RABBITMQ_PORT = 31833


NOTIFY_URL  = os.getenv("NOTIFY_URL")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT"))


RABBITMQ_PUB_WITHDRAW_MONEY_QUEUE       = 'withdrawMoney'
RABBITMQ_PUB_REFUND_MONEY_QUEUE         = 'refundMoney'
RABBITMQ_PUB_RESERVE_STOCK_QUEUE        = 'stockReserve'
RABBITMQ_PUB_REFUND_STOCK_QUEUE         = 'stockRefund'
RABBITMQ_PUB_RESERVE_DELIVERY_QUEUE     = 'deliveryReserve'
RABBITMQ_CONSUME_QUEUE                  = 'orderChangeState' 


async def callback( message: IncomingMessage):
    async with message.process():
        print(f"Received message: {message.body.decode()}")
        try:
            msg = json.loads(message.body.decode())
            if type(msg) != dict or ("order_id" not in msg.keys()) or ("status" not in msg.keys()): 
                raise Exception('message is not valid JSON')
        except Exception as e:
            print('MESSAGE PARSE ERROR: ' + str(e)) 
            return

        order_data = await db.get_order(msg['order_id']) 
        # Обработка входящего сообщения
        if msg['status'] in ['Account not found', 'Not enough money']: # денег нет. Конец саги
            
            print(order_data['id_product'], order_data['quantity'])
            r = requests.post(f"{NOTIFY_URL}/notify", json={"login": order_data['login']
                                                            , 'e_mail': order_data['e_mail']
                                                            , 'text' : "Недостаточно средств для оплаты товара"})
        

        elif msg['status'] == 'Payment Succes': # платёж прошёл, резервируем товар
            print('Payment success. Go to stock')
           
            print(order_data['id_product'], order_data['quantity'])
            r = requests.post(f"{NOTIFY_URL}/notify", json={"login": order_data['login']
                                                            , 'e_mail': order_data['e_mail']
                                                            , 'text' : "Заказ успешно оплачен!"})
            await publish(RABBITMQ_PUB_RESERVE_STOCK_QUEUE, json.dumps({"id_product" : order_data['id_product'], "quantity" : order_data['quantity'], "order_id" : msg['order_id']}))


        elif msg['status'] == 'Not enough position quantity': # недостаточно товара на складе
            print('Возврат денег')
      
            print(order_data['login'], order_data['amount'])
            r = requests.post(f"{NOTIFY_URL}/notify", json={"login": order_data['login']
                                                            ,'e_mail': order_data['e_mail']
                                                            , 'text' : "Не удалось зарезервировать товар на складе. Деньги будут возвращены на Ваш счёт"})
            await publish(RABBITMQ_PUB_REFUND_MONEY_QUEUE, json.dumps({"order_id" : msg['order_id'],  "login" : order_data['login'],  "amount" : order_data['amount'] }))

    
        elif msg['status'] == 'Reserve Stock Succes': # товар зарезервирован, бронируем доставку
          
            r = requests.post(f"{NOTIFY_URL}/notify", json={"login": order_data['login']
                                                            ,'e_mail': order_data['e_mail']
                                                            , 'text' : "Товар успешно зарезервирован на складе"})
            await publish(RABBITMQ_PUB_RESERVE_DELIVERY_QUEUE, json.dumps({"order_id" : msg['order_id'],  "dtime" : order_data['dtime']}, default=str))


        elif msg['status'] == "Delivery Error": # доставку не удалось забронировать
            
            print(order_data['login'], order_data['amount'])

            r = requests.post(f"{NOTIFY_URL}/notify", json={"login": order_data['login']
                                                            ,'e_mail': order_data['e_mail']
                                                            , 'text' : "Не удалось зарезервировать курьера. Деньги будут возвращены на Ваш счёт"})
            print('Возврат денег')
            await publish(RABBITMQ_PUB_REFUND_MONEY_QUEUE, json.dumps({"order_id" : msg['order_id'],  "login" : order_data['login'],  "amount" : order_data['amount'] }))
            print('Возврат товара')
            await publish(RABBITMQ_PUB_REFUND_STOCK_QUEUE, json.dumps({"id_product" : order_data['id_product'], "quantity" : order_data['quantity'], "order_id" : msg['order_id']}))


        elif msg['status'] == "Delivery Succes": # Всё круто!!!!

            r = requests.post(f"{NOTIFY_URL}/notify", json={"login": order_data['login']
                                                            ,'e_mail': order_data['e_mail']
                                                            , 'text' : "Заказ успешно оформлен! Спасибо, что Вы с нами!"})
        

        await order.set_order_status(msg['order_id'], msg['status'])


async def consume():
    connection = await connect_robust(host=RABBITMQ_HOST, port=RABBITMQ_PORT) 
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)
    queue = await channel.declare_queue(RABBITMQ_CONSUME_QUEUE)
    await queue.consume(callback)


async def publish(queue_name, message):
    print("MESSAGE FOR PUBLISH", message)
    connection = await connect_robust(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
    channel = await connection.channel()
    queue = await channel.declare_queue(queue_name)
    await channel.default_exchange.publish(Message(body=message.encode()),
                                                     routing_key=queue_name)

