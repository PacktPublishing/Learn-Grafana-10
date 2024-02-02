#!env python3

import csv
import io
import sys


def is_comment(l):
    return l[0] == "#"


def is_blank(l):
    return l.strip() == ""


def filter_csv(f):
    with open(f) as csvfile:
        return io.StringIO(
            "".join(
                [
                    l
                    for l in csvfile.readlines()
                    if not is_comment(l) and not is_blank(l)
                ]
            )
        )


def prep_csv(f):
    csvfile = filter_csv(f)

    header, *csvrows = csvfile.readlines()
    fieldnames = header.strip().split(",")

    csvfile = io.StringIO("".join(csvrows))
    dialect = csv.Sniffer().sniff(header)

    return fieldnames, csvfile, dialect


def split_csv(f):
    header, *lines = f.readlines()
    return header, io.StringIO(lines)


def calc_delta(f, t):
    diffs = {}
    for k in f:
        if f[k] == t[k] or t[k] == "":
            continue

        diff = (f[k], t[k])
        diffs[k] = diff
        print(diffs)
    return diffs


numeric_fields = [
    "Set Temp (F)",
    "Heat Set Temp (F)",
    "Current Temp (F)",
    "Current Humidity (%RH)",
    "Outdoor Temp (F)",
    "Wind Speed (km/h)",
    "Cool Stage 1 (sec)",
    "Heat Stage 1 (sec)",
    "Aux Heat 1 (sec)",
    "Fan (sec)",
    "DM Offset",
    "Thermostat Temperature (F)",
    "Thermostat Humidity (%RH)",
    "Thermostat Motion",
    "Upstairs (F)",
    "Upstairs2",
]


def conform_row(row):
    for key in row:
        field = row[key]
        if field != "" and key in numeric_fields:
            row[key] = float(field)
    return row


def calculate_deltas(r):
    deltas = []
    from_val, to_val = None, None

    for row in r:
        if r.line_num == 1:
            continue

        # row = conform(row)
        if not to_val:
            to_val = row
            continue

        from_val, to_value = to_val, row

        if from_val == to_val:
            continue

        deltas.append(calc_delta(from_val, to_val))

    return deltas


exclusion_list = ["Time", "Date", None]


def purge_fields(reader):
    rows = []

    for row in reader:
        new_row = dict((k, v) for k, v in row.items() if k not in exclusion_list)
        rows.append(new_row)

    return rows


def main():
    input = "data/report-312915984121-2023-02-18-to-2023-02-25.csv"
    output = "data/thermostat_events.csv"

    fieldnames, csvfile, dialect = prep_csv(input)
    reader = csv.DictReader(csvfile, fieldnames=fieldnames, dialect=dialect)

    rows = purge_fields(reader)
    fieldnames = [k for k in fieldnames if k not in exclusion_list]

    with open(output, "w") as of:
        writer = csv.DictWriter(of, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return 0


if __name__ == "__main__":
    sys.exit(main())
