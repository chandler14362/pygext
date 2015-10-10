__author__ = 'stowellc17'


from twisted.internet.error import AlreadyCalled
from twisted.internet.task import LoopingCall
from twisted.internet import reactor

from pygext.notifier import global_notify


TASK_DONE = 0
TASK_AGAIN = 1


class Task:
    notify = global_notify.new_category('Task')

    def __init__(self, task_mgr, name, method, args, kwargs, looping, delay):
        self.task_mgr = task_mgr
        self.name = name
        self.method = method
        self.args = args
        self.kwargs = kwargs
        self.looping = looping
        self.delay = delay

        self.caller = None

    def call_method(self):
        task_status = self.method(self, *self.args, **self.kwargs)

        if task_status == TASK_DONE:
            self.__finish()
            return

        if task_status == TASK_AGAIN:
            if not self.looping:
                self.start()
            return

        self.notify.warning('Task returned invalid status %s' % task_status)

    def start(self):
        if self.looping:
            self.caller = LoopingCall(self.call_method)
            self.caller.start(1.0 / 60.0)
            return

        self.caller = reactor.callLater(self.delay, self.call_method)

    def stop(self):
        if not self.looping:
            try:
                self.caller.cancel()
            except AlreadyCalled:
                pass
            return

        self.caller.stop()

    def __finish(self):
        self.task_mgr.remove(self.name)


class TaskManager:
    notify = global_notify.new_category('TaskManager')

    def __init__(self):
        self._tasks = {}

    def add(self, name, method, args=None, kwargs=None):
        if name in self._tasks:
            self.notify.warning('Tried to add task %s when it was already in the task dict' % name)
            return

        args = args or []
        kwargs = kwargs or {}

        task = Task(self, name, method, args, kwargs, True, 0)
        self._tasks[name] = task
        task.start()

        return task

    def do_method_later(self, delay, name, method, args=None, kwargs=None):
        if name in self._tasks:
            self.notify.warning('Tried to add task %s when it was already in the task dict' % name)
            return

        args = args or []
        kwargs = kwargs or {}

        task = Task(self, name, method, args, kwargs, False, delay)
        self._tasks[name] = task
        task.start()

        return task

    def remove(self, name):
        if name not in self._tasks:
            self.notify.warning('Tried to remove non-existent task %s' % name)
            return

        self._tasks[name].stop()
        del self._tasks[name]

    def stop_all_tasks(self):
        for name in self._tasks.keys():
            self.remove(name)

global_taskmgr = TaskManager()
