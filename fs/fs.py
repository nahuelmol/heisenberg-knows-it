import os

def fsys():
    current = os.getcwd()
    msg = '\tcwd:'
    for each in os.listdir(current):
        msg = '{}\n--{}'.format(msg, each)
    return msg

