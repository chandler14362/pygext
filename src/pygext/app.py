__author__ = 'stowellc17'


import sys


if sys.version_info >= (3, 0):
    import builtins as __builtin__
else:
    import __builtin__


# Create the global notifer
from pygext.notifier import Notifier
__builtin__.notifier = Notifier()

# Create the global config
from pygext.config import Config
__builtin__.config = Config()

# Create the global messenger
from pygext.messenger import Messenger
__builtin__.messenger = Messenger()

# Create the global task_mgr
from pygext.taskmanager import TaskManager
__builtin__.task_mgr = TaskManager()


from twisted.internet import reactor

from pygext.gameobject import GameObject

from pygame.locals import *
import pygame


class App(GameObject):
    notify = notifier.new_category('App')

    def __init__(self):
        GameObject.__init__(self)

        # Make ourselves a builtin type
        __builtin__.app = self

        # Init pygame
        pygame.init()

        # Set the notify level
        notifier.set_notify_level(config.get_notify_level())

        # Update the window properties
        pygame.display.set_caption(config.get('window-title', 'PyGame'))
        pygame.display.set_mode(config.get('window-res', [800, 600]))

        # Update the display
        pygame.display.update()

    def __tick(self, task):
        # Process the pending pygame events
        for event in pygame.event.get():
            messenger.send(event.type)

        return task.AGAIN

    def run(self):
        # Accept the QUIT event
        self.accept(QUIT, self.exit)

        # Create the main loop
        task_mgr.add('main-loop', self.__tick)

        # Run the reactor
        reactor.run()

    def exit(self):
        reactor.stop()
        pygame.quit()
        sys.exit()
