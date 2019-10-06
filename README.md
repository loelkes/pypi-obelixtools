# obelixtools

1. Install it with ```pip install obelixtools```

## API

This is a small wrapper I wrote around the requests library. It has some extra features like a speedtest and connectivity check.

### Basic use

```
from obelixtools import API
endpoint = API(url, 'json')
endpoint.query()
print(endpoint.content)
```

### Speedtest and connectivity check

```
% python -m obelixtools
06-Oct-19 11:28:44 - obelixtools - INFO: Performing selftest with https://1.1.1.1
06-Oct-19 11:28:44 - obelixtools - INFO: Connected to the internet.
06-Oct-19 11:28:44 - obelixtools - INFO: Performing speedtest with http://speedtest.belwue.net/100M
06-Oct-19 11:29:11 - obelixtools - INFO: Connection speed is 3MB/sµ
```

### Variables

#### .url : str

The URL of the API.

#### .format : str

Define a certain data format for the data return by the API. This can by either _json_, _xml_ or raw. Any other value will sit it to raw.

#### .content

The content of the API response after postprocessing. Postprocessing happens by setting _.format_

### Methods

#### .query(url : str, optional) -> bool

Fetched the data from the API if the age of the existing data in .content is older than *.last_update*. This timeout is ignored if _url_ is set (useful for speedtests).

#### .check_connection(url='https://1.1.1.1', timeout=5) -> bool

Fetches the given url and and returns True if the servers returns a status code 200 and False otherwise. Comprehensive log messages are passed to the loggin module.

#### .speedtest(url='http://speedtest.belwue.net/100M') -> bool

Downloads the file provided at the given url and returns the speed in bytes per second. The logging module received a log message with humand readable speed (e.g. kB/s, MB/s...)
