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
3. Check the `secrets` and `time_zone` keys in the `/config/appdaemon/appdaemon.yaml` file
4. Copy `vodafone_station_restarter.py` to `/config/appdaemon/apps/`
````bash
git clone git@github.com:G0RIAN/VodafoneStationRestarter.git
cp ./VodafoneStationRestarter/vodafone_station_restarter.py /config/appdaemon/apps/
````
5. Copy the app config to your `apps.yaml` and set the password (directly or in `secrets.yaml` under the `router_password` key:
```bash
cat ./VodafoneStationRestarter/apps.yaml >> /config/appdaemon/apps/apps.yaml
```
or add it manually
```yaml
vodafone_station_restarter:
    module: vodafone_station_restarter
    class: VodafoneStationRestarter
    password: !secret router_password           # password to the Vodafone Station (may use HA secrets), required
    restart_time: 05:00:00                      # timestamp when to restart the vodafone station (HH:MM:SS), optional
    router_ip: 192.168.0.1                      # IPv4 address of the Vodafone Station, optional
                                                # IPv6 or mDNS should work too, but is untested
                                                # e. g. "["1234:abcd::1]" or "kabelbox.local"
    timeout: 10                                 # time in seconds to wait before aborting, optional
    time_step: 0.1                              # time step in seconds between checking if page is loaded, optional
```

[caiconkhicon]: https://github.com/caiconkhicon/vodafone-station-restart
[appdaemon4]: https://github.com/hassio-addons/repository/tree/master/appdaemon
