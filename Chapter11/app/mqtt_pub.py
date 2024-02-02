#!env python3
import argparse
import csv
import logging
import sys
import time

from yaml import load, Loader
import paho.mqtt.publish as publish


config = """
tags:
    - System Setting
    - System Mode
fields:
    - Cool Set Temp (F)
    - Heat Set Temp (F)
    - Current Temp (F)
    - Outdoor Temp (F)
    - Current Humidity (%RH)
    - Wind Speed (km/h)
"""


class CSVReader:
    def __init__(self, csvfile):
        self._csvfile = csvfile
        self._dialect = csv.Sniffer().sniff(self._csvfile.read(1024))

    @property
    def csvfile(self):
        self._csvfile.seek(0)
        return self._csvfile

    @property
    def dialect(self):
        return self._dialect

    @property
    def reader(self):
        reader = csv.DictReader(self.csvfile, dialect=self.dialect)
        return reader


class MQTTMetric:
    def __init__(
        self, measurement: str, data: dict, tag_names: list, field_names: list
    ):
        self._measurement = measurement
        self._data = data
        self._tag_names = tag_names
        self._field_names = field_names
        self._tags = []
        self._fields = []

    @property
    def measurement(self):
        return self._measurement

    @property
    def timestamp(self):
        return int(time.time() * 1e9)

    @property
    def message(self):
        for k in self._tag_names:
            self.add_tag(k, self._data[k])
        for k in self._field_names:
            self.add_field(k, self._data[k])
        return f"{self.measurement}{self._tags_to_string()} {self._fields_to_string()} {self.timestamp}\n"

    def add_field(self, key, value):
        self._fields.append(f"{self.escape_string(key)}={value}")

    def add_tag(self, key, value):
        self._tags.append(f"{self.escape_string(key)}={self.escape_string(value)}")

    def _fields_to_string(self):
        return ",".join(self._fields)

    def _tags_to_string(self):
        if self._tags:
            return f",{','.join(self._tags)}"
        else:
            return ""

    @staticmethod
    def escape_string(string):
        return string.translate(string.maketrans({",": r"\,", " ": r"\ ", "=": r"\="}))

    @staticmethod
    def quote_string(string):
        return f'"{string}"'

class MQTTPublisher:
    def __init__(self, broker: str, port: int):
        self.broker = broker
        self.port = port

    def publish(self, topic, message):
        publish.single(topic, payload=message, hostname=self.broker, port=self.port)
        logging.info(f"Published `{message}` to topic `{topic}`")


def load_event_data(config, broker, port, topic, csvfile, interval):
    reader = CSVReader(csvfile).reader
    publisher = MQTTPublisher(broker, port)

    for r in reader:
        metric = MQTTMetric(
            measurement="thermostat",
            data=r,
            tag_names=config["tags"],
            field_names=config["fields"],
        )

        publisher.publish(topic, metric.message)
        time.sleep(interval)


def process_cli():
    parser = argparse.ArgumentParser(description="publish MQTT messages")
    parser.add_argument(
        "--broker", dest="broker", default="localhost", help="MQTT broker host"
    )
    parser.add_argument(
        "--port", dest="port", type=int, default=1883, help="MQTT broker port"
    )
    parser.add_argument("--topic", dest="topic", help="MQTT topic")
    parser.add_argument(
        "--interval",
        dest="interval",
        type=int,
        default="5",
        help="publish interval (secs)",
    )
    parser.add_argument(
        "--input", dest="input_file", type=argparse.FileType("r"), help="input file"
    )
    return parser.parse_args()


def main():
    logging.basicConfig(level=logging.INFO)
    args = process_cli()
    configuration = load(config, Loader=Loader)

    if args.input_file:
        load_event_data(
            configuration,
            args.broker,
            args.port,
            args.topic,
            args.input_file,
            args.interval,
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
