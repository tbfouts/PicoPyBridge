from machine import Pin
import json
import time

# Rotary encoder on GP0 (CLK) and GP1 (DT)
clk = Pin(0, Pin.IN, Pin.PULL_UP)
dt = Pin(1, Pin.IN, Pin.PULL_UP)

# Button 1 (GP15) = eco theme, Button 4 (GP13) = sport theme
button_eco = Pin(15, Pin.IN, Pin.PULL_UP)
button_sport = Pin(13, Pin.IN, Pin.PULL_UP)

# LEDs on GP14 and GP10
led = Pin(14, Pin.OUT)
ledTwo = Pin(10, Pin.OUT)

speed = 0
prev_clk = clk.value()
prev_eco = 1
prev_sport = 1
last_sent = {}

while True:
    # Rotary encoder: adjust speed 0-160
    val_clk = clk.value()
    if val_clk != prev_clk:
        if dt.value() != val_clk:
            speed = max(0, speed - 1)
        else:
            speed = min(160, speed + 1)
    prev_clk = val_clk

    # Gear based on speed
    if speed == 0:
        gear = "N"
    elif speed <= 30:
        gear = "1"
    elif speed <= 55:
        gear = "2"
    elif speed <= 80:
        gear = "3"
    elif speed <= 110:
        gear = "4"
    elif speed <= 140:
        gear = "5"
    else:
        gear = "6"

    state = {"mphValue": str(speed), "gear": gear}

    # Eco button: switch theme on release
    val = button_eco.value()
    if prev_eco == 0 and val == 1:
        state["theme"] = "eco"
        led.on()
        ledTwo.off()
    prev_eco = val

    # Sport button: switch theme on release
    val = button_sport.value()
    if prev_sport == 0 and val == 1:
        state["theme"] = "sport"
        led.off()
        ledTwo.on()
    prev_sport = val

    # Send only changed values
    delta = {k: v for k, v in state.items() if last_sent.get(k) != v}
    if delta:
        print(json.dumps(delta))
        last_sent.update(delta)

    time.sleep(0.002)
