# Python Hubitat Data Logging

There exists other logging options out there that utilize something call "node-red" to capture and store data in
InfluxDB. While interesting, I couldn't really do much with it because I know nothing about Node programming. So, I took
the general format and layout and converted it all to Python. 

The general data flow goes something like this: `hubitat => python => influx` and then you can use graphana on top of
that to view the data.

## TODO

 - make logging dynamic. Load log path from the `.env` file.
 - update README with system status
