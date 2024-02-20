from fastapi import FastAPI

import pika

app = FastAPI()


@app.post("/send_gps_message")
async def send_gps_message():
    # Connect to RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # Declare a queue named 'gps'
    channel.queue_declare(queue='gps')

    # Message to be sent
    message = 'Event'

    # Publish the message to the 'gps' queue
    channel.basic_publish(exchange='', routing_key='gps', body=message)

    # Close the connection
    connection.close()

    return {"message": f"GPS message sent: {message}"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001)