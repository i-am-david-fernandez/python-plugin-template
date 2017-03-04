'''Template for a plugin factory.'''

import logging

from . import plugin

LOGGER = logging.getLogger(__name__)


class Factory(object):
    '''A factory class to create/provide --- objects.'''


    @classmethod
    def list(cls):
        '''Return a list of available plugins.'''

        plugin.initialise()
        return plugin.get_codes()


    @classmethod
    def get(cls, plugin_code, *args, **kwargs):
        '''Return a --- object for the specified plugin.'''

        plugin.initialise()
        return plugin.instantiate(plugin_code, *args, **kwargs)
