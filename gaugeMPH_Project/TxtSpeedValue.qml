import QtQuick
import DesignTokens as Tokens

Item {
    id: txtSpeedValue

    height: 144
    width: 294

    Text {
        id: txtSpeedValue_1

        height: 144
        width: 295

        color: Tokens.Tokens.colors.textMPHValue
        font.family: "Galvji"
        font.italic: true
        font.pixelSize: 150
        font.weight: Font.Normal
        horizontalAlignment: Text.AlignRight
        text: Tokens.Values.strings.mphValue
        textFormat: Text.PlainText
        verticalAlignment: Text.AlignVCenter
    }
}