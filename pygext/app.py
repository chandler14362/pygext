__author__ = 'stowellc17'


import sys

from twisted.internet import reactor

from pygext.notifier import global_notify
from pygext.config import global_config
from pygext.messenger import global_messenger
from pygext.taskmanager import global_taskmgr, TASK_AGAIN
from pygext.gameobject import GameObject

from pygame.locals import *
import pygame


class App(GameObject):
    notify = global_notify.new_category('App')

    def __init__(self):
        GameObject.__init__(self)

        # Init pygame
        pygame.init()

        # Set the notify level
        global_notify.notify_level = global_config.notify_level

        # Update the window properties
        pygame.display.set_caption(global_config.get('window-title', 'PyGame'))
        pygame.display.set_mode(global_config.get('window-res', [800, 600]))

        # Update the display
        pygame.display.update()

    def __tick(self, task):
        # Process the pending pygame events
        for event in pygame.event.get():
            global_messenger.send(event.type)

        return TASK_AGAIN

    def run(self):
        # Accept the QUIT event
        self.accept(QUIT, self.exit)

        # Create the main loop
        global_taskmgr.add('main-loop', self.__tick)

        # Run the reactor
        reactor.run()

    def exit(self):
        reactor.stop()
        pygame.quit()
        sys.exit()
