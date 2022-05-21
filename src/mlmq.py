from fastapi import FastAPI
import uvicorn
import pika
import config as cfg
import requests
import json
from consumer import Consumer
from publisher import Publisher,Sample

app = FastAPI()


# RabbitMQ 연결

@app.get("/pub")
def pub():
    data = {
        "rec_id": 1,
        "name": "My Name",
        "text": "배송이 느려요"
    }
    print(data)
    print('type of data', type(data))
    message = json.dumps(data)
    print(message)
    print('type of message', type(message))

    publisher = Publisher()
    publisher.main(message)

    return

@app.get("/sample")
def sample():
    data = {
        "rec_id": 1,
        "name": "My Name",
        "text": "배송이 빨라"
    }
    print(data)
    print('type of data', type(data))
    message = json.dumps(data)
    print(message)
    print('type of message', type(message))

    publisher = Sample()
    publisher.main(message)

    return


@app.on_event("startup")
#@app.get("/con")
def startup():
    consumer = Consumer()
    consumer.main()

    return

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081)