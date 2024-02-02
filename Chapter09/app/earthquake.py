import argparse
import logging
import requests
import sys
import time

# print(time.localtime())
# print(time.gmtime())


def escape_string(string):
    return string.translate(string.maketrans({",": r"\,", " ": r"\ ", "=": r"\="}))

def time_to_string(t):
    epoch_secs = int(t/1000)
    ltime = time.localtime(epoch_secs)
    ftime = time.strftime('%Y-%m-%d %H:%M:%S', ltime)
    return ftime

def dump_eq_data(size, window, output):
    url = f"https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/{size}_{window}.geojson"
    response = requests.get(url)
    logging.info(response.url)
    if response.status_code != requests.codes.ok:
        raise Exception(f"dump_eq_data: {response.status_code}:{response.reason}")

    for feature in response.json()['features']:
        measure = "event"

        properties, geometry = feature["properties"], feature["geometry"]

        lon, lat, dep = geometry['coordinates']

        mag = properties['mag']
        if mag is None:
            logging.error(f"bad event: {feature}")
            continue

        tags = [
            f"tag_latitude={lat}",
            f"tag_longitude={lon}",
            f"tag_place={escape_string(properties['place'])}",
            f"tag_alert={properties['alert']}",
            f"tag_time={escape_string(time_to_string(properties['time']))}"
        ]

        fields = [
            f"magnitude={properties['mag']}",
            f"cdi={properties['cdi'] if properties['cdi'] else 0.0}",
            f"mmi={properties['mmi'] if properties['mmi'] else 0.0}",
            f"felt={properties['felt'] if properties['felt'] else 0}",
            f"sig={properties['sig']}",
            f"depth={dep}",
        ]

        timestamp = properties['time']

        data = f"{measure},{','.join(tags)} {','.join(fields)} {timestamp}\n"
        logging.debug(data)
        output.write(data)

    output.close()


def load_eq_data(db_host, db_port, db_name, token, input_file, precision):
    if not db_name:
        raise Exception(f'drop: no database specified')

    url = f"http://{db_host}:{db_port}/write"
    headers = {"Authorization": f"Token {token}"}
    data = input_file.read().encode('utf-8')
    response = requests.post(
        url, params=dict(db=db_name, precision=precision), headers=headers, data=data
    )
    logging.info(response.url)
    if response.status_code != requests.codes.no_content:
        raise Exception(f"load_wx_data: {response.status_code}:{response.reason} {response.json()['message']}")
    

def process_cli():
    parser = argparse.ArgumentParser(description="read earthquake data from USGS into Influxdb")
    file_group = parser.add_mutually_exclusive_group()

    parser.add_argument('--host', dest='host', default='localhost',
                        help='database host')
    parser.add_argument('--port', dest='port', type=int, default=8086,
                        help='database port')
    parser.add_argument('--db', dest='database',
                        help="name of database to store data in")
    parser.add_argument("--token", dest="token", help="InfluxDB API token")
    file_group.add_argument('--input', dest='input_file', type=argparse.FileType('r'),
                            help="input file")
    file_group.add_argument('--output', dest='output_file', type=argparse.FileType('w'),
                            help='output file')
    parser.add_argument("--precision", dest="precision", default="s", 
                        help="InfluxDB data precision")
    parser.add_argument("--size", dest="size", choices=['significant', '4.5', '2.5', '1.0', 'all'],
                        default='significant', help="earthquake size")
    parser.add_argument("--window", dest="window", choices=['hour', 'day', 'week', 'month'],
                        default='hour', help="earthquake time window")

    return parser.parse_args()


def main():
    logging.basicConfig(level=logging.INFO)
    args = process_cli()

    if args.output_file:
        dump_eq_data(args.size, args.window, args.output_file)

    if args.input_file:
        load_eq_data(db_host=args.host, db_port=args.port, db_name=args.database,
        token=args.token,
        input_file=args.input_file,
        precision=args.precision)


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as err:
        logging.exception(err)
        sys.exit(1)
