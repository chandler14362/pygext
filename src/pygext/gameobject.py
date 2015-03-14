__author__ = 'stowellc17'


class GameObject:
    notify = notifier.new_category('GameObject')

    def __init__(self):
        self.__accepting = []

    def accept(self, event, method):
        if event in self.__accepting:
            self.notify.warning('Tried accepting an event that is already being accepted: %s' % event)
            return

        messenger.accept(self, event, method)
        self.__accepting.append(event)

    def ignore(self, event):
        if event in self.__accepting:
            messenger.ignore(self, event)
            self.__accepting.remove(event)

    def ignore_all(self):
        for event in self.__accepting:
            messenger.ignore(self, event)
            self.__accepting.remove(event)
