pragma Singleton

import QtQuick
import PicoBridge 1.0

QtObject {
    id: tokens

    property TokensTheme activeTheme: Bridge.theme === "eco" ? eco : sport
    property TokensColors colors: activeTheme.colors

    property TokensTheme eco: TokensTheme {
        colors: TokensColors {
            backgroundColor: "#ff000000"
            grey: "#ff737373"
            needleColor: "#ff008500"
            prndlColor: "#ffd4d4d4"
            redlineColor: "#ff00aa00"
            rightArcColor: "#ff598b57"
            textMPHValue: "#ffcdcdcd"
            txtMPH: "#ff757575"
        }
    }
    property TokensTheme sport: TokensTheme {
        colors: TokensColors {
            backgroundColor: "#ff000000"
            grey: "#ff737373"
            needleColor: "#ffff0000"
            prndlColor: "#ffdeca81"
            redlineColor: "#ffa85353"
            rightArcColor: "#ffec3d3d"
            textMPHValue: "#ffffffff"
            txtMPH: "#ffb2b5b6"
        }
    }
}