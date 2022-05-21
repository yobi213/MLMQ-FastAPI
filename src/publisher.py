import config as cfg
import pika

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



class Sample:
    def __init__(self):
        self.__url = cfg.url
        self.__port = cfg.port
        self.__vhost = cfg.source_vhost
        self.__cred = pika.PlainCredentials(cfg.cred_id,cfg.cred_pw)
        self.__queue = cfg.source_queue
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