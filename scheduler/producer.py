import os
import pika

def produce(body):
    rabbit_host = os.environ.get("RABBITMQ_HOST", "rabbitmq")
    rabbit_user = os.environ.get("RABBITMQ_USER", "admin")
    rabbit_pass = os.environ.get("RABBITMQ_PASS", "rabbitmq")

    credentials = pika.PlainCredentials(rabbit_user, rabbit_pass)
    parameters = pika.ConnectionParameters(host=rabbit_host, credentials=credentials)

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.exchange_declare(exchange="jobs", exchange_type="direct")
    channel.queue_declare(queue="router_jobs")
    channel.queue_bind(queue="router_jobs", exchange="jobs", routing_key="check_interfaces")

    channel.basic_publish(exchange="jobs", routing_key="check_interfaces", body=body)

    connection.close()

if __name__ == "__main__":
    produce("192.168.1.44")