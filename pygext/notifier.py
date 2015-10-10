__author__ = 'stowellc17'


LEVEL_DEBUG = 0
LEVEL_INFO = 1
LEVEL_WARNING = 2
LEVEL_ERROR = 3


class NotifyCategory:
    def __init__(self, notify, name):
        self.notify = notify
        self.name = name

    def debug(self, message):
        if self.notify.can_output(LEVEL_DEBUG):
            print('|DEBUG| %s: %s' % (self.name, message))

    def info(self, message):
        if self.notify.can_output(LEVEL_INFO):
            print('|INFO| %s: %s' % (self.name, message))

    def warning(self, message):
        if self.notify.can_output(LEVEL_WARNING):
            print('|WARNING| %s: %s' % (self.name, message))

    def error(self, message):
        if self.notify.can_output(LEVEL_ERROR):
            print('|ERROR| %s: %s' % (self.name, message))
            app.exit()


class Notifier:
    def __init__(self):
        self.notify_level = LEVEL_DEBUG

    def can_output(self, notify_level):
        return notify_level >= self.notify_level

    def new_category(self, name):
        return NotifyCategory(self, name)

global_notify = Notifier()
