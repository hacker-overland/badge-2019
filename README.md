# Hacker Campers Badge 2019

Blog post: https://ash-wilson.com//blog/hardware/badgelife/defcon/2019/08/16/Thats-How-They-Get-You.html

## Parts list

Board files located in this repo under `boards/`, or use the links below to
order directly from https://oshpark.com.

| qty | Name                 | Link                                         |
|-----|----------------------|----------------------------------------------|
| 1   | ESP32 breakout board | https://www.adafruit.com/product/4172        |
| 5   | Neopixel LEDs        | https://www.sparkfun.com/procucts/12986      |
| 1   | I2S audio codec      | https://www.sparkfun.com/procucts/14809      |
| 1   | Speaker              | https://www.sparkfun.com/procucts/15350      |
| 1   | 3xAA Battery box     |                                              |
| 1   | Front plate          | https://oshpark.com/shared_projects/XpUuSjO7 |
| 1   | Back plate           | https://oshpark.com/shared_projects/cNtZyBs1 |
| 6   | M2 screws            |                                              |
| 3   | M2 spacers           |                                              |
| 1   | Power switch         | https://www.sparkfun.com/procucts/102        |
| 1   | Lanyard              |                                              |
| 1   | SAO connector        |                                              |
| 3   | AA batteries         |                                              |

## Build requirements

Only install this if you don't want to do it the easy way. Otherwise, follow
the directions under the `Loading Firmware` section, below.

* ESP IDF
   * https://github.com/espressif/esp-idf
   * Commit `5c88c5996dbde6208e3bec05abc21ff6cd822d26`
* Micropython (Mike Teachman's I2S mod)
   * https://github.com/miketeachman/micropython
   * Commit `6b023290f6dbccfdb427857120cd12c292e622f2`
* ampy (file transfer tool)
* esptool


## Assembly

* Orientation reference: corner without M2 hole goes down and to the right.
* Install LEDs (flat side goes to the right, or down)
* Install power switch in the upper-left corner
* Install SAO connector on the rear of the plate, with the slot UP
* Install I2S audio codec
   * Solder two wire leads to the plate, for the speaker leads.
   * Solder a 7-pin header onto the board
   * Situate the codec on the two speaker leads and pin header, solder down.
* Install the ESP32
   * On the bottom row, and starting from the far right and moving to the left:
      * Solder five leads into the plate, skipping the first hole on the right.
   * On the top row, solder a lead into the second hole from the far right.
   * On the top row, solder a lead for GPIO pin \#5. Use the ESP32 to align.
   * Solder pin headers onto ESP32 breakout board, with pins facing up.
   * Situate the ESP32 on the leads and solder down.
* Load firmware onto the ESP32 (see `Loading firmware`, below) and confirm functionality.
* Solder battery box leads to the bottom plate, with the red lead closest to the M2 hole in the upper left corner.
* Use 2-sided tape to attach the battery box to the back of the bottom plate.
* Use a hot glue gun to fill holes in top plate, creating diffusers for LEDs
* Use the screws and spacers to attach the top plat to the bottom plate

![Badges](https://ash-wilson.com/blog/images/hacker_overland_v4.jpg)


## Loading firmware (Ubuntu 18.04, Docker)

* Configure roles (by mac address) in `source/configs/config.json`
* Build the Docker container: `docker build -t flasher:latest .`
* Plug in USB TTY (Assuming it will show up as `/dev/ttyUSB0`)
* Restart ESP32 in ROM serial bootloader mode.
* Flash the badge `docker run -it --rm  --device=/dev/ttyUSB0 builder`
* Follow directions on-screen. You will need to re-enter bootloader mode after flash is cleared.
