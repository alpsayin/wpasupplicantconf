#!/usr/bin/env python3

import logging
from wpasupplicantconf import WpaSupplicantConf
from typing import Callable


def reload_first(func: Callable) -> Callable:
    def reload_and_perform(*args, **kwargs):
        _self = args[0]
        if not isinstance(_self, WifiConfigWrapper):
            print(
                f'Decorator not compatible with this function; use it on a WifiConfigWrapper\'s member functions')
        if _self.wconf is None:
            print(f'WpaSupplicantConf object is None')
            return None
        else:
            print(f'Reloading WpaSupplicantConf')
            _self.wconf.reload()
            return func(*args, **kwargs)
    return reload_and_perform


class WifiConfigWrapper(object):
    """A simpler class for handling wifi config operations"""
    def __init__(self, filepath=None):
        super(WifiConfigWrapper, self).__init__()
        if filepath is None:
            self.wconf = WpaSupplicantConf.default()
        else:
            self.wconf = WpaSupplicantConf.from_file(filepath)

    @reload_first
    def list(self, *args, **kwargs):
        try:
            return self.wconf.networks()
        except Exception as ex:
            logging.exception(f'Couldnt list wifi networks: {ex}')
            return None

    @reload_first
    def put(self, ssid, key=None, *args, **kwargs):
        try:
            if key:
                self.wconf.add_network(ssid, psk=key, key_mgmt='WPA-PSK')
            else:
                self.wconf.add_network(ssid)
            self.wconf.write()
            return self.wconf.networks()
        except Exception as ex:
            logging.exception(f'Couldnt append wifi network: {ex}')
            return None

    @reload_first
    def remove(self, ssid, *args, **kwargs):
        try:
            self.wconf.remove_network(ssid)
            self.wconf.write()
            return self.wconf.networks()
        except Exception as ex:
            logging.exception(f'Couldnt remove wifi network: {ex}')
            return None

    @reload_first
    def clear(self, *args, **kwargs):
        try:
            ssids = list(self.wconf.networks().keys())
            for ssid in ssids:
                self.wconf.remove_network(ssid)
            self.wconf.write()
            return self.wconf.networks()
        except Exception as ex:
            logging.exception(f'Couldnt clear wifi networks: {ex}')
            return None
