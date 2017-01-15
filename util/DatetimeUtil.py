import datetime


def string2datetime(string_date):
    fmt = "%Y-%m-%d %H:%M:%S"
    return datetime.datetime.strptime(string_date, fmt)
