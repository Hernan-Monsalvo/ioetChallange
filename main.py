import os
import sys

from typing import List, Tuple

from exceptions import DataError, DayOutboundError

class Wages():
    normal = [
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
    ]
    weekend = [
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

def load_file(file_path: str) -> List[str]:
    """
    param file_path: Path to the file with the data to calculate
    return: list of lines from the file
    """
    if not os.path.exists(file_path):
        print("file not found")
        raise FileNotFoundError

    with open(file_path, "r") as f:
        return f.readlines()


def hour_to_minutes(hour24: str) -> int:
    """
    param hour24: a string hour in format 'hh:mm'
    return: amount of minutes from 00:00 to input hour
    """
    try:
        hour, minutes = hour24.split(":")
        return (int(hour) * 60) + int(minutes)
    except ValueError:
        raise DataError(hour24)


def calculate(input_str: str) -> Tuple[str, int]:
    """
    param input_str: string specifying the schedule of one employee
    return: tuple containing the employee name and the payment
    """
    try:
        employee, schedule = input_str.split("=")
        lapses = schedule.split(",")
    except ValueError:
        raise DataError(input_str)

    payment = 0

    for lapse in lapses:
        day = lapse[:2]
        time = lapse[2:]
        try:
            start_time, end_time = time.split("-")
        except ValueError:
            raise DataError(input_str)
        start_in_minutes = hour_to_minutes(start_time)
        end_in_minutes = hour_to_minutes(end_time)
        if (end_in_minutes - start_in_minutes) < 0:
            raise DayOutboundError(lapse)

        wages = Wages.weekend if day in ["SA", "SU"] else Wages.normal

        for period in wages:
            if period["initial"] <= start_in_minutes <= period["end"]:
                if end_in_minutes < period["end"]:
                    worked_minutes = end_in_minutes - start_in_minutes

                else:
                    worked_minutes = period["end"] - start_in_minutes
                    # if the worked period go through the change of wage
                    # the start is moved forward, so it enters the next loop.
                    start_in_minutes += worked_minutes

                payment += worked_minutes / 60 * period["value"]

    return employee, int(payment)


if __name__ == '__main__':


    try:
        path = sys.argv[1]
        lines = load_file(path)
    except FileNotFoundError as e:
        exit()
    except IndexError:
        print("No file path was given")
        exit()

    for line in lines:
        employee, payment = calculate(line)
        print(f"The amount to pay {employee} is: {payment} USD")
