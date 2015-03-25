import QtQuick 2.4
import QtQuick.Controls 1.3
import QtQuick.Layouts 1.1

ApplicationWindow {
    width: 800
    height: 600

    RowLayout {
        anchors.fill: parent
        spacing: 0
        Rectangle {
            Layout.fillHeight: true
            implicitWidth: parent.width * 0.3
            color: 'black'
            Rectangle {
                color: '#000055'
                width: parent.width
                height: 100
                Text {
                    text: "Log in"
                    color: 'white'
                    font.pointSize: 20
                    anchors.centerIn: parent
                }
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        logic.hello()
                        console.log('123')
                    }
                }
            }
        }
        Rectangle {
            Layout.fillHeight: true
            Layout.fillWidth: true
            color: 'white'

            ListView {
                anchors.fill: parent
                model: ListModel {
                    ListElement {
                        sender: "Server"
                        dataText: "I 7122ed..."
                    }
                    ListElement {
                        sender: "Server"
                        dataText: "zzzzzzzz"
                    }
                }
                delegate: Rectangle {
                    width: parent.width
                    height: 30
                    color: 'red'
                    Text {
                        text: '<b>' + sender + ': </b>' + dataText
                    }
                }
            }

            Row {
                height: 200
                width: parent.width
                anchors.bottom: parent.bottom
                TextArea {
                    id: textArea
                    anchors {
                        top: parent.top
                        bottom: parent.bottom
                        left: parent.left
                        margins: 20
                    }
                    width: parent.width * 0.7
                    text: 'epsilon'
                    //height: parent.height
                }
                Button {
                    anchors {
                        top: parent.top
                        bottom: parent.bottom
                        left: sentText.right
                        right: parent.right
                        margins: 20
                    }
                    //implicitWidth: parent.width*0.3
                    text: 'Send'
                    onClicked: {
                        logic.send( textArea.text )
                        textArea.text = ''
                    }
                }
            }
        }
    }
}
