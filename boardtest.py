# Complete project details at https://RandomNerdTutorials.com

from machine import Pin
import machine, neopixel, time
import network


# LED strip configuration
# number of pixels
n = 2
# strip control gpio
p = 5 

def eyes_level(indexen, level, wait):
    """level is 1, 2, 3"""
    if level == 1:
        brightness = 0.2
        color = (16, 8, 0)
    elif level == 2:
        brightness = 0.4
        color = (8, 4, 0)
    elif level == 3:
        brightness = 0.6
        color = (4, 2, 0)
    else:
        raise ValueError("SHITTY USER YOU ARE")
    np = neopixel.NeoPixel(machine.Pin(p), n)
    for i in indexen:
        np[i] = color
    np.write()
    time.sleep_ms(wait)
    for i in indexen:
        np[i] = (0, 0, 0)
        np.write()
    
def scan_stations():
    station = network.WLAN(network.STA_IF)
    station.active(True)
    for ap in station.scan():
        print(ap[0])
    return

def scan_beacons():
    bt = network.Bluetooth()
    bt.start_scan(10)
    time.sleep(10)
    for adv in bt.get_advertisements():
        print(adv)
    return

scan_stations()
eyes_level([0, 1], 1, 2000)
time.sleep(2)
eyes_level([0, 1], 2, 2000)
time.sleep(2)
eyes_level((0, 1), 3, 2000)
