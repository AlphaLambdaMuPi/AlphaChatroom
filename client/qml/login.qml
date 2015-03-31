import QtQuick 2.4
import QtQuick.Controls 1.3
import QtQuick.Layouts 1.1
import QtQuick.Controls.Styles 1.3

Rectangle {
    height: 600
    width: 300

    ColumnLayout {
        anchors.fill: parent
        spacing: 0

        Rectangle {
            color: '#222222'
            Layout.fillWidth: true
            height: parent.height * 0.1

            Text {
                anchors.centerIn: parent
                text: 'Welcome to Alllpha chatroom'
                color: 'white'
                font {
                    pointSize: 12
                }
            }
        }
        Rectangle {
            color: '#228833'
            Layout.fillWidth: true
            height: 6
        }
        Rectangle {
            color: '#222222'
            Layout.fillWidth: true
            height: parent.height * 0.5

            Rectangle {
                color: '#333333'
                border {
                    color: '#223388'
                    width: 20
                }
                radius: 20
                anchors.centerIn: parent
                width: {
                    var a = Math.min(parent.width, parent.height)
                    return a * 0.7;
                }
                height: {
                    var a = Math.min(parent.width, parent.height)
                    return a * 0.7;
                }                
                Image {
                    anchors.margins: 20
                    anchors.fill: parent
                    source: '../img/alpha.png'
                }
            }
            
        }

        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: '#444444'

            ColumnLayout {
                anchors.centerIn: parent
                Text {
                    anchors.horizontalCenter: parent.horizontalCenter
                    text: 'Nick Name: '
                    color: 'yellow'
                }
                TextField {
                    id: nickTf
                    anchors.horizontalCenter: parent.horizontalCenter
                    text: 'alpha'
                    style: TextFieldStyle {
                        background: Rectangle {
                            radius: 2
                            color: '#666666'
                        }
                    }
                }
                Button {
                    anchors.top: nickTf.bottom
                    anchors.topMargin: 20
                    anchors.horizontalCenter: parent.horizontalCenter
                    text: 'Login!!'
                    style: ButtonStyle {
                        background: Rectangle {
                            radius: 2
                            color: control.hovered ? '#4AaaA5' : '#3A9a95'
                        }
                    }
                    onClicked: {
                        logic.login(nickTf.text)
                    }
                }
            }
        }
    }
}