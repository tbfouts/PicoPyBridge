import QtQuick

Item {
    id: needleRotation

    property alias needleVecRotation: needleVec.rotation
    property alias needleVecSource: needleVec.source

    height: 30
    width: 870

    clip: true
    rotation: 0

    Image {
        id: needleVec

        y: 5.04

        rotation: 0
        source: Qt.resolvedUrl("assets/needleVec_1.png")
    }
}