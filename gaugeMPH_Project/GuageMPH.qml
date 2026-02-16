import QtQuick

Rectangle {
    id: guageMPH

    height: 950
    width: 1000

    clip: true
    color: "#000000"

    GaugeStatic {
        id: gaugeStatic

        clip: true
        gaugeCenter1GaugeCenter1_1Source: Qt.resolvedUrl("assets/gaugeCenter1.png")
        gaugeCenter2GaugeCenter2_1Source: Qt.resolvedUrl("assets/gaugeCenter2.png")
    }
    TxtSpeedValue {
        id: txtSpeedValue

        x: 662
        y: 389
    }
    TxtGearValue {
        id: txtGearValue

        x: 477
        y: 407
    }
    NeedleArc {
        id: needleArc

        x: 87
        y: 35

        needleArc_1Source: Qt.resolvedUrl("assets/needleArc.png")
        visible: false
    }
    NeedleRotation {
        id: needleRotation

        x: 91
        y: 457

        clip: true
        needleVecRotation: 0
        needleVecSource: Qt.resolvedUrl("assets/needleVec.png")
        rotation: 0
    }
}