__author__ = 'stowellc17'


class Messenger:
    notify = notifier.new_category('Messenger')

    def __init__(self):
        self.__acceptors = {}

    def accept(self, object, event, method):
        if event not in self.__acceptors:
            self.__acceptors[event] = []

        for accepting_data in self.__acceptors[event]:
            if accepting_data[0] == object:
                self.notify.warning('%s tried accepting an event it was already accepting: %s' % (object, event))
                return

        self.__acceptors[event].append([object, method])

    def ignore(self, object, event):
        if event not in self.__acceptors:
            self.notify.warning('%s tried ignoring an event it wasnt accepting: %s' % (object, event))
            return

        for accepting_data in self.__acceptors[event]:
            if accepting_data[0] == object:
                self.__acceptors[event].remove(accepting_data)

                if len(self.__acceptors[event]) == 0:
                    del self.__acceptors[event]

                return

        self.notify.warning('%s tried ignoring an event it wasnt accepting: %s' % (object, event))

    def send(self, event, args=[], kwargs={}):
        if event not in self.__acceptors:
            return

        for accepting_data in self.__acceptors[event]:
            accepting_data[1](*args, **kwargs)

    def ignore_all_events(self):
        for event in self.__acceptors:
            for object, _ in self.__acceptors[event]:
                self.ignore(object, event)
