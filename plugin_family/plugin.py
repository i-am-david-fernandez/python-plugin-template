'''Plugin framework.'''

import os
import sys
import logging
import importlib


LOGGER = logging.getLogger(__name__)


import abc


class PluginBase(metaclass=abc.ABCMeta):
    '''Base class definition for plugin.'''

    ## Pure abstract methods are decorated with '@abc.abstractmethod`.


    @classmethod
    @abc.abstractmethod
    def get_code(cls):
        '''Returns the code/label of this thing as a string.'''
        pass


    def __str__(self):
        '''Return a string representation.'''
        return self.get_code()


## <DF> Global (private) to hold plugin registry
_plugin_registry = {}


def find():
    '''Find all files in the plugin directory and imports them.
    Stolen from here: http://aroberge.blogspot.ch/2008/12/plugins-part-3-simple-class-based.html
    '''

    ## Add plugin directory to path so 'manual' imports succeed
    plugin_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'plugins')
    sys.path.insert(0, plugin_dir)
    LOGGER.debug('Scanning for plugins in %s', plugin_dir)

    try:
        ## Include only files ending in '.py' and exclude '__init__.py' and derivatives
        plugin_files = [x[:-3] for x in os.listdir(plugin_dir)
                        if (x.endswith('.py')) and (not '__init__' in x)]
    except FileNotFoundError:
        return

    ## This feels terribly fudgy, but so be it.
    ## We wish to import each plugin with full package name resolution, otherwise
    ## multiple (separate) plugin groups within an application won't always work,
    ## seemingly due to a name collision/conflict.
    ## So, we will construct a package name based on the (leading) name of _this_
    ## module, essentially retaining all but the last component. For example,
    ## if this module is "a.b.c.plugin", we will construct a parent package
    ## name of "a.b.c", and combine this with each plugin name to form
    ## "a.b.c.plugins.my_plugin"

    parent_package_name = '.'.join(__name__.split('.')[:-1])

    for plugin in plugin_files:
        plugin = '{}.plugins.{}'.format(parent_package_name, plugin)
        LOGGER.debug('Importing plugin: %s', plugin)
        importlib.import_module(plugin)


def register():
    '''Register all class based plugins.

    Uses the fact that a class knows about all of its subclasses
    to automatically initialize the relevant plugins
    '''

    _plugin_registry.clear()

    ##LOGGER.debug("Subclasses: %s", ' '.join([str(s) for s in PluginBase.__subclasses__()]))

    for plugin in PluginBase.__subclasses__():

        ## Verify completeness of plugin in terms of interface implementation
        try:
            test = plugin()
        except TypeError as e:
            LOGGER.error('Could not register plugin %s: %s', plugin, e)
        else:
            ## Plugin is good.
            LOGGER.info('Registering plugin: %s', plugin)
            _plugin_registry[plugin.get_code()] = plugin


def initialise():
    '''Find and register available plugins.'''

    if not _plugin_registry:
        find()
        register()


def get_codes():
    '''Return a list of all plugin codes.'''

    return list(_plugin_registry.keys())


def get_plugins():
    '''Return a list of all plugin classes.'''
    return list(_plugin_registry.values())


def instantiate(plugin_code, *args, **kwargs):
    '''Return an instantiated plugin, referenced by code.
    Returns None if no such code exists.'''

    if plugin_code in _plugin_registry:
        return _plugin_registry[plugin_code](*args, **kwargs)
    else:
        return None
