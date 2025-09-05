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
    elif target == 'typs':
        cats = data.select_dtypes(include=['object', 'category', 'string']).columns
        nums = data.select_dtypes(include=['int32', 'float32', 'int64', 'float64']).columns
        msg = '\tcategorical:'
        for each in cats:
            msg = '{}\n{}'.format(msg, each)
        msg = '{}\n\tnumerical:'
        for each in nums:
            msg = '{}\n{}'.format(msg, each)
    elif target == 'dims':
        cols, labs = data.shape
        msg = 'cols: {}\nlabs: {}'.format(cols, labs)
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

