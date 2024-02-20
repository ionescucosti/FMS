import ast
import pika
import json


def apply_penalty_points(event):
    speed = event.get('speed', 0)
    penalty_points = 0

    if speed > 60:
        penalty_points += (speed - 60)
    if speed > 80:
        penalty_points += 2 * (speed - 80)
    if speed > 100:
        penalty_points += 5 * (speed - 100)

    return penalty_points


def consume_events():
    connection_params = pika.ConnectionParameters(
        host='0.0.0.0',
        port=5672,
        virtual_host='/',
        credentials=pika.PlainCredentials('guest', 'guest')
    )
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()
    channel.queue_declare(queue='gps')
    channel.queue_declare(queue='penalty_points')

    def callback(ch, method, properties, body):
        event = ast.literal_eval(body.decode('utf-8'))
        penalty_points = apply_penalty_points(event)
        print(penalty_points)
        # Emit penalty points to Fleet Management Service
        channel.basic_publish(exchange='',
                              routing_key='penalty_points',
                              body=json.dumps({
                                                  'driver_id': event['driver_id'],
                                                  'penalty_points': penalty_points
                                              }))

    channel.basic_consume(queue='gps', on_message_callback=callback, auto_ack=True)

    print(" [*] Waiting for events. To exit press CTRL+C")
    channel.start_consuming()


def main():
    consume_events()
    return {"message": "Consuming events and emitting penalty points"}


if __name__ == '__main__':
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.run_forever()

