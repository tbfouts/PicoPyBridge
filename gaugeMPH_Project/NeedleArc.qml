import QtQuick

Item {
    id: needleArc

    property alias needleArc_1Source: needleArc_1.source

    height: 868
    width: 868

    visible: true

    Image {
        id: needleArc_1

        source: Qt.resolvedUrl("assets/needleArc_1.png")
    }
}