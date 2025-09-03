import json

def take_from_mani(target):
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

def make_request():
    return True, 'making request'

def explore(code):
    if code == 'act':
        insert('transfer', True)
        return 'transference initialized'
    elif code == 'end':
        insert('transfer', False)
        return 'transference finished'
    elif code == 'state':
        res = take_from_mani('transfer')
        return 'transfer: {}'.format(res)
    else:
        return 'not recognized code'

