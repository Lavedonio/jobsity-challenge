import re
import sys
import json
import uuid
import hashlib
from contextlib import closing
from datetime import datetime

import psycopg2
from confluent_kafka import Consumer, KafkaException
from clickhouse_driver import Client


KAFKA_CONF = {
    "bootstrap.servers": "localhost:9092"
}
KAFKA_RAW_TRIPS_TOPIC = "raw_trips_data"


def retrieve_credentials(key: str) -> dict:
    """
        Retrieve the credentials needed in a dict format
        based on the provided :key.
    """
    with open("credentials.json") as f:
        creds = json.load(f)

    try:
        return creds[key]
    except KeyError as e:
        message = "Unable to retrive the credentials"
        raise ValueError(message) from e


def create_hash_md5(value: str) -> str:
    """
        Create a hash based on a given :value
        based on the md5 algorithm.
    """
    md5_hash = hashlib.md5()
    md5_hash.update(value.encode('utf-8'))
    return str(md5_hash.hexdigest())


def parse_raw_data(data: str, hash_value: str) -> dict:
    """
        Parse the raw data received from Kafka in order for it
        to meet the final database column schemas.
    """
    data_dict = json.loads(data)

    # Creating an uuid that will be shared by both databases
    data_dict["uuid"] = uuid.uuid4()

    # Adding hash_value to dict
    data_dict["hash_value"] = hash_value

    # Creating a year_week column in order to help the
    # data-viz parsing process
    date_time = datetime \
        .strptime(data_dict["date_time"], "%Y-%m-%d %H:%M:%S%z")
    data_dict["year_week"] = date_time.strftime("%Y_%V")

    # Removing timezone from date_time column
    data_dict["date_time"] = str(date_time.replace(tzinfo=None))

    # Parsing latitude and longitude from geo-location coordenates
    geo_coordenates = ["origin", "destination"]
    for geo in geo_coordenates:
        regex = r"[-+]?\d{1,3}.\d{1,15}"
        lat, long = re.findall(regex, data_dict[f'{geo}_coord'])

        data_dict[f'{geo}_latitude'] = lat
        data_dict[f'{geo}_longitude'] = long

        del data_dict[f'{geo}_coord']

    return data_dict


def update_metabase_clickhouse(data_dict: dict) -> None:
    """
        Runs the entire process to insert or update the data on
        the Metabase ClickHouse database.
    """
    print("Preparing SQL statements...")
    clickhouse_delete_old = """ALTER TABLE jobsity_challenge.trips DELETE WHERE hash_value = '{hash_value}'""".format(
        **data_dict
    )
    clickhouse_insert = """INSERT INTO jobsity_challenge.trips (*) VALUES ('{uuid}', '{hash_value}', '{region}', {origin_latitude}, {origin_longitude}, {destination_latitude}, {destination_longitude}, '{date_time}', '{datasource}', '{year_week}')""".format(
        **data_dict
    )

    print("Retrieving credentials...")
    creds = retrieve_credentials("ClickHouse_Metabase")
    print("Instantiating ClickHouse client...")
    client = Client(**creds)
    try:
        print("Executing first command...")
        client.execute(clickhouse_delete_old)
        print("Executing second command...")
        client.execute(clickhouse_insert)
    except Exception as e:
        raise e
    finally:
        client.disconnect()


def update_metabase_postgres(data_dict: dict) -> None:
    """
        Runs the entire process to insert or update the data on
        the Metabase Postgres database.
    """
    print("Preparing SQL statements...")
    postgres_delete_old = """DELETE FROM jobsity_challenge.trips WHERE hash_value = '{hash_value}';""".format(
        **data_dict
    )
    postgres_insert = """
        INSERT INTO jobsity_challenge.trips(uuid, hash_value, region, origin_latitude, origin_longitude, destination_latitude, destination_longitude, date_time, datasource)
        VALUES ('{uuid}', '{hash_value}', '{region}', {origin_latitude}, {origin_longitude}, {destination_latitude}, {destination_longitude}, '{date_time}', '{datasource}')
    """.format(
        **data_dict
    )

    print("Retrieving credentials...")
    creds = retrieve_credentials("Postgres_Metabase")
    print("Creating a connection...")
    with closing(psycopg2.connect(**creds)) as conn:
        with conn, conn.cursor() as cur:
            print("Executing first command...")
            cur.execute(postgres_delete_old)
            print("Executing second command...")
            cur.execute(postgres_insert)


def update_django_postgres(data_dict: dict) -> None:
    """
        Runs the entire process to insert or update the data on
        the Metabase Postgres database.
    """
    print("Preparing SQL statement...")
    postgres_update = """
        UPDATE kaskaskjsdfjsdf
        SET status = 'S'
        WHERE hash_value = '{hash_value}';
    """.format(
        **data_dict
    )

    print("Retrieving credentials...")
    creds = retrieve_credentials("Postgres_Django")
    print("Creating a connection...")
    with closing(psycopg2.connect(**creds)) as conn:
        with conn, conn.cursor() as cur:
            print("Executing SQL command...")
            cur.execute(postgres_update)


def process(key: str, data: str) -> None:
    """
        From the data retrieved from the Kafka Consumer,
        start processing the single datapoint and updating
        all final databases and the status from the Django API.
    """
    print("-----------------------------------")
    print(f"-- Processing message key {key} --")
    print("Creating hash from data and parsing the raw data...")
    hash_value = create_hash_md5(data)
    data_dict = parse_raw_data(data, hash_value)
    print("Data parsed.")
    print("")

    print("Starting Metabase ClickHouse update process...")
    update_metabase_clickhouse(data_dict)
    print("End of Metabase ClickHouse update process.")
    print("")

    print("Starting Metabase Postgres update process...")
    update_metabase_postgres(data_dict)
    print("End of Metabase Postgres update process.")
    print("")

    print("Starting Django Postgres update process...")
    update_django_postgres(data_dict)
    print("End of Django Postgres update process.")
    print("")

    print("Done!")
    print("")


def main():
    """
        Main Kafka process.

        Keeps looping indefinitely, consuming new messages from the
        raw_trips_data topic and processing each message.
    """
    c = Consumer(KAFKA_CONF)
    c.subscribe([KAFKA_RAW_TRIPS_TOPIC])
    while True:
        try:
            msg = c.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())
            else:
                sys.stderr.write('%% %s [%d] at offset %d with key %s:\n' %
                                 (msg.topic(), msg.partition(), msg.offset(),
                                     str(msg.key())))
                print(msg.value())

                # Get message and start processing
                unpacked_message = msg.value().decode('utf-8')
                process(str(msg.key()), unpacked_message)

        except KeyboardInterrupt:
            break

        except Exception as e:
            import traceback
            print(traceback.format_exc())
            break

        finally:
            c.close()


if __name__ == "__main__":
    main()
