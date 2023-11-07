# for main file
ALARM_MODE = bool(True)
STATUS = 0

# for message trigger file
INSERTION_TIME = 2
HIGH_PRIORITY_TIME = 20
LOW_PRIORITY_TIME = 60
HIGH_ALERT_TIMER, LOW_ALERT_TIMER = HIGH_PRIORITY_TIME, LOW_PRIORITY_TIME


def set_high_priority_time(time: int):
    global HIGH_ALERT_TIMER, HIGH_PRIORITY_TIME
    HIGH_PRIORITY_TIME = HIGH_ALERT_TIMER = time


def set_low_priority_time(time: int):
    global LOW_ALERT_TIMER, LOW_PRIORITY_TIME
    LOW_PRIORITY_TIME = LOW_ALERT_TIMER = time


