import os
import sys
from exceptions import DataError, DayOutboundError

WAGES = {
    "normal": [
        {
            "initial": 1,
            "end": 9 * 60,
            "value": 25
        },
        {
            "initial": 9 * 60,
            "end": 18 * 60,
            "value": 15
        },
        {
            "initial": 18 * 60,
            "end": 24 * 60,
            "value": 20
        }
    ],
    "weekend": [
        {
            "initial": 1,
            "end": 9 * 60,
            "value": 30
        },
        {
            "initial": 9 * 60,
            "end": 18 * 60,
            "value": 20
        },
        {
            "initial": 18 * 60,
            "end": 24 * 60,
            "value": 25
        }
    ]
}

def load_file(file_path: str) -> list:
    if not os.path.exists(file_path):
        print("file not found")
        raise FileNotFoundError

    with open(file_path, "r") as f:
        return f.readlines()


def hour_to_minutes(hour24: str) -> int:
    try:
        hour, minutes = hour24.split(":")
        return (int(hour) * 60) + int(minutes)
    except ValueError:
        raise DataError(input)


def calculate(input: str) -> str:
    try:
        employee, schedule = input.split("=")
        lapses = schedule.split(",")
    except ValueError:
        raise DataError(input)

    payment = 0

    for lapse in lapses:
        day = lapse[:2]
        time = lapse[2:]
        try:
            start_time, end_time = time.split("-")
        except ValueError:
            raise DataError(input)
        start_in_minutes = hour_to_minutes(start_time)
        end_in_minutes = hour_to_minutes(end_time)
        if (end_in_minutes - start_in_minutes) < 0:
            raise DayOutboundError(lapse)

        wages = WAGES["weekend"] if day in ["SA", "SU"] else WAGES["normal"]

        for period in wages:
            if period["initial"] <= start_in_minutes <= period["end"]:
                if end_in_minutes < period["end"]:
                    worked_minutes = end_in_minutes - start_in_minutes

                else:
                    worked_minutes = period["end"] - start_in_minutes
                    start_in_minutes += worked_minutes

                payment += worked_minutes / 60 * period["value"]

    output = (f"The amount to pay {employee} is: {int(payment)} USD")
    return output


if __name__ == '__main__':

    path = sys.argv[1]
    try:
        lines = load_file(path)
    except FileNotFoundError as e:
        exit()

    for line in lines:
        print(calculate(line))
