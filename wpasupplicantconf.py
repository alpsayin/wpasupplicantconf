from collections import OrderedDict
from pathlib import Path
from typing import Union
from io import IOBase


DEFAULT_WPA_SUPPLICANT_FILEPATH = Path('/etc/wpa_supplicant/wpa_supplicant.conf')


class ParseError(ValueError):
    pass


class WpaSupplicantConf:
    """This class parses a wpa_supplicant configuration file, allows
    manipulation of the configured networks and then writing out of
    the updated file.

    WARNING: Although care has been taken to preserve ordering,
    comments will be lost for any wpa_supplicant.conf which is
    round-tripped through this class.
    """

    def __init__(self, lines=None, filepath=None):
        self._fields = OrderedDict()
        self._networks = OrderedDict()
        self._comments = list()
        self._lines = lines
        if filepath is not None:
            with open(filepath, 'r') as rfid:
                self._lines = rfid.readlines()
            self.filepath = Path(filepath)
        else:
            self.filepath = None
        self.reload()

    def reload(self):
        network = None
        for linenumber, line in enumerate(self._lines):
            line = line.strip()
            if not line or line.startswith('#'):
                self._comments.append((linenumber, line))
                continue

            if line == "}":
                if network is None:
                    raise ParseError("unxpected '}'")

                ssid = network.pop('ssid', None)
                if ssid is None:
                    raise ParseError('missing "ssid" for network')
                self._networks[dequote(ssid)] = network
                network = None
                continue

            parts = [x.strip() for x in line.split('=', 1)]
            if len(parts) != 2:
                raise ParseError("invalid line: %{!r}".format(line))

            left, right = parts

            if right == '{':
                if left != 'network':
                    raise ParseError('unsupported section: "{}"'.format(left))
                if network is not None:
                    raise ParseError("can't nest networks")

                network = OrderedDict()
            else:
                if network is None:
                    self._fields[left] = right
                else:
                    network[left] = right

    def fields(self):
        return self._fields

    def networks(self):
        return self._networks

    def add_network(self, ssid, **attrs):
        self._networks[ssid] = attrs

    def remove_network(self, ssid):
        self._networks.pop(ssid, None)

    def write(self, fid: Union[IOBase, Path, str] = None):
        print(f'fid={fid}')
        if fid is None and self.filepath is not None:
            fid = open(self.filepath, 'w+')
        elif fid is None:
            raise TypeError(f'write() missing 1 required positional argument: fid')
        elif isinstance(fid, str):
            fid = open(Path(fid), 'w+')

        for name, value in self._fields.items():
            fid.write("{}={}\n".format(name, value))

        for ssid, info in self._networks.items():
            fid.write("\nnetwork={\n")
            fid.write('    ssid="{}"\n'.format(ssid))
            for name, value in info.items():
                fid.write("    {}={}\n".format(name, value))
            fid.write("}\n")

        try:
            fid.close()
        except Exception as e:
            print(f'Couldnt close the output file {fid}: {e}')
            pass

    @classmethod
    def default(cls):
        return WpaSupplicantConf(filepath=DEFAULT_WPA_SUPPLICANT_FILEPATH)

    @classmethod
    def from_file(cls, rfilepath: Path):
        return WpaSupplicantConf(filepath=rfilepath)

    @classmethod
    def from_lines(cls, lines):
        return WpaSupplicantConf(lines=lines)


def dequote(v):
    if len(v) < 2:
        return v
    if v.startswith('"') and v.endswith('"'):
        return v[1:-1]
    return v
