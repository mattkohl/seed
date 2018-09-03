from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError


class Producer:

    @staticmethod
    def publish_message(producer: KafkaProducer, topic_name: str, key: str, value: str) -> None:
        key_bytes = bytes(key, encoding='utf-8')
        value_bytes = bytes(value, encoding='utf-8')
        future = producer.send(topic_name, key=key_bytes, value=value_bytes)
        try:
            record_metadata = future.get(timeout=10)
            print('Message published successfully.')
        except KafkaError as e:
            print(e)
        else:
            print(record_metadata.topic)
            print(record_metadata.partition)
            print(record_metadata.offset)
            producer.flush()

    @staticmethod
    def connect() -> KafkaProducer:
        producer = None
        try:
            producer = KafkaProducer(bootstrap_servers=['localhost:9092'], api_version=(0, 10))
        except Exception as ex:
            print("Exception while connecting Kafka Producer")
            print(str(ex))
        finally:
            return producer


class Consumer:

    def __init__(self, topic) -> None:
        self.topic = topic

    @property
    def queue(self) -> KafkaConsumer:
        consumer = None
        try:
            consumer = KafkaConsumer(self.topic,
                                     group_id='earliest',
                                     bootstrap_servers=['localhost:9092'],
                                     api_version=(0, 10),
                                     consumer_timeout_ms=1000)
        except Exception as ex:
            print(f"Exception while connecting Kafka Consumer {self.topic}")
            print(str(ex))
        finally:
            return consumer
