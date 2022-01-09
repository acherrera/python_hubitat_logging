# Python Hubitat Data Logging

There exists other logging options out there that utilize something call "node-red" to capture and store data in
InfluxDB. While interesting, I couldn't really do much with it because I know nothing about Node programming. So, I took
the general format and layout and converted it all to Python. 

The general data flow goes something like this: `hubitat => python => influx` and then you can use graphana on top of
that to view the data.

## Env Configuration

The configuration information is read in from `.env` file. Copy `env_sample.json` and fill in values to get working. In
order to log, it needs the IP address of the Hubitat, the IP address of the InfluxDB instance and the username and
password of the InfluxDB user.


## TODO

 - make logging dynamic. Load log path from the `.env` file.
 - update README with system status
