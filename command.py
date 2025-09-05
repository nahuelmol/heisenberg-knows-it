from actions.actions import make_request, get_data, explore

class Command:
    def __init__(self, cmd):
        self.cmd = cmd
        self.root = cmd[0][1:]
        self.options = None
        self.message = ''

    def set(self):
        if self.root == 'cal':
            if len(self.cmd) > 1:
                self.action = self.cmd[1]
                if len(self.cmd) > 2:
                    self.options = self.cmd[2:]
            else:
                self.message = 'few args'

    def execute(self):
        if self.root == 'cal':
            if self.action == 'req':
                res, msg = make_request()
                self.message = msg
            elif self.action == 'time':
                self.message = 'requesting time'
            elif self.action == 'act':
                msg = explore('act')
                self.message = msg
            elif self.action == 'end':
                msg = explore('end')
                self.message = msg
            elif self.action == 'ch':
                msg = explore('state')
                self.message = msg
            elif self.action == 'cols':
                msg = get_data('cols')
                self.message = msg
            elif self.action == 'typs':
                msg = get_data('typs')
                self.message = msg
            elif self.action == 'dims':
                msg = get_data('dims')
                self.message = msg
            elif self.action == 'dir':
                msg = fsys()
                self.message = msg
            else:
                self.message = 'not recognized action'
        else:
            self.message = 'not recognized cmd'
