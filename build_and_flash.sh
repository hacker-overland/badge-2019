#!/bin/bash
set -xe

##############
# Setup path
. /root/esp/esp-idf/add_path.sh
. /src/assets/set_esp32_path.sh

cd /root/esp/${CTF_PROJECT}
make flash
