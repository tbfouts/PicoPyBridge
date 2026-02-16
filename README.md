# Picopy — Figma-to-Qt + Pico Serial Bridge

Drive a Figma-designed QML UI from a Raspberry Pi Pico over USB serial. Design in Figma, export with the "Figma to Qt" plugin, make a few small edits, and physical controls (knobs, buttons) on the Pico update the UI in real time.

## Demo

This repo includes a working example: a speedometer gauge (`gaugeMPH_Project`) controlled by a rotary encoder and two theme-switching buttons on a Pico WH breadboard.

- **Rotary encoder** — controls speed (0-160 mph), gear shifts automatically
- **Button 1 (GP15)** — switches to eco theme (green), lights LED 1
- **Button 4 (GP13)** — switches to sport theme (red), lights LED 4

## Architecture

```
Figma Design (variables + themes)
       |  "Figma to Qt" plugin export
       v
QML Project Folder
  DesignTokens/
    ValuesStrings.qml    <-- declares variable properties
    Values.qml           <-- edited: bind to Bridge.xxx
    Tokens.qml           <-- edited: bind theme to Bridge.theme
       |
       v
app.py (PySide6)
  QQuickView loads QML
  Registers "PicoBridge" module from Python (no .qml file)
  QML singletons use `import PicoBridge 1.0` → `Bridge.xxx`
  SerialReader thread reads JSON from USB
       ^
       |  USB serial JSON lines
       |
Pico (MicroPython)
  main.py reads hardware inputs, sends {"mphValue": "72", "gear": "3"}
```

## The API contract

The `PROPERTIES` list at the top of `app.py` is the single source of truth:

```python
PROPERTIES = [
    "mphValue",
    "gear",
    "theme",
]
```

Each name must match across three places:
1. **app.py** — the `PROPERTIES` list
2. **main.py** — the JSON keys sent from the Pico
3. **QML** — the `Bridge.xxx` bindings in `Values.qml` / `Tokens.qml`

## JSON protocol

The Pico sends one JSON object per line. Only changed values are sent (delta protocol):

```json
{"mphValue": "72", "gear": "3"}
{"mphValue": "73"}
{"theme": "eco"}
```

All values are strings.

## Setup

### Prerequisites

- Python 3.9+
- macOS (or any OS with PySide6 + pyserial support)
- Raspberry Pi Pico (any variant) with MicroPython
- [mpremote](https://docs.micropython.org/en/latest/reference/mpremote.html) (`pip install mpremote`)

### Install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install PySide6 pyserial
```

### Install MicroPython on a fresh Pico

1. Hold **BOOTSEL** while plugging the Pico into USB
2. It mounts as a drive called **RPI-RP2**
3. Download the correct firmware:
   - Pico / Pico H: [RPI_PICO](https://micropython.org/download/RPI_PICO/)
   - Pico W / Pico WH: [RPI_PICO_W](https://micropython.org/download/RPI_PICO_W/)
   - Pico 2: [RPI_PICO2](https://micropython.org/download/RPI_PICO2/)
4. Copy the `.uf2` file to the RPI-RP2 drive — it reboots automatically
5. Unplug and replug (without BOOTSEL)

### Flash and run

```bash
mpremote cp main.py :main.py && mpremote reset
.venv/bin/python app.py gaugeMPH_Project
```

## Hardware wiring (demo)

Uses a Pico WH on a breadboard — no soldering required.

| Component        | Pico Pin | Notes                     |
|------------------|----------|---------------------------|
| Rotary encoder CLK | GP0    |                           |
| Rotary encoder DT  | GP1    |                           |
| Button 1 (eco)   | GP15     | Switches to eco theme     |
| LED 1            | GP14     | Lights when eco active    |
| Button 4 (sport) | GP13     | Switches to sport theme   |
| LED 4            | GP10     | Lights when sport active  |

Buttons use internal pull-up resistors (`Pin.PULL_UP`), active low (connect button between pin and GND).

## Adapting for a different Figma export

Follow these steps to use any Figma-to-Qt export with this bridge.

### 1. Export from Figma

Use the "Figma to Qt" plugin. Your Figma design should use **variables** for any values you want to control from hardware (text, colors, etc.). The export creates a `*_Project/` folder with QML files and a `DesignTokens/` module.

### 2. Identify your variables

Open `DesignTokens/ValuesStrings.qml` in the export. It lists the Figma variables:

```qml
QtObject {
    property string mphValue
    property string gear
}
```

These names are your API. If the Figma design has themes, check `DesignTokens/Tokens.qml` for theme names (e.g. `eco`, `sport`).

### 3. Edit app.py

Add your variable names to the `PROPERTIES` list:

```python
PROPERTIES = [
    "mphValue",
    "gear",
    "theme",       # only if switching themes
]
```

### 4. Edit Values.qml

In `DesignTokens/Values.qml`, add the PicoBridge import and replace hardcoded defaults with Bridge bindings. `PicoBridge` is not a file — it's a module registered by `app.py` at runtime via `qmlRegisterSingletonInstance`:

**Before** (from Figma export):
```qml
import QtQuick

...
    strings: ValuesStrings {
        gear: "D"
        mphValue: "95"
    }
```

**After**:
```qml
import QtQuick
import PicoBridge 1.0

...
    strings: ValuesStrings {
        gear: Bridge.gear
        mphValue: Bridge.mphValue
    }
```

### 5. Edit Tokens.qml (optional, for theme switching)

If your design has themes and you want to switch them from hardware:

**Before**:
```qml
import QtQuick

...
    property TokensTheme activeTheme: sport
```

**After**:
```qml
import QtQuick
import PicoBridge 1.0

...
    property TokensTheme activeTheme: Bridge.theme === "eco" ? eco : sport
```

### 6. Write main.py for the Pico

Send JSON with keys matching your `PROPERTIES` list. Example for a simple simulation:

```python
from machine import Pin
import json
import time

last_sent = {}

while True:
    state = {
        "mphValue": "72",
        "gear": "D",
    }

    delta = {k: v for k, v in state.items() if last_sent.get(k) != v}
    if delta:
        print(json.dumps(delta))
        last_sent.update(delta)

    time.sleep(0.1)
```

Replace the hardcoded values with real hardware reads (ADC, encoder, buttons, sensors).

### 7. Flash and run

```bash
mpremote cp main.py :main.py && mpremote reset
.venv/bin/python app.py yourExport_Project
```

## Adding a new variable

1. **app.py** — add the name to `PROPERTIES`
2. **main.py** — add the matching JSON key
3. **Values.qml** — add the `Bridge.xxx` binding
4. **ValuesStrings.qml** — add `property string xxx` if not already there from the Figma export

## Project structure

```
picopy/
├── main.py              # Pico — reads hardware, sends JSON over serial
├── app.py               # Mac — QML runner with serial bridge
├── gaugeMPH_Project/    # Figma-to-Qt export (with Bridge edits)
│   ├── *.qmlproject     # Project manifest (mainFile, imports)
│   ├── DesignTokens/    # Values.qml, Tokens.qml, ValuesStrings.qml
│   ├── *.qml            # UI components
│   └── assets/          # Exported images
└── README.md
```
