from pika import ConnectionParameters, BlockingConnection
connection_params = ConnectionParameters(
    host = "192.168.101.10",
    port = 31833,
)
def main():
    with BlockingConnection(connection_params) as conn:
        with conn.channel() as ch:
            ch.queue_declare(queue="messages")
            ch.basic_publish(
                exchange="",
                routing_key="messages",
                body="Hello RabbitMQ!"
            )
            print("Message sent")


for i in range(10):
    main()  