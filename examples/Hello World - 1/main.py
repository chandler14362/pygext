__author__ = 'stowellc17'


'''
Example 1: Hello World

This example shows you how to do the following:
- Start your app using App
- Load in a config file
'''

# Here is the import statement that will import App:
from pygext.app import App

# We also need one for our global_config:
from pygext.config import global_config

# Now that we have imported global_config we can load in our config.
# In this example the config file is called config.json, however, you can call it whatever you want.
global_config.load_config('config.json')

# Now that we have our config loaded we can create the App instance.
app = App()

# Now that we have created our App instance we can start the app!
# To start the app simply add app.run().
# No code put after app.run() will be executed until the main loop ends.
app.run()
