from datetime import datetime

def get_timestamp_now():
    current_datetime = datetime.now()
    unix_timestamp = int(current_datetime.timestamp() * 1000)
    return unix_timestamp
