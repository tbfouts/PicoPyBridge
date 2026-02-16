import QtQuick

Item {
    id: gaugeStatic

    property alias gaugeCenter1GaugeCenter1_1Source: gaugeCenter1.gaugeCenter1_1Source
    property alias gaugeCenter2GaugeCenter2_1Source: gaugeCenter2.gaugeCenter2_1Source

    height: 950
    width: 1000

    clip: true

    OuterArcsComp {
        id: outerArcsComp

        x: 45
        y: 185
    }
    GaugeTicks {
        id: gaugeTicks

        x: 103
        y: 61
    }
    GaugeNumbersComp {
        id: gaugeNumbersComp

        x: 42
        y: 41

        clip: true
    }
    GaugeNumbers {
        id: gaugeNumbers

        x: 786
        y: 550

        clip: true
    }
    GuageEllipses {
        id: guageEllipses

        x: 91
        y: 38
    }
    GaugeCenter1 {
        id: gaugeCenter1

        x: 402
        y: 349

        gaugeCenter1_1Source: Qt.resolvedUrl("assets/gaugeCenter1_1.png")
    }
    GaugeCenter2 {
        id: gaugeCenter2

        x: 390
        y: 337

        gaugeCenter2_1Source: Qt.resolvedUrl("assets/gaugeCenter2_1.png")
    }
}