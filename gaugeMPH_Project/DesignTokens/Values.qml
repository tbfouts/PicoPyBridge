pragma Singleton

import QtQuick
import PicoBridge 1.0

QtObject {
    id: values

    property ValuesTheme activeTheme: mode_1
    property ValuesStrings strings: activeTheme.strings

    property ValuesTheme mode_1: ValuesTheme {
        strings: ValuesStrings {
            gear: Bridge.gear
            mphValue: Bridge.mphValue
        }
    }
}