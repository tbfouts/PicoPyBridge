import sys
import os
import glob
import json

import serial
from PySide6.QtCore import QThread, Signal, Property, QObject, QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQuick import QQuickView
from PySide6.QtQml import qmlRegisterSingletonInstance

# ── API ──────────────────────────────────────────────────────────
# Figma variable names = Pico JSON keys = QML Bridge properties.
# To add a new variable:
#   1. Add the name here
#   2. Add the key in main.py on the Pico
#   3. Add the binding in Values.qml  (e.g.  gear: Bridge.gear)
PROPERTIES = [
    "mphValue",
    "gear",
    "theme",
]
# ─────────────────────────────────────────────────────────────────


class SerialReader(QThread):
    data_received = Signal(dict)

    def __init__(self, port, baudrate=115200):
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self._running = True

    def run(self):
        self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
        while self._running:
            try:
                line = self.ser.readline().decode("utf-8").strip()
                if line:
                    data = json.loads(line)
                    self.data_received.emit(data)
            except (json.JSONDecodeError, UnicodeDecodeError):
                continue
            except serial.SerialException:
                break
        self.ser.close()

    def stop(self):
        self._running = False
        self.wait()


def _build_bridge_class(props):
    """Create a QObject with a string Property for each name in props."""
    attrs = {}
    for name in props:
        sig = Signal()
        attrs[f"{name}Changed"] = sig
        priv = f"_{name}"

        def mkget(p):
            return lambda self: getattr(self, p, "")

        def mkset(p, s):
            def setter(self, v):
                if getattr(self, p, "") != v:
                    setattr(self, p, v)
                    getattr(self, s).emit()
            return setter

        attrs[name] = Property(str, mkget(priv), mkset(priv, f"{name}Changed"), notify=sig)
    return type("DataBridge", (QObject,), attrs)


DataBridge = _build_bridge_class(PROPERTIES)


def main():
    project_dir = None
    serial_port = None

    for arg in sys.argv[1:]:
        if os.path.isdir(arg):
            project_dir = arg
        elif arg.startswith("/dev/") or arg.startswith("COM"):
            serial_port = arg

    if not project_dir:
        dirs = glob.glob("*_Project")
        project_dir = dirs[0] if dirs else None
    if not project_dir:
        print("No project folder found. Pass a *_Project directory as argument.")
        sys.exit(1)

    if not serial_port:
        ports = glob.glob("/dev/tty.usbmodem*")
        serial_port = ports[0] if ports else None
    if not serial_port:
        print("No serial port found. Pass a port as argument or connect a Pico.")
        sys.exit(1)

    project_dir = os.path.abspath(project_dir)
    print(f"Project: {project_dir}")
    print(f"Serial:  {serial_port}")

    # Find main QML file from .qmlproject
    qmlproject = glob.glob(os.path.join(project_dir, "*.qmlproject"))
    if not qmlproject:
        print("No .qmlproject file found")
        sys.exit(1)
    import re
    match = re.search(r'mainFile:\s*"([^"]+)"', open(qmlproject[0]).read())
    if not match:
        print("No mainFile in .qmlproject")
        sys.exit(1)
    main_file = match.group(1)

    app = QGuiApplication(sys.argv)

    # Expose bridge to QML as a singleton: import PicoBridge 1.0 → Bridge.gear
    bridge = DataBridge()
    qmlRegisterSingletonInstance(DataBridge, "PicoBridge", 1, 0, "Bridge", bridge)

    view = QQuickView()
    view.setResizeMode(QQuickView.SizeViewToRootObject)
    view.setTitle("Picopy")
    view.engine().addImportPath(project_dir)
    view.setSource(QUrl.fromLocalFile(os.path.join(project_dir, main_file)))

    if view.status() == QQuickView.Error:
        for err in view.errors():
            print(f"QML: {err.toString()}")
        sys.exit(1)

    view.show()

    # Wire serial data to bridge properties
    reader = SerialReader(serial_port)

    def on_data(delta):
        for key, value in delta.items():
            if hasattr(bridge, key):
                setattr(bridge, key, str(value))

    reader.data_received.connect(on_data)
    reader.start()

    ret = app.exec()
    reader.stop()
    sys.exit(ret)


if __name__ == "__main__":
    main()
