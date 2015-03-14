__author__ = 'stowellc17'


from twisted.internet.error import AlreadyCalled
from twisted.internet.task import LoopingCall
from twisted.internet import reactor


class Task:
    notify = notifier.new_category('Task')

    DONE = 0
    AGAIN = 1

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

        if task_status == Task.DONE:
            self.__finish()
            return

        if task_status == Task.AGAIN:
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

    def get_name(self):
        return self.name

    def is_looping(self):
        return self.looping

    def get_delay(self):
        return self.delay


class TaskManager:
    notify = notifier.new_category('TaskManager')

    def __init__(self):
        self.__tasks = {}

    def add(self, name, method, args=[], kwargs={}):
        if name in self.__tasks:
            self.notify.warning('Tried to add task %s when it was already in the task dict' % name)
            return None

        task = Task(self, name, method, args, kwargs, True, 0)
        self.__tasks[name] = task
        task.start()

        return task

    def do_method_later(self, delay, name, method, args=[], kwargs={}):
        if name in self.__tasks:
            self.notify.warning('Tried to add task %s when it was already in the task dict' % name)
            return None

        task = Task(self, name, method, args, kwargs, False, delay)
        self.__tasks[name] = task
        task.start()

        return task

    def remove(self, name):
        if name not in self.__tasks:
            self.notify.warning('Tried to remove non-existent task %s' % name)
            return

        self.__tasks[name].stop()
        del self.__tasks[name]

    def stop_all_tasks(self):
        for name in self.__tasks:
            self.remove(name)
