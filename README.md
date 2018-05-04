# GoPiGo Scratch Extension

Control the Raspberry Pi expansion board *[GoPiGo3](https://www.dexterindustries.com/gopigo3/)* from the programming language *[Scratch](https://en.wikipedia.org/wiki/Scratch_(programming_language))*. *[ScratchX](http://scratchx.org/#scratch)* and the *Scratch 2 Offline Editor* are supported.

The GoPiGo3 is made by [Dexter Industries](https://www.dexterindustries.com/). Scratch was developed by the [MIT Media Lab](https://www.media.mit.edu/).

## Features

The following GoPiGo3 or Raspberry Pi features are supported by the Scratch extension:

* GoPiGo3 motion control
  * drive forward/backward specific distance at specific speed and then stop
  * drive forward/backward at specific speed until another motor command is sent
  * turn given degrees to the left/right at specific speed and then stop
  * turn to the left/right at specific speed until another motor command is sent
  * set speed and direction for left and right motor individually and maintain until another motor command is sent
  * stop motors
* Servo control
  * set position (0..180 degrees) for servo motors connected to Servo 1 or Servo 2 connectors
* Distance sensor
  * read distance in cm
* Blinkers (two red LED lights at the front of the GoPiGo3 board)
  * turn on/off individually or both at the same time
* Eyes (two RGB LED lights on top of GoPiGo3 board)
  * control individually or both eyes at the same time
  * set color and brightness by specification of RGB components

![Scratch Blocks](images/scratch_blocks.png)

## Compatibility

Tested with
* *Raspberry Pi 3 Model B*
* *GoPiGo3*
* *[Servo](https://www.dexterindustries.com/shop/servo-package/)*
* *[Distance Sensor](https://www.dexterindustries.com/shop/distance-sensor/)*
* *Rasbian Stretch with Desktop* Version *April 2018* with latest updates as of 03-May-2018
* *Python libraries for GoPiGo3* as of 03-May-2018
* *ScratchX* as of 03-May-2018
* *Scratch 2 Offline Editor* (as it comes with Raspbian, as of 03-May-2018)

## Approach

This extension comes with a server that needs to run on the Raspberry Pi that has the GoPiGo3 board attached to it. The server exposes expansion board functionality through HTTP endpoints. It uses GoPiGo3 Python libraries to control the board. In Scratch an extension needs to be loaded. The extension exposes board functionality as additional Scratch blocks. Scratch can be running on the same computer as the server, or a different one. It needs to be able to connect to the server.

## Installation

### Rasbian

Download and install the latest [Rasbian](https://www.raspberrypi.org/downloads/raspbian/).

Update Rasbian with
 ```
 $ sudo apt update
 $ sudo apt upgrade
 ```

### Enable SPI and I2C interfaces

The *Serial Peripheral Interface* (SPI) bus is used for communication between Raspberry Pi and GoPiGo3 board. The *Inter-Integrated Circuit* (I2C) bus can be used to connect I2C devices (e.g. distance sensor) to the Raspberry Pi. The GoPiGo3 board provides two I2C [Grove](http://wiki.seeedstudio.com/Grove_System/) connectors that are directly connected to the Raspberry Pi.

Per default the SPI and I2C interface are disabled in Raspbian. To enable the interfaces go to menu *Preferences* > *Raspberry Pi Configuration*, tab *Interfaces*. Make sure the interfaces *SPI* and *I2C* are enabled.

### Python libraries for GoPiGo3 and sensors

See https://github.com/DexterInd/GoPiGo3 for details.

```
$ sudo sh -c "curl -kL dexterindustries.com/update_gopigo3 | bash"
```

Install DI_sensors (https://github.com/DexterInd/DI_Sensors)

```
$ cd ~
$ git clone https://github.com/simonmonk/raspirobotboard3.git
$ cd raspirobotboard3/python
$ sudo python setup.py install
```

### Scratch extension

```
$ cd ~
$ git clone https://github.com/markokimpel/rrbscratchextension.git
```

## Use Scratch

First, the server needs to be started.

```
$ cd ~/rrbscratchextension/rrbserver/
$ ./run.sh
Server listening at 0.0.0.0:8080

RRB3 Server homepage : http://<your_ip_addr>:8080/
Scratch extension URL: http://<your_ip_addr>:8080/scratch_extension.js

Press Ctrl-C to stop server
```

Open the RRB Server homepage with your browser to see detailed instructions on how to load the extension in ScratchX and the Scratch 2 Offline Editor.

![Scratch screenshot](scratch_screenshot.png)

There also is a Controller UI that allows you to control the board manually from your browser - great for testing.

![Controller UI](rrb3_controller.png)

# Limitations

TODO

# Security

The server exposes expansion board functionality through unsecured HTTP endpoints. Everyone with access to the endpoints can control the board. The server needs to be run in a network that guards against unauthorized access.

# License

* Copyright 2018 Marko Kimpel
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*     http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
