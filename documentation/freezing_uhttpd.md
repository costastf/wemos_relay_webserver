# Freezing uhttpd on a custom micropython firmware.

Performed on an ubuntu 16.04

    # create a working directory
    mkdir uhttp_freezing
    cd uhttp_freezing

    # first we need to build the cross compiler toolchain
    git clone https://github.com/pfalcon/esp-open-sdk.git

    # on ubuntu 16.04 there were some libraries required
    sudo apt-get install gperf bison flex texinfo help2man libtool-bin

    # build the toolchain
    cd esp-open-sdk/
    make STANDALONE=y
    # go get coffee, this will take some time
    # once done you need to add it to the path
    cd ..
    export PATH=./esp-open-sdk/xtensa-lx106-elf/bin:$PATH

    # get all other required projects
    git clone https://github.com/micropython/micropython-lib.git
    git clone https://github.com/micropython/micropython.git
    git clone https://github.com/fadushin/esp8266.git

    # go into the modules directory of micropython for esp8266
    cd micropython/esp8266/modules

    # create a directory to handle asyncio files
    mkdir uasyncio

    # create symlinks of all required files in the appropriate place
    ln -s ../../../esp8266/micropython/uhttpd/http_api_handler.py http_api_handler.py
    ln -s ../../../esp8266/micropython/uhttpd/http_file_handler.py http_file_handler.py
    ln -s ../../../esp8266/micropython/logging/ulog.py ulog.py
    ln -s ../../../esp8266/micropython/logging/console_sink.py console_sink.py
    ln -s ../../../micropython-lib/logging/logging.py logging.py
    ln -s ../../../micropython-lib/uasyncio/uasyncio/__init__.py uasyncio/__init__.py
    ln -s ../../../micropython-lib/uasyncio.core/uasyncio/core.py uasyncio/core.py

    # IMPORTANT. Required python version is 3.5+ for micropython.
    # The build will fail with v2.7

    # we get to the root of micropython directory
    cd ../..

    # update all required submodules
    git submodule update --init

    # actually make the build
    make -C mpy-cross
    cd micropython/esp8266
    make axtls
    make

    # once this is done you have a firmware-combined.bin under build directory
    # we copy that to the root of our project
    cp ./build/firmware-combined.bin ../../esp8266-`date +%Y%m%d`-v1.8.7-uhttpd.bin

    # so finally now you should have a esp8266-WHATEVERDATE-v1.8.7-uhttpd.bin
     under the initially created "uhttp_freezing" directory 
