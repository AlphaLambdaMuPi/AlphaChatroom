import QtQuick 2.4
import QtQuick.Controls 1.3
import QtQuick.Layouts 1.1
import QtQuick.Controls.Styles 1.3
import QtQuick.Dialogs 1.2

RowLayout {
    spacing: 20
    anchors {
        fill: parent
        margins: 20
    }
    TextArea {
        id: ta
        Layout.fillHeight: true
        Layout.preferredWidth: parent.width * 0.75
        anchors.margins: 20
    }
    Button {
        Layout.fillHeight: true
        Layout.fillWidth: true
        anchors.margins: 20
        text: 'Send'
        onClicked: {
            medium.Qsend(activeChannel, ta.text)
        }
    }
}
