# wpasupplicantconf
Python library for parsing, manipulation and generation of wpa_supplicant.conf files

Like me, you may find yourself a neat module to edit wpa_supplicant.conf file.
Because like me you may go through below steps:
1. I can't be the only one
2. Yes, it's a simple-enough text parsing and editing.
3. Which is exactly the reason why I shouldn't re-invent the wheel.
4. And of course, there must be someone who wrote this and published (thank you @TheCacophonyProject).

## wifi_config_wrapper
This is the extra simple module where things can get wrong easier. But provides a much simpler interface.
Example code below:
```python
wifi = WifiConfigWrapper()  # or you can give it a pathlib.Path or str
wifi_list = wifi.list()

# Returns the list with wifi added or updated depending on the situation
result = wifi_list.put('mywifiname', 'mywifipass')

# Returns the list if removed, will still return a list if wifi doesnt exist
result = wifi_list.remove('mywifiname', 'mywifipass')

# Dangerous
wifi_list.clear()
```


## WpaSupplicantConf
This is the the underlying interface which originally works by reading some lines into memory and then writing to a target file.
I've added the functionality to hold a filepath in class and work with that. Note that, this class is ignorant to changes made outside.
To avoid that, you can use the reload function. 
 - If you do reload without writing first, you'll lose any changes. 
 - And if you do write before reloading, you'll lose the external changes. 

The wrapper above always reloads before any operation. More IO at the expense of *almost* atomic access to wpa_supplicant.
Example code below:
```python
wifi = WpaSupplicantConf.default()  # same as WpaSupplicantConf.from_file('/etc/wpa_supplicant/wpa_supplicant.conf')
initial_fields = wifi.fields()
list_of_networks = wifi.networks()
wifi.add_network(self, 'mywifiname', psk='"mywifipassword"', key_mgmt='WPA-PSK')
wifi.remove_network(self, 'mywifiname')
wifi.write():
```
Example code below:
```python
lines = open('/etc/wpa_supplicant/wpa_supplicant.conf', 'r').readlines()
wifi = WpaSupplicantConf.from_lines(lines)  # uses /etc/wpa_supplicant/wpa_supplicant.conf
list_of_networks = wifi.networks()
wifi.add_network(self, 'mywifiname', psk='"mywifipassword"', key_mgmt='WPA-PSK')
wifi.reload()  # mywifiname wifi is lost now
wifi.remove_network(self, 'anotherwifi')
wifi.write(open('/etc/wpa_supplicant/wpa_supplicant.conf','w'))  # this can take a str, an IOBase or a pathlib.Path
```
