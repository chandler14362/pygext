__author__ = 'stowellc17'


from pygext.notifier import Notifier

import json


notify_levels = {
    'debug': Notifier.DEBUG,
    'info': Notifier.INFO,
    'warning': Notifier.WARNING,
    'error': Notifier.ERROR
}


class Config:
    notify = notifier.new_category('Config')

    def __init__(self):
        self.__values = {}

    def load_config(self, filepath):
        with open(filepath, 'r') as f:
            config_data = json.loads(f.read())
            self.__values.update(config_data)

    def get_notify_level(self):
        level = self.__values.get('notify-level', 'info')

        if level not in notify_levels:
            self.notify.warning('Unknown notify level: %s' % level)
            level = 'info'

        return notify_levels[level]

    def get(self, value, default_value):
        return self.__values.get(value, default_value)
