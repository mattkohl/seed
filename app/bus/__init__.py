import os
import threading
import multiprocessing
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError


KAFKA_HOST = os.getenv("KAFKA_HOST", "localhost")
KAFKA_PORT = os.getenv("KAFKA_PORT", "9092")


class Producer(threading.Thread):

    def __init__(self) -> None:
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()

    def stop(self) -> None:
        self.stop_event.set()

    def publish_message(self, producer: KafkaProducer, topic_name: str, key: str, value: str) -> None:
        if not self.stop_event.is_set():
            key_bytes = bytes(key, encoding='utf-8')
            value_bytes = bytes(value, encoding='utf-8')
            future = producer.send(topic_name, key=key_bytes, value=value_bytes)
            try:
                record_metadata = future.get(timeout=10)
            except KafkaError as e:
                print(e)
            else:
                print(f"{record_metadata.topic}:{record_metadata.partition}:{record_metadata.offset}")
                producer.flush()

    @staticmethod
    def connect() -> KafkaProducer:
        producer = None
        try:
            producer = KafkaProducer(bootstrap_servers=[f"{KAFKA_HOST}:{KAFKA_PORT}"], api_version=(0, 10))
        except KafkaError as ex:
            print(f"Exception while connecting Kafka Producer: {ex}")
        finally:
            return producer


class Consumer(multiprocessing.Process):

    def __init__(self, topic) -> None:
        multiprocessing.Process.__init__(self)
        self.stop_event = multiprocessing.Event()
        self.topic = topic

    def stop(self) -> None:
        self.stop_event.set()

    @property
    def queue(self) -> KafkaConsumer:
        consumer = None
        try:
            consumer = KafkaConsumer(self.topic,
                                     group_id='earliest',
                                     bootstrap_servers=[f"{KAFKA_HOST}:{KAFKA_PORT}"],
                                     api_version=(0, 10),
                                     auto_offset_reset='smallest',
                                     consumer_timeout_ms=1000)
        except Exception as ex:
            print(f"Exception while connecting Kafka Consumer {self.topic}")
            print(str(ex))
        finally:
            while not self.stop_event.is_set():
                for message in consumer:
                    if self.stop_event.is_set():
                        break
                    else:
                        yield message

            consumer.close()
