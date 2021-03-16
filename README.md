# Franklin T9 API
A Python wrapper for the Franklin T9 Mobile Hotspot admin API.

## Installation

Copy/paste `frankie.py`. If there is sufficient interest I may upload to PyPi.

## Usage

These APIs have only been tested on firmware revision `R717F21.FR.891`. I recommend following snt.sh's [guide](https://snt.sh/2020/09/rooting-the-t-mobile-t9-franklin-wireless-r717/) on rooting the Franklin T9 to downgrade versions.

**Proceed at your own risk. Using this tool may brick your device or allow you to make modifications considered illegal in some jurisdictions. Any changes you make are your own responsibility.**

### Example
```python
from frankie import get_about
print(get_about())
# prints iccid, imei, imsi, ip_address, mac_address, wifi_name, wifi_password, and more
```

See `frankie.py` for a complete list of APIs available.

[Examples](./examples) are also available.

### Use Cases

* Change APN settings based on which sim card is inserted
* Change wifi settings based on time of day
* See which band priority gets you the best speeds

## Dependencies

The only dependency is requests. 

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

### Contributors
This project was inspired by the [article](https://snt.sh/2020/09/rooting-the-t-mobile-t9-franklin-wireless-r717/) about rooting the Franklin T9 on snt.sh. Big thanks for all the work they did.

## License
[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)
