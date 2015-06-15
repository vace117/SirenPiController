# Raspberry Pi Siren Controller
This is a Raspberry Pi script for controlling an AC powered siren light. The script drives a GPIO pin, which in turn controls the power switching circuitry. 

Users can communicate with this script by sending commands via a TCP/IP socket. The script will listen on port 8080.

There are only 2 commands:
 - SIREN_ON
 - SIREN_OFF

If the command is executed successfully, the script will respond to the caller with an `OK` message. Otherwise `FAIL` is sent.

## Installation Prerequesites
In order to run this Pythin script, you'll need to do the following on your Raspberry Pi:
* `apt-get install python3-flufl.enum`
* `apt-get install python3-setuptools`
* `apt-get install python3-dev`
* `wget https://pypi.python.org/packages/source/n/netifaces/netifaces-0.10.4.tar.gz`
* `tar zxvf netifaces-0.10.4.tar.gz`
* `python3 setup.py install`

## Running the script
`./SirenServer.py`

## Testing the script
You can test the script by connecting to it with netcat:
`netcat <ip of the RPi> 8080`

Here you can type a command and press [Enter] to indicate the end of the command.
