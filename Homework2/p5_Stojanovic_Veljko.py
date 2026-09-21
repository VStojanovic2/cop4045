import datetime
import sys


def read_observations(filename):
    """Read station observations, returning valid records and line errors."""
    observations = {}
    errors = []
    seen = set()

    with open(filename, "r", encoding="utf-8") as infile:
        for line_number, line in enumerate(infile, start=1):
            fields = line.strip().split(",")
            if len(fields) != 3:
                errors.append((line_number, "Malformed line: expected three fields"))
                continue

            station, date_text, temperature_text = [field.strip() for field in fields]
            if not station or not date_text or not temperature_text:
                errors.append((line_number, "Malformed line: fields cannot be empty"))
                continue

            try:
                date = datetime.datetime.strptime(date_text, "%I:%M:%S %p %m/%d/%Y")
            except ValueError:
                errors.append((line_number, "Invalid date"))
                continue

            try:
                temperature = float(temperature_text)
            except ValueError:
                errors.append((line_number, "Invalid temperature: expected a number"))
                continue

            if not -100 <= temperature <= 150:
                errors.append((line_number, "Invalid temperature: must be between -100 and 150"))
                continue

            key = (station, date)
            if key in seen:
                errors.append((line_number, "Duplicate station/date combination"))
                continue

            seen.add(key)
            observations.setdefault(station, []).append((date, temperature))

    for records in observations.values():
        records.sort(key=lambda record: record[0])

    return observations, errors


def station_statistics(observations):
    """Return (minimum, maximum, mean) temperatures for each station."""
    statistics = {}
    for station, records in observations.items():
        temperatures = [temperature for date, temperature in records]
        statistics[station] = (
            min(temperatures),
            max(temperatures),
            sum(temperatures) / len(temperatures),
        )
    return statistics


def station_outliers(observations):
    """Return stations whose latest temperature exceeds their mean."""
    statistics = station_statistics(observations)
    return {
        station: (date, temperature, statistics[station][2])
        for station, records in observations.items()
        for date, temperature in [max(records, key=lambda record: record[0])]
        if temperature > statistics[station][2]
    }


def write_statistics(filename, statistics):
    """Write station,minimum,maximum,mean rows in station order, without a header."""
    with open(filename, "w", encoding="utf-8") as outfile:
        for station in sorted(statistics):
            minimum, maximum, mean = statistics[station]
            outfile.write(f"{station},{minimum:.1f},{maximum:.1f},{mean:.1f}\n")


def main():
    """Read observations and report statistics using command-line filenames."""
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} input_file output_file", file=sys.stderr)
        return 1

    try:
        observations, errors = read_observations(sys.argv[1])
        for line_number, message in errors:
            print(f"Line {line_number}: {message}", file=sys.stderr)
        statistics = station_statistics(observations)
        print("Statistics:", statistics)
        print("Outliers:", station_outliers(observations))
        write_statistics(sys.argv[2], statistics)
    except OSError as error:
        print(f"File access error: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
