# VodafoneStationRestarter

Home Assistant AppDaemon 4 script to restart the Vodafone Station (Germany, manufactured by Arris) every night. 
This helps reduce package loss and problems with the buggy Vodafone Station. 

The script is based on the approach by [@caiconkhicon][caiconkhicon].

## Installation & Configuration

1. Install the [Home Assistant AppDaemon 4 add-on][appdaemon4] (if not alredy installed)
2. Add the required system and python packages to the add-on config
```
system_packages:
  - chromium-chromedriver
  - chromium
python_packages:
  - selenium
```
3. Check the path of your `secrets.yaml` file in the `/config/appdaemon/appdaemon.yaml` file
4. Clone the `vodafone_station_restarter.py` to `/config/appdaemon/apps/`
5. Add the new app to your `/config/appdaemon/apps.yaml` and specify the required parameters `module`, `class` and `password`:
```
vodafone_station_restarter:
    module: vodafone_station_restarter          # name of *.py file, required
    class: VodafoneStationRestarter             # class name in *.py file, required
    password: !secret router_password           # password to the Vodafone Station, required
    restart_time: 05:00:00                      # timestamp when to restart the vodafone station (HH:MM:SS), optional
    router_ip: 192.168.0.1                      # IPv4 address of the Vodafone Station, optional
                                                # IPv6 or mDNS should work too, but is untested
                                                # e. g. "["1234:abcd::1]" or "kabelbox.local"
    timeout: 10                                 # time in seconds to wait before aborting, optional
    time_step: 0.1                              # time step in seconds between checking if page is loaded , optional
```

[caiconkhicon]: https://github.com/caiconkhicon/vodafone-station-restart
[appdaemon4]: https://github.com/hassio-addons/repository/tree/master/appdaemon
