import re
import json
from copy import deepcopy
from rest_framework import serializers
from .models import Trip
from .aux import create_hash_md5, kafka_produce


def kafka_callback(err, message):
    """
        Kafka Trips producer callback
    """
    if err is None:
        print(f"Message successfully produced: {message.value()}")
    else:
        print(f"Failed to produce message: {message.value()}: {err.str()}")


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ["region", "origin_coord",
                  "destination_coord", "date_time", "datasource"]

    def create(self, validated_data):
        kafka_data = deepcopy(validated_data)
        kafka_data['date_time'] = str(kafka_data['date_time'])

        kafka_value = json.dumps(kafka_data)
        kafka_key = create_hash_md5(kafka_value)

        kafka_produce(kafka_key, kafka_data)

        validated_data['hash_value'] = kafka_key
        return super().create(validated_data)

    def __coordenates_are_valid(self, value):
        main_format = re.compile(
            r"POINT \(\d{1,3}.\d{1,15} \d{1,3}.\d{1,15}\)")

        if main_format.search(value):
            lat, long = re.findall(r"[-+]?\d{1,3}.\d{1,15}", value)

            try:
                lat = float(lat)
                long = float(long)
            except ValueError:
                return False

            if -90 <= lat <= 90 and -180 <= long <= 180:
                return True
        return False

    def validate_origin_coord(self, value: str):
        """Validate input origin coordenates"""

        if self.__coordenates_are_valid(value):
            return value.strip()
        else:
            raise serializers.ValidationError("Invalid Origin Coordenates")

    def validate_destination_coord(self, value: str):
        """Validate input destination coordenates"""

        if self.__coordenates_are_valid(value):
            return value.strip()
        else:
            raise serializers.ValidationError(
                "Invalid Destination Coordenates")
