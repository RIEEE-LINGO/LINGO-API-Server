from datetime import datetime

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

USERS = {
    "1": {
        "first": "Mark",
        "last_name": "Hills",
        "created_on": get_timestamp(),
        "modified_on": get_timestamp(),
    }
}

def read_all():
    return list(USERS.values())