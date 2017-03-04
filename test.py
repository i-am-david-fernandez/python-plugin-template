#!/usr/bin/env python3

import plugin_family

def main():

    plugin = plugin_family.Factory.get('my_plugin')

    print(plugin.get_code())

if __name__ == '__main__':
    main()
