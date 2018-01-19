# Wemos D1 relay webserver
Micropython code that toggles a relay using wemos d1 mini

Some electrical assembly required :)

# WARNING
Only mess with high current if you really really know what you are doing. If
not certified to do so please refrain from it. It can definitely kill you,
which is not a desired outcome for any hobby project.


# Problem statement (here, insert your personal problem)
So you got an electic blanket and that greatly improved your quality of life!
Its great going to sleep to a nice warm bed in the middle of winter.
But! You have to get up from the couch where you are watching a film all cuddled
up with your wonderful significant other and turn them on an hour before since they
need some time to warm up. Or do you?

# Solution
Using a simple relay operated through a simple api things can be as easy as clicking
on a button, or even better not doing anything since your home automation solution
can enable things on a schedule or based on the room temperature. Sweet!



# Requirements
[wemos d1 mini](https://www.aliexpress.com/item/D1-mini-Mini-NodeMcu-4M-bytes-Lua-WIFI-Internet-of-Things-development-board-based-ESP8266-by/32644199530.html)

[a compatible relay](https://www.aliexpress.com/item/Smart-Electronics-Relay-Shield-for-Wemos-D1-mini-Relay-Module-Free-shipping/32664403256.html)

[220v to 5v power converted](https://www.aliexpress.com/item/5V-700mA-3-5W-AC-DC-Precision-Buck-Converter-AC-220v-to-5v-DC-step-down/32649591757.html)


# Physical Connection

The relay is just stacked on top of the wemos d1. You can see pictures of the connectivity under the images directory [here](images)


# Schematics

Images in png format and a fritzing project can be found under [schematics](schematics)


# Configuration

Rename configuration_sample.json to configuration.json and edit accordingly.
 Everything else should just work out of the box.

# Security

Please refrain from joining this wemos d1 on a unsecure wireless network or either you will probably end up being a victim of cyber crime.
 Probably you want to assign this wemos d1 on a seperate wireless network by making use of seperate SSIDs, VLANs and advanced firewall rules.

Furthermore this project has some basic security measures already built in, for instance by using a simple (but yet effective) token mechanism in the HTTP payload.


# Custom micropython required

To load this project the wemos d1 needs to be running micropython and you
could probably use ampy.

This code uses the amazing uhttpd library by **Fred Dushin** found [here](https://github.com/fadushin/esp8266/tree/master/micropython/uhttpd).

This library provides a framework with which proper web development can be
done on the wemos d1 based on asyncio. The only downside is that it cannot be
 loaded on an existing micropython due to memory constrains and needs to be
 frozen in order to be usable.

I have already frozen the library on a custom 1.8.7 micropython which can be
found [here](firmware/esp8266-20170517-v1.8.7-uhttpd.bin). If someone does
not trust downloading binaries (and you very well should not) step by step
instructions to building one can be found [here](documentation/freezing_uhttpd.md)

# Flashing micropython

Required tools:

   [esptool](https://github.com/espressif/esptool) (Follow installation instructions)

  With the board connected to a usb port of your linux box assuming that the
  port is ttyUSB0 (check with dmesg after connecting to see what is assigned)

    esptool.py --port /dev/ttyUSB0 erase_flash
    esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 MICROPYTHON_FIRMWARE_FOR_ESP8266+uhttpd.bin

  I have had some d1 boards having trouble flashing with the above with
  garbage on the serial and the led staying on. On those boards this command
  works.

    esptool.py --port /dev/ttyUSB0 write_flash -fm dio -fs 32m 0 MICROPYTHON_FIRMWARE_FOR_ESP8266+uhttpd.bin


# Loading the project

Required tools:

   [ampy](https://github.com/adafruit/ampy) (Follow installation instructions)

    export AMPY_PORT=/dev/ttyUSB0
    ampy put library
    ampy put configuration.json
    ampy put main.py
    ampy put boot.py

# Checking output

   On an ubuntu box you can fire off a few curl commands to see how the board
    behaves

    for time in `seq 1000`
        do
        curl -H "Content-Type: application/json" -X POST -d '{"token":"<YOUR_TOKEN>","state":true}' http://STATIC_IP_SUPPLIED_BY_ROUTER/api/relay
        sleep 1
        curl -H "Content-Type: application/json" -X POST -d '{"token":"<YOUR_TOKEN>","state":false}' http://STATIC_IP_SUPPLIED_BY_ROUTER/api/relay
        sleep 1
        done

   You can find STATIC_IP_SUPPLIED_BY_ROUTER by checking the serial console output where the ip
    will be printed with

    screen /dev/ttyUSB0 115200

   The above code will turn the relay on and off for a thousand
    times with a second of delay in between.

   You also have the possibility to just give a pulse signal on the relay switch. This can become quite handy when you just want to close a circuit (i.e. using it for an automatic garage door opener) and simulate a button press.
    In the JSON payload, use state: "pulse" and you're all set. The relay will turn on, pauses for 1 second and finally turns off.

# Integrating with [Home Assistant](https://home-assistant.io/)

 In order to integrate with home assistant you need to add an entry for a
 RESTfull switch like below:

    - platform: rest
      resource: "http://STATIC_IP_SUPPLIED_BY_ROUTER/api/relay"
      name: "NAME OF THE SWITCH FOR THE UI"
      body_on: '{"state": true}'
      body_off: '{"state": false}'
