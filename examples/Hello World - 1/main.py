__author__ = 'stowellc17'


'''
Example 1: Hello World

This example shows you how to do the following:
- Start your app using App
- Load in the config
'''


# The first thing we need to do to get or app running is import App.
# Once App is imported all of the global objects are created.

# Here is the list of all the global objects:
# - messenger (Messenger instance)
# - task_mgr (TaskManager instance)
# - notifier (Notifier instance)
# - config (Config instance)

# Here is the import statement that will import App:
from pygext.app import App

# Now that we have imported App we can load in our config.
# In this example the config file is called config.json, however, you can call it whatever you want.
config.load_config('config.json')

# Now that we have our config loaded we can create the App instance.
# When you create the App instance, it assigns itself to a new global object called app.
App()

# Now that we have created our App instance we can start the app!
# To start the app simply add app.run().
# No code put after app.run() will be executed.
app.run()
