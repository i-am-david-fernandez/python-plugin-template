import logging

import plugin_family.plugin

LOGGER = logging.getLogger(__name__)

class MyPlugin(plugin_family.plugin.PluginBase):

    @classmethod
    def get_code(cls):
        '''Returns the code/label of this data source as a string.'''
        return 'my_plugin'
