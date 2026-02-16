import QtQuick

Item {
    id: gaugeCenter2

    property alias gaugeCenter2_1Source: gaugeCenter2_1.source

    height: 272
    width: 272

    Image {
        id: gaugeCenter2_1

        source: Qt.resolvedUrl("assets/gaugeCenter2_2.png")
    }
}