from pika import ConnectionParameters, BlockingConnection
connection_params = ConnectionParameters(
    host = "192.168.101.10",
    port = 31833,
)


def process_message(ch, method, properties, body):
    print(f"Получено сообщение: {body.decode()}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    with BlockingConnection(connection_params) as conn:
        with conn.channel() as ch:
            ch.queue_declare(queue="messages")
            ch.basic_consume(
                queue="messages",
                on_message_callback=process_message,
            )
            print("Жду сообщений")
            ch.start_consuming()


main()