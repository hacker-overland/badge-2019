"""Top-level logic here."""
import binascii
import gc
import neopixel
import network
import random
import time
import ubinascii
import ujson
import _thread
from machine import Pin
from machine import I2S

from features import Raccoon, Bat, Truck, Smoke


__author__ = "ashmastaflash"

CONFIG = {"friendlies": {"E4:8D:8C:45:72:E5": "raccoon",
                         "E4:8D:8C:45:72:E6": "smoke",
                         "E4:8D:8C:45:72:E4": "truck",
                         "E4:8D:8C:45:72:B5": "bat"}}

FEATURES = {"raccoon": {"pixels": [0, 1],
                        "filename": "raccoon.wav",
                        "lights": Raccoon},
            "truck": {"pixels": [2],
                    "filename": "truck.wav",
                    "lights": Truck},
            "bat": {"pixels": [3],
                      "filename": "bat.wav",
                      "lights": Bat},
            "smoke": {"pixels": [4],
                      "filename": "smoke.wav",
                      "lights": Smoke}}
BADGES_OBSERVED = set([])

MY_ROLE = None
DEFAULT_AUDIO_FILE = "default.wav"
AUDIO_THRESHOLD = 4

# LED strip configuration
# number of pixels
PIXELS = 5
# strip control gpio
CONTROL = 5
NP = neopixel.NeoPixel(Pin(PIXELS), CONTROL, bpp=3)

LOCAL_LEVEL = 0

# I2S STUFF
BCK_PIN = Pin(14)
WS_PIN = Pin(13)
SDOUT_PIN = Pin(12)

AUDIO_OUT = I2S(I2S.NUM1,
                bck=BCK_PIN,
                ws=WS_PIN,
                sdout=SDOUT_PIN,
                standard=I2S.PHILIPS,
                mode=I2S.MASTER_TX,
                dataformat=I2S.B16,
                channelformat=I2S.ONLY_RIGHT,
                samplerate=16000,
                dmacount=16,
                dmalen=512)

def main():
    global CONFIG
    global LOCAL_LEVEL
    global BADGES_OBSERVED
    global FEATURES
    indexen = [0, 1, 2, 3, 4]
    CONFIG.update(config_from_file("config.json"))
    lights_down(indexen)
    _thread.start_new_thread(sound_handler, ())
    _thread.start_new_thread(light_handler, ())
    _thread.start_new_thread(network_handler, ())
    friendlies = [str(x, 'utf-8') for x in CONFIG["friendlies"]]
    print("Friendlies:")
    for friend in friendlies:
        print(friend)
    while True:
        time.sleep(120)
        if MY_ROLE:
            print("I am a %s!" % MY_ROLE)
        else:
            print("Existential crisis! I know not what I am!")
    return


def sound_handler():
    """Handle sound features."""
    print(">> Starting sound handler...")
    global MY_ROLE
    global DEFAULT_AUDIO_FILE
    while True:
        try:
            my_audio = FEATURES[MY_ROLE]["filename"]
            f = open(my_audio, "r")
            my_file_exists = True
            f.close()
        except OSError:
            print("%s does not exist" % my_audio)
            my_file_exists = False
        except KeyError:
            print("Bad role: %s" % MY_ROLE)
            my_file_exists = False
        if my_file_exists:
            effective_audio = my_audio
        else:
            effective_audio = DEFAULT_AUDIO_FILE
        print(">> Local level: {}".format(LOCAL_LEVEL))
        if LOCAL_LEVEL >= AUDIO_THRESHOLD:
            print(">> BEEP")
            with open(effective_audio) as audio_file:
                samples = bytearray(audio_file.read(1000))
                read_count = 1000
                while samples:
                    print("Read {}".format(read_count))
                    AUDIO_OUT.write(samples)
                    gc.collect()
                    samples = bytearray(audio_file.read(1000))
                    read_count += 1000
            print(">> DONE_BEEPING")
            time.sleep(30)
        time.sleep(30)


def light_handler():
    """Handle light feature state changes."""
    print(">> Starting light handler...")
    global BADGES_OBSERVED
    global FEATURES
    badge_count = len(BADGES_OBSERVED)
    pixels = [0, 1, 2, 3, 4]
    iter_settings = {x: (0, 0, 0) for x in pixels}
    while True:
        gc.collect()
        feature_generators = [FEATURES[x]["lights"](badge_count,
                                                    FEATURES[x]["pixels"]).generator()
                              for x in BADGES_OBSERVED]
        badge_count = len(feature_generators)
        print("badge_count: %s" % badge_count)
        while len(feature_generators) == badge_count:
            badge_count = len(BADGES_OBSERVED)
            for feature_generator in feature_generators:
                iter_settings.update(next(feature_generator))
            for pixel in pixels:
                settings = iter_settings[pixel]
                cleaned = tuple([int(x) for x in settings])
                NP[pixel] = cleaned
                NP.write()
            time.sleep_ms(100)


def network_handler():
    """Scan wireless LAN, return BSSIDs."""
    global MY_ROLE
    global BADGES_OBSERVED
    global LOCAL_LEVEL
    access_point = network.WLAN(network.AP_IF)
    station = network.WLAN(network.STA_IF)
    sleep_factors = {1: 10, 2: 15, 3: 60, 4: 600}
    friendlies = [str(x, 'utf-8') for x in CONFIG["friendlies"]]
    password = binascii.b2a_base64(str(random.getrandbits(30)))
    access_point.active(True)
    access_point.config(authmode=4, password=password)
    my_bssid = str(ubinascii.hexlify(access_point.config("mac")), "utf-8")
    while True:
        station.active(True)
        scan_results = [str(ubinascii.hexlify(x[1]), "utf-8")
                        for x in access_point.scan()]
        scan_results.append(my_bssid)
        print("I am {}".format(my_bssid))
        print("I observe %s" % ", ".join(scan_results))
        try:
            MY_ROLE = CONFIG["friendlies"][my_bssid]
        except KeyError:
            MY_ROLE = None
        BADGES_OBSERVED = {CONFIG["friendlies"][x]
                           for x in scan_results
                           if x in friendlies}
        LOCAL_LEVEL = abs(len(BADGES_OBSERVED))
        password = binascii.b2a_base64(str(random.getrandbits(30)))
        access_point.active(True)
        access_point.config(authmode=4, password=password)
        if LOCAL_LEVEL in sleep_factors:
            sleep_this_time = sleep_factors[LOCAL_LEVEL]
        else:
            sleep_this_time = 120
        time.sleep(sleep_this_time)


def lights_down(indexen):
    """Turn off LEDs for each index in indexen."""
    for i in indexen:
        NP[i] = (0, 0, 0)
        NP.write()


def config_from_file(file_name):
    """Load and return json from file."""
    with open(file_name) as config_file:
        config = ujson.load(config_file)
    return config

main()
