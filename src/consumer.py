import pika
import json
from publisher import Publisher
from modelAPI import ModelAPI
import config as cfg


modelAPI = ModelAPI()

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
        pred = modelAPI.get_model_pred(message['text'])
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