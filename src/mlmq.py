from fastapi import FastAPI
import uvicorn
import pika
import config as cfg
import requests
import json

app = FastAPI()

def get_model_pred(sentence):
    model_url = cfg.model_url
    pred = requests.get(model_url+sentence).json()
    return pred

class Consumer:
    def __init__(self):
        self.__url = cfg.url
        self.__port = cfg.port
        self.__vhost = cfg.source_vhost
        self.__cred = pika.PlainCredentials(cfg.cred_id, cfg.cred_pw)
        self.__queue = cfg.source_queue
        return

    def on_message(channel, method_frame, header_frame, body):
        print('Received %s' % body)
        return

    def model_inference(channel, method_frame, header_frame, body):
        message = json.loads(body)
        print('message:',message)
        print('model input :',message['text'])
        pred = get_model_pred(message['text'])
        message['pred'] = pred
        message = json.dumps(message)
        print(message)
        publisher = Publisher()
        publisher.main(message)
        return

    def main(self):
        conn = pika.BlockingConnection(pika.ConnectionParameters(self.__url, self.__port, self.__vhost, self.__cred))
        chan = conn.channel()
        chan.basic_consume(
            queue = self.__queue,
            on_message_callback = Consumer.model_inference,
            auto_ack = True
        )
        print('Consumer is starting...')
        chan.start_consuming()
        return

class Publisher:
    def __init__(self):
        self.__url = cfg.url
        self.__port = cfg.port
        self.__vhost = cfg.dest_vhost
        self.__cred = pika.PlainCredentials(cfg.cred_id,cfg.cred_pw)
        self.__queue = cfg.dest_queue
        return

    def main(self,message):
        conn = pika.BlockingConnection(pika.ConnectionParameters(self.__url, self.__port, self.__vhost, self.__cred))
        chan = conn.channel()
        chan.basic_publish(
            exchange = '',
            routing_key = self.__queue,
            body = message
        )
        conn.close()
        return


#
# consumer = Consumer()
# consumer.main()

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

#@app.on_event("startup")
@app.get("/con")
def startup():
    consumer = Consumer()
    consumer.main()

    return

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081)