from machine import Pin
import json
import time

# Rotary encoder on GP12 (CLK) and GP13 (DT)
clk = Pin(12, Pin.IN, Pin.PULL_UP)
dt = Pin(13, Pin.IN, Pin.PULL_UP)

# Knob press on GP14 (signal) and GP15 (ground reference)
button_press = Pin(14, Pin.IN, Pin.PULL_UP)
button_gnd = Pin(15, Pin.OUT, value=0)

speed = 0
prev_clk = clk.value()
prev_press = 1
last_sent = {}
last_knob_time = time.ticks_ms()
KNOB_DEBOUNCE_MS = 5
step_count = 0
STEPS_PER_CHANGE = 2

# Mode cycling: each press advances to the next mode
modes = ["sport", "eco"]
mode_index = 0

while True:
    # Rotary encoder: adjust speed 0-160 (every 2 steps)
    val_clk = clk.value()
    now = time.ticks_ms()
    if val_clk != prev_clk and time.ticks_diff(now, last_knob_time) > KNOB_DEBOUNCE_MS:
        if dt.value() != val_clk:
            step_count += 1
            if step_count >= STEPS_PER_CHANGE:
                speed = min(160, speed + 1)
                step_count = 0
        else:
            step_count -= 1
            if step_count <= -STEPS_PER_CHANGE:
                speed = max(0, speed - 1)
                step_count = 0
        last_knob_time = now
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

    # Knob press: cycle mode on release
    val = button_press.value()
    if prev_press == 0 and val == 1:
        mode_index = (mode_index + 1) % len(modes)
        state["theme"] = modes[mode_index]
        time.sleep(0.05)  # debounce
    prev_press = val

    # Send only changed values
    delta = {k: v for k, v in state.items() if last_sent.get(k) != v}
    if delta:
        print(json.dumps(delta))
        last_sent.update(delta)

    time.sleep(0.002)
