Spotlight on Technology AirPi and Zombie Detector
=================================================

A Raspberry Pi weather station and air quality monitor.

This is a modified version of the original code for the project. The original code is located at http://airpi.es The spotlight version is located at http://spotlight16.dow.catholic.edu.au

Currently it is split into airpi.py, as well as multiple input and multiple output plugins. airpi.py collects data from each of the input plugins specified in sensors.cfg, and then passes the data provided by them to each output defined in outputs.cfg. The code for each sensor plugin is contained in the 'sensors' folder and the code for each output plugin in the 'outputs' folder. The original code did not use thingspeak this version does.

All of this code is based on the work of Tom Hartley and team. I have only modifed it to suit the Spotlight competition. I have decided to for the code as this version will probably not go further

Some of the files are based off code for the Raspberry Pi written by Adafruit: https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code

For competition instructions, see http://spotlight16.dow.catholic.edu.au/competitions/raspberrypi
##  Installation

### 1 Prerequisites
For the Raspberry Pi make sure your system is able to compile Python extensions and you also need some other modules to drive the airpi board. You will need to install the following dependencies:

```
cd ~
sudo apt-get update
sudo apt-get install build-essential git-core python-dev python-pip python-smbus libxml2-dev libxslt1-dev python-lxml i2c-tools
```

and
```
sudo pip install rpi.gpio requests
```

This version of the Airpi Code does not require the ees code

### 2 Set up the i2c code

To set up i2c, first add your user to the i2c group.  For example, if your username is "pi":
```
sudo adduser pi i2c
```

Now, add the modules needed.
```
sudo nano /etc/modules
```

Add the following two lines to the end of the file:

```
i2c-bcm2708
i2c-dev
```

Exit by pressing CTRL+X, followed by y to confirm you want to save, and ⏎ (enter) to confirm the filename.

Finally, unblacklist i2c by running the following command:
```
sudo nano /etc/modprobe.d/raspi-blacklist.conf
```
Add a `#` character  at the beginning of the line `blacklist i2c-bcm2708`. Then exit in the same way as last time.

Now, reboot your Raspberry Pi:
```
sudo reboot
```
##### 2.1 Board Version

Let's check to see which board version you have.  Run:
```
sudo i2cdetect -y 1
```
You should see this as the output:

```
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- -- 
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
70: -- -- -- -- -- -- -- 77
```


If not, run:
```
sudo i2cdetect -y 0
```

and you should see the above.  This tells you if your board is version 0 or 1.  This is important for the "configuring the airpi" step.

### 3 Get the Adafruit DHT code
Go to https://github.com/adafruit/Adafruit_Python_DHT Install the library by downloading with: 
```
cd ~/git
git clone https://github.com/adafruit/Adafruit_Python_DHT.git
cd Adafruit_Python_DHT
```
and executing:
```
sudo python setup.py install
```


### 4 Get The AirPi Code

Clone this repo into your git directory (or wherever you want):

```
cd ~/git
git clone https://github.com/alanibbett/Spotlight-AirPi.git
cd Spotlight-AirPi
```

### 5 Configuring

Edit the settings file by running:

`nano sensors.cfg`

The start of the file should look like this:

```
[BMP085-temp]			;Barometric Pressure Sensor
filename=bmp085		;Load the correct python file	
enabled=on			;Switch it on (only switch it on if you have the sensor)
measurement=temp		;Tell the module to measure temperature
i2cbus = 1			;tell Python where the module is located could be 1 or 0. Usually 1
fieldID = field7		;Tell Thingspeak which field this reading goes in to.

[BMP085-pres]			;Barometric Pressure Sensor. note we have called this a seperate section
filename=bmp085		;load the file
enabled=on			;switch it on
measurement=pres		;tell it to measure pressure
mslp=on				;tell the module to calulate the pressure as mean sea level pressure. Turn this off for local pressure
i2cbus = 1			;tell the module where the module is located
altitude=40			; for mlsp we need to know our altitude
fieldID = field4		;Tell thingspeak which field to put this in

[MCP3008]			     ;this is the analog to digital converter module
filename=mcp3008		;load the module for the correct module file
enabled=on			;switch it on. Note: this module is essential for all analog to digital conversions

[DHT22]				;DHT 22 humidity and temperatue module
filename=dht22
enabled=on
measurement=humidity	; tell it to measure humidity
pinNumber=4			; the the Pi which pin the module is connected to
fieldID=field2			; tell thingspeak what field the humidity is stored in

[DTH22T]			     ;create a new section for the DHT22 to read the temperature
filename=dht22			;load the module
enabled=on			;switch it on
measurement=temperature		;tell it to measure temperature
pinNumber=4			; locate the device
fieldID=field1			; store the output in field one on thingspeak

[LDR]
filename=analogue
enabled=on
pullUpResistance=10000
measurement=Lux
adcPin = 0
sensorName = LDR
fieldID = field6


[UVI]
filename=analogue
enabled = on
measurement =UVI
adcPin = 4
sensorName =UVI
fieldID = field3

[TGS2600]			     ; Air pollution sensor
filename=analogue		; use the analogue module
enabled=on			; switch it on
pullDownResistance=22000	; tell the module what the pull down resistance is in ohms
measurement=Smoke_Level	; name the reading
adcPin=1			     ; tell the pi which adc pin the sensor is on
sensorName=TGS2600		; name the sensor
fieldID=field5			; store the value in field 5.
```
Press CTRL+X to exit the file, when prompted, press "y" to save the file.
NOTE: for the BMP085 sensor if your board version is "0" change both instances of `i2cbus = 1` to `i2cbus = 0`

If you want to push the data to Thingspeak, edit the `outputs.cfg` file:

`nano outputs.cfg`

The start of the file should look like this:
```
[Print]			;section heading. The [print] section prints the staus on the screen
filename=print		; the filename of the module to load. Do not change
enabled=on		; to switch this on set enabled to on to switch it off set it to off

[Xively]		;This is another IoT service but it's not free so don't use it
filename=xively
enabled=off
APIKey=YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY
FeedID=XXXXXXXXXX

[Thingspeak]		     ;YAY! here is our IoT service name
filename=thingspeak	     ;load the thingspeak module from the folder
enabled=on		     ;Switch it on
APIKey= xxxxxxxxxxxxxx   ;This is you channel 1 WRITE API Key

#you can write to your second channel by copying the entire 
#Thingspeak section and renaming it [Thingspeak2]
#change your write key to the channel 2 write key

```
For this project we will keep the xively feed off and switch on the thingspeak module.

## 6   Running

AirPi **must** be run as root.

```
cd ~/git/Spotlight-Airpi/

sudo python ./airpi.py

```

If everything is working, you should see output similar to this:

```
Success: Loaded sensor plugin BMP085-temp
Success: Loaded sensor plugin BMP085-pres
Success: Loaded sensor plugin MCP3008
Success: Loaded sensor plugin DHT22
Success: Loaded sensor plugin LDR
Success: Loaded sensor plugin MiCS-2710
Success: Loaded sensor plugin MiCS-5525
Success: Loaded sensor plugin Mic
Success: Loaded output plugin Print
Success: Loaded output plugin Thingspeak

Time: 2014-06-04 09:10:18.942625
Temperature: 30.2 C
Pressure: 992.55 hPa
Relative_Humidity: 35.9000015259 %
Light_Level: 3149.10025707 Ohms
Nitrogen_Dioxide: 9085.82089552 Ohms
Carbon_Monoxide: 389473.684211 Ohms
Volume: 338.709677419 mV
Uploaded successfully

```
