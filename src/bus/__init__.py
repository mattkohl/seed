from kafka import KafkaProducer


class Producer:

    @staticmethod
    def publish_message(producer: KafkaProducer, topic_name: str, key: str, value: str) -> None:
        try:
            key_bytes = bytes(key, encoding='utf-8')
            value_bytes = bytes(value, encoding='utf-8')
            producer.send(topic_name, key=key_bytes, value=value_bytes)
            producer.flush()
            print('Message published successfully.')
        except Exception as ex:
            print('Exception in publishing message')
            print(str(ex))

    @staticmethod
    def connect():
        producer = None
        try:
            producer = KafkaProducer(bootstrap_servers=['localhost:9092'], api_version=(0, 10))
        except Exception as ex:
            print('Exception while connecting Kafka')
            print(str(ex))
        finally:
            return producer
