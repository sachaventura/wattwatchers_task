from datetime import datetime

def get_current_timestamp():
    now = datetime.now()
    return int(datetime.timestamp(now))

def joules_to_kwh(joules):
    return  joules / 3600000
