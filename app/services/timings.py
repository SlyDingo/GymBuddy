import datetime, time

def epoch_now() -> int:
    """Returns the current time in Unix epoch format."""
    return int(time.time())

def epoch_to_datetime(epoch_time: int, format='') -> str:
    """Converts Unix epoch time to a datetime object."""
    time = datetime.datetime.fromtimestamp(epoch_time)

    if format:
        return time.strftime(format)
    
    return str(datetime.datetime.fromtimestamp(epoch_time))
