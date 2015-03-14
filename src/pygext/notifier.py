__author__ = 'stowellc17'


class NotifyCategory:
    def __init__(self, notify, name):
        self.notify = notify
        self.name = name

    def debug(self, message):
        if self.notify.can_output(self.notify.DEBUG):
            print('|DEBUG| %s: %s' % (self.name, message))

    def info(self, message):
        if self.notify.can_output(self.notify.INFO):
            print('|INFO| %s: %s' % (self.name, message))

    def warning(self, message):
        if self.notify.can_output(self.notify.WARNING):
            print('|WARNING| %s: %s' % (self.name, message))

    def error(self, message):
        if self.notify.can_output(self.notify.ERROR):
            print('|ERROR| %s: %s' % (self.name, message))
            app.exit()



class Notifier:
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3

    def __init__(self):
        self.notify_level = Notifier.DEBUG

    def can_output(self, notify_level):
        return notify_level >= self.notify_level

    def new_category(self, name):
        return NotifyCategory(self, name)

    def set_notify_level(self, notify_level):
        self.notify_level = notify_level
