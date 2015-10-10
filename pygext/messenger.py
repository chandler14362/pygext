__author__ = 'stowellc17'


from pygext.notifier import global_notify


class Messenger:
    notify = global_notify.new_category('Messenger')

    def __init__(self):
        self._acceptors = {}

    def accept(self, object, event, method):
        if event not in self._acceptors:
            self._acceptors[event] = []

        for accepting_data in self._acceptors[event]:
            if accepting_data[0] == object:
                self.notify.warning('%s tried accepting an event it was already accepting: %s' % (object, event))
                return

        self._acceptors[event].append([object, method])

    def ignore(self, object, event):
        if event not in self._acceptors:
            self.notify.warning('%s tried ignoring an event it wasnt accepting: %s' % (object, event))
            return

        for accepting_data in self._acceptors[event]:
            if accepting_data[0] == object:
                self._acceptors[event].remove(accepting_data)

                if len(self._acceptors[event]) == 0:
                    del self._acceptors[event]

                return

        self.notify.warning('%s tried ignoring an event it wasnt accepting: %s' % (object, event))

    def send(self, event, args=None, kwargs=None):
        if event not in self._acceptors:
            return

        args = args or []
        kwargs = kwargs or {}

        for accepting_data in self._acceptors[event]:
            accepting_data[1](*args, **kwargs)

    def ignore_all_events(self):
        for event in self._acceptors:
            for object, _ in self._acceptors[event]:
                self.ignore(object, event)

global_messenger = Messenger()
