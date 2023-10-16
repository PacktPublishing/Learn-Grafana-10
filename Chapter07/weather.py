#!/usr/bin/python3

import argparse
import logging
import requests
import sys

from dateutil.parser import isoparse


def iso_to_timestamp(ts):
    return int(isoparse(ts).timestamp())


def get_station_obs(station):
    url = f"https://api.weather.gov/stations/{station}/observations"
    response = requests.get(url)
    logging.info(response.url)
    if response.status_code != requests.codes.ok:
        raise Exception(f"get_station_obs: {response.status_code}:{response.reason}")

    data = response.json()["features"]
    return data


def get_station_info(station):
    info = {}

    url = f"https://api.weather.gov/stations/{station}"
    response = requests.get(url)
    logging.info(response.url)
    if response.status_code != requests.codes.ok:
        raise Exception(f"get_station_info: {response.status_code}:{response.reason}")

    station_properties = response.json()["properties"]
    info["station_name"] = station_properties["name"].split(",")
    info["station_id"] = station_properties["stationIdentifier"]

    url = station_properties["county"]
    response = requests.get(url)
    logging.info(response.url)
    if response.status_code != requests.codes.ok:
        raise Exception(f"get_station_info: {response.status_code}:{response.reason}")

    county_properties = response.json()["properties"]
    info["county"] = county_properties["name"]
    info["state"] = county_properties["state"]
    info["cwa"] = county_properties["cwa"]
    info["timezone"] = county_properties["timeZone"]

    return info


def load_wx_data(db_host, db_port, db_name, token, precision, input_file):
    if not db_name:
        raise Exception(f"load_wx_data: no database specified")

    url = f"http://{db_host}:{db_port}/write"
    headers = {"Authorization": f"Token {token}"}
    data = input_file.read()
    response = requests.post(
        url, params=dict(db=db_name, precision=precision), headers=headers, data=data
    )
    logging.info(response.url)
    if response.status_code != requests.codes.no_content:
        raise Exception(f"load_wx_data: {response.status_code}:{response.reason}")


def escape_string(string):
    return string.translate(string.maketrans({",": "\,", " ": "\ ", "=": "\="}))


def dump_wx_data(stations, output):
    for s in stations.split(","):
        station_info = get_station_info(s)
        tags = [
            f'station={escape_string(station_info["station_id"])}',
            f'name={escape_string(",".join(station_info["station_name"]))}',
            f'cwa={escape_string(station_info["cwa"][0])}',
            f'county={escape_string(station_info["county"])}',
            f'state={escape_string(station_info["state"])}',
            f'tz={escape_string(station_info["timezone"][0])}',
        ]

        wx_data = get_station_obs(s)
        for feature in wx_data:
            for measure, observation in feature["properties"].items():
                if not isinstance(observation, dict) or measure in ["elevation"]:
                    continue

                value = observation["value"]
                if value is None:
                    continue

                unit = observation["unitCode"]

                timestamp = iso_to_timestamp(feature["properties"]["timestamp"])

                data = f'{measure},{",".join(tags)},unit={unit} value={value} {timestamp}\n'
                output.write(data)

    output.close()


def process_cli():
    parser = argparse.ArgumentParser(
        description="read forecast data from NWS into Influxdb"
    )
    group = parser.add_mutually_exclusive_group()

    parser.add_argument(
        "--host", dest="host", default="localhost", help="database host"
    )
    parser.add_argument(
        "--port", dest="port", type=int, default=8086, help="database port"
    )
    parser.add_argument(
        "--db", dest="database", help="name of database to store data in"
    )
    parser.add_argument(
        "--stations",
        dest="stations",
        help="list of stations to gather weather data from",
    )
    parser.add_argument("--token", dest="token", help="InfluxDB API token")
    parser.add_argument("--precision", dest="precision", default="s", 
        help="InfluxDB data precision")
    group.add_argument(
        "--input", dest="input_file", type=argparse.FileType("r"), help="input file"
    )
    group.add_argument(
        "--output", dest="output_file", type=argparse.FileType("w"), help="output file"
    )
    return parser.parse_args()


def main():
    logging.basicConfig(level=logging.INFO)
    args = process_cli()

    if args.output_file:
        dump_wx_data(args.stations, args.output_file)

    if args.input_file:
        load_wx_data(
            db_host=args.host,
            db_port=args.port,
            db_name=args.database,
            token=args.token,
            precision=args.precision,
            input_file=args.input_file,
        )


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as err:
        logging.exception(err)
        sys.exit(1)
