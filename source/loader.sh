cd /root/esp/${UPYTHON_PROJECT_NAME}/ports/esp32
echo ">>>> ERASING FLASH"
make erase
echo ">>>> WRITING IMAGE"
make deploy
###
echo "RESET IT"
sleep 30
cd ${BADGE_SOURCE_PATH}
echo ">>>> COPYING FEATURES"
ampy --port /dev/ttyUSB0 put features.py features.py
echo ">>>> COPYING CONFIG"
ampy --port /dev/ttyUSB0 put ./configs/config.json config.json
echo ">>>> COPYING DEFAULT SOUND"
ampy --port /dev/ttyUSB0 put ./audio/raccoonbadge.wav default.wav
echo ">>>> COPYING MAIN"
ampy --port /dev/ttyUSB0 put main.py main.py
echo "Done!"
