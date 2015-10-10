__author__ = 'stowellc17'


from pygext.notifier import global_notify
from pygext.messenger import global_messenger


class GameObject:
    notify = global_notify.new_category('GameObject')

    def __init__(self):
        self._accepting = []

    def accept(self, event, method):
        if event in self._accepting:
            self.notify.warning('Tried accepting an event that is already being accepted: %s' % event)
            return

        global_messenger.accept(self, event, method)
        self._accepting.append(event)

    def ignore(self, event):
        if event in self._accepting:
            global_messenger.ignore(self, event)
            self._accepting.remove(event)

    def ignore_all(self):
        for event in self._accepting:
            global_messenger.ignore(self, event)

        del self._accepting[:]
