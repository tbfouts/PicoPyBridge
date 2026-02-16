import QtQuick
import DesignTokens as Tokens

Item {
    id: txtGearValue

    height: 137
    width: 99

    Text {
        id: txtGearValue_1

        height: 137
        width: 100

        color: Tokens.Tokens.colors.prndlColor
        font.family: "Galvji"
        font.pixelSize: 150
        font.weight: Font.Normal
        horizontalAlignment: Text.AlignHCenter
        text: Tokens.Values.strings.gear
        textFormat: Text.PlainText
        verticalAlignment: Text.AlignVCenter
    }
}