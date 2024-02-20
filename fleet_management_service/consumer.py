import ast
import pika
import requests


async def consumer():
    connection_params = pika.ConnectionParameters(
        host='0.0.0.0',
        port=5672,
        virtual_host='/',
        credentials=pika.PlainCredentials('guest', 'guest',)
    )
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()
    channel.queue_declare(queue='penalty_points')

    def callback(ch, method, properties, body):
        event = ast.literal_eval(body.decode('utf-8'))
        print(f" [x] Received {event}")

        get_response = requests.get(url=f'http://0.0.0.0:8000/drivers/{event["driver_id"]}').json()
        get_response['points'] = event["penalty_points"]
        post_response = requests.put(url=f'http://0.0.0.0:8000/drivers/', json=get_response)
        print(f'Updated: {post_response.json()["fullName"]}')

    channel.basic_consume(queue='penalty_points', on_message_callback=callback, auto_ack=True)

    print(' [*] fleet_management_service started. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(consumer())
    loop.run_forever()
