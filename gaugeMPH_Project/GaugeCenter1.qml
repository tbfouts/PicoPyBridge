import QtQuick

Item {
    id: gaugeCenter1

    property alias gaugeCenter1_1Source: gaugeCenter1_1.source

    height: 249
    width: 249

    Image {
        id: gaugeCenter1_1

        source: Qt.resolvedUrl("assets/gaugeCenter1_2.png")
    }
}