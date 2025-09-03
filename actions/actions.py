import json
import os
import pandas as pd

def take(target):
    with open('manifest.json', 'r') as f:
        data = json.loads(f.read())
        return data[target]

def insert(target, new):
    data = {}
    with open('manifest.json', 'r') as f:
        data = json.loads(f.read())
        data[target] = new
    with open('manifest.json', 'w') as f:
        json.dump(data, f, indent=4)

def delete(target):
    os.remove(target)

def make_request():
    return True, 'making request'

def get_data(target):
    file = take('file')
    data = pd.read_csv(file)
    msg  = ''
    if target == 'cols':
        for col in data.columns:
            dt = data[col].dtype
            msg = '{}\n{} -> {}'.format(msg, col, dt)
    else:
        msg = 'target not recognized'

    return msg

def explore(code):
    if code == 'act':
        insert('transfer', True)
        return 'transference started'
    elif code == 'end':
        insert('transfer', False)
        filepath = take('file')
        delete(filepath)
        insert('file', '')
        return 'transference finished'
    elif code == 'state':
        res = take('transfer')
        return 'transfer: {}'.format(res)
    else:
        return 'not recognized code'

