#
# This source code is licensed under the terms of the
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2016
#
import datetime


def string_to_float_or_zero(string):
    """
    Try to convert a string to an float, returns 0.0 on failure
    :param string: String to convert
    :type string: str
    :return: float value of the string or 0.0
    :rtype: float
    """
    try:
        return float(string.replace(',', '.'))
    except ValueError:
        return 0


def string_to_float_or_value(string, value):
    """
    Try to convert a string to an float, returns value on failure
    :param string: String to convert
    :type string: str
    :param value: Default value
    :type value: float
    :return: float value of the string or value
    :rtype: float
    """
    try:
        return float(string.replace(',', '.'))
    except ValueError:
        return value


def string_to_int_or_zero(string):
    """
    Try to convert a string to an int, returns 0 on failure
    :param string: String to convert
    :type string: str
    :return: integer value of the string or 0
    :rtype: int
    """
    try:
        return int(string)
    except ValueError:
        return 0


def string_to_int_or_value(string, value):
    """
    Try to convert a string to an int, returns value on failure
    :param string: String to convert
    :type string: str
    :param value: Default value
    :type value: int
    :return: integer value of the string or 0
    :rtype: int
    """
    try:
        return int(string)
    except ValueError:
        return value


def get_next_date(date, interval_months):
    """
    Get the first date that is `date + x*interval` that's in the future
    :param date: Starting date
    :type date: datetime.date
    :param interval_months: Interval in months
    :type interval_months: int
    :return: first date in future
    :rtype: datetime.date
    """
    interval = datetime.timedelta(days=interval_months * (365/12.0))
    while date < datetime.date.today():  # Move date to future
        date += interval
    return date


def get_closest_date(date, interval_months):
    """
    Get the closest date to today from `date + x*interval`. Can be in the future or in the past
    :param date: Starting date
    :type date: datetime.date
    :param interval_months: Interval in months
    :type interval_months: int
    :return: closest date on interval
    :rtype: datetime.date
    """
    now = datetime.date.today()
    next = get_next_date(date, interval_months)
    if abs((next - now).days) > (interval_months * 365/12 / 2):
        closest = next - datetime.timedelta(interval_months * (365/12))  # Have not passed half-way to next date
    else:
        closest = next                                                   # Past half-way

    return closest


def check_next_date_in_30d(orig_date, interval):
    """
    Check if the first date in future is within 30 days of today
    :param orig_date: Starting date
    :type orig_date: datetime.date
    :param interval: Date interval in months
    :type interval: int
    :return: Is next date withing 30 days?
    :rtype: bool
    """

    today = datetime.date.today()
    date = orig_date
    if date > today:                              # Date is in future
        if (date - today) < datetime.timedelta(days=30):  # and close enough
            return True
        else:
            return False                                  # Far away...

    date = get_next_date(date, interval)

    if (date - today) < datetime.timedelta(days=30):
        return True
    else:
        return False