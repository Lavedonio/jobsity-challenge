import json
import hashlib
from django.conf import settings
from confluent_kafka import Producer


def create_hash_md5(value: str) -> str:
    """
        Create a hash based on a given :value
        based on the md5 algorithm.
    """
    md5_hash = hashlib.md5()
    md5_hash.update(value.encode('utf-8'))
    return str(md5_hash.hexdigest())


def kafka_callback(err, message):
    """
        Kafka Trips producer callback
    """
    if err is None:
        print(f"Message successfully produced: {message.value()}")
    else:
        print(f"Failed to produce message: {message.value()}: {err.str()}")


def kafka_produce(kafka_key: str, kafka_value: dict) -> None:
    """
        Wrapper for the kafka producer
    """
    kafka_value = json.dumps(kafka_value)

    producer = Producer(settings.KAFKA_CONF)
    producer.produce(
        settings.KAFKA_RAW_TRIPS_TOPIC,
        key=kafka_key,
        value=kafka_value,
        on_delivery=kafka_callback
    )

    print("Flushing record...")
    producer.flush()
    print("Done")
