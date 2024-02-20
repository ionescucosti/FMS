import time
import pika
import random
import schedule
import threading


def generate_event(vehicle_id=1, driver_id=1):
    coordinates = (random.uniform(-90, 90), random.uniform(-180, 180))
    speed = int(random.uniform(0, 120))

    event = {
        'vehicle_id': vehicle_id,
        'coordinates': coordinates,
        'speed': speed,
        'driver_id': driver_id,
        'timestamp': int(time.time())
    }

    return event


def send_to_rabbitmq(event):
    connection_params = pika.ConnectionParameters(
        host='0.0.0.0',
        port=5672,
        virtual_host='/',
        credentials=pika.PlainCredentials('guest', 'guest')
    )
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()
    channel.queue_declare(queue='gps')
    channel.basic_publish(exchange='',
                          routing_key='gps',
                          body=str(event))
    connection.close()


def main():
    event = generate_event()
    print(event)
    send_to_rabbitmq(event)


# Schedule the job every 5 seconds
schedule.every(5).seconds.do(main)


# Function to run the scheduler in a separate thread
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)


# Start the scheduler in a separate thread
scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.start()

if __name__ == '__main__':
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.run_forever()
