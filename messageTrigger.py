import time
import threading
# from firebase import firebase
import firebase.firebase as fb
import firebase.settings as s

# s.INSERTION_TIME = 2
# s.HIGH_PRIORITY_TIME = 20
# s.LOW_PRIORITY_TIME = 60
# s.HIGH_ALERT_TIMER, s.LOW_ALERT_TIMER = s.HIGH_PRIORITY_TIME, s.LOW_PRIORITY_TIME

HIGH_ALERT_DATA = {}
LOW_ALERT_DATA = {}


def __start_high_alert_timer__():
    """This method needs to be called in a thread."""
    # global s.HIGH_ALERT_TIMER
    s.HIGH_ALERT_TIMER = 0
    while s.HIGH_ALERT_TIMER < s.HIGH_PRIORITY_TIME:
        time.sleep(1)
        s.HIGH_ALERT_TIMER += 1


def __start_low_alert_timer__():
    """This method needs to be called in a thread."""
    # global s.LOW_ALERT_TIMER
    s.LOW_ALERT_TIMER = 0
    while s.LOW_ALERT_TIMER < s.LOW_PRIORITY_TIME:
        time.sleep(1)
        s.LOW_ALERT_TIMER += 1


def send_high_alert(name, accuracy, image):
    def send_message():
        if len(HIGH_ALERT_DATA) > 0:
            max_pair = sorted(HIGH_ALERT_DATA.items(), key=lambda x: x[1][0])[0]
            # todo: send the message using firebase
            fb.send_message(name, accuracy, image)
            print("high alert triggerd")
            print(f"high alert --:{max_pair[0]} -- {max_pair[1][1]}")
            HIGH_ALERT_DATA.clear()
            pass
        else:
            print(f"high alert :{name} -- {accuracy}")

    # global s.HIGH_ALERT_TIMER
    if s.HIGH_PRIORITY_TIME == s.HIGH_ALERT_TIMER:
        if len(HIGH_ALERT_DATA) == 0:
            HIGH_ALERT_DATA[name] = (1, accuracy, image)
        send_message()

        threading.Thread(target=__start_high_alert_timer__).start()
    elif s.HIGH_ALERT_TIMER >= s.HIGH_PRIORITY_TIME - s.INSERTION_TIME:
        count = 1 if HIGH_ALERT_DATA.get(name) is None else HIGH_ALERT_DATA.get(name)[0] + 1
        HIGH_ALERT_DATA[name] = (count, accuracy, image)


def send_low_alert(name, accuracy, image):
    # pass
    # print(f'low alert : {name} -- {accuracy}')
    #
    def send_message():
        if len(LOW_ALERT_DATA) > 0:
            max_pair = sorted(LOW_ALERT_DATA.items(), key=lambda x: x[1][0])[0]
            # todo: send the message using firebase
            fb.send_message(name, accuracy, image)
            print("low alert triggerd")
            print(f"high alert --:{max_pair[0]} -- {max_pair[1][1]}")
            LOW_ALERT_DATA.clear()
            pass
        else:
            print(f"high alert :{name} -- {accuracy}")

    # global s.LOW_ALERT_TIMER
    if s.LOW_PRIORITY_TIME == s.LOW_ALERT_TIMER:
        if len(LOW_ALERT_DATA) == 0:
            LOW_ALERT_DATA[name] = (1, accuracy, image)
        send_message()

        threading.Thread(target=__start_low_alert_timer__).start()
    elif s.LOW_ALERT_TIMER >= s.LOW_PRIORITY_TIME - s.INSERTION_TIME:
        count = 1 if LOW_ALERT_DATA.get(name) is None else LOW_ALERT_DATA.get(name)[0] + 1
        LOW_ALERT_DATA[name] = (count, accuracy, image)
