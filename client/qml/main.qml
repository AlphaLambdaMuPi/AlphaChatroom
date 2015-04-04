import QtQuick 2.4
import QtQuick.Controls 1.3
import QtQuick.Layouts 1.1
import QtQuick.Controls.Styles 1.3
import QtGraphicalEffects 1.0
import QtQuick.Dialogs 1.2

Rectangle {
    height: 600
    width: 800
    property alias channelMod: cl.channelMod
    property alias chatView: chatView

    RowLayout {
        spacing: 0
        anchors.fill: parent

        Rectangle {
            width: 200
            Layout.fillHeight: true
            color: '#DDDDDD'
            ChannelList {
                id: cl
            }
        }


        Dialog {
            standardButtons: StandardButton.Ok | StandardButton.Cancel
            id: addChannelDialog
            TextField {
                id: addChannelText
                text: '0.0'
                anchors.centerIn: parent
                width: parent.width - 20
            }
            onAccepted: {
                medium.Qjoin(addChannelText.text)
            }
        }

        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            ColumnLayout {
                anchors.fill: parent
                spacing: 0
                Rectangle {
                    color: '#BBBBBB'
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    Layout.minimumHeight: 200

                    ScrollView {
                        anchors.fill: parent
                        ListView {
                            id: chatView
                            anchors {
                                margins: 20
                                fill: parent
                            }
                            spacing: 20
                            model: ListModel {
                                id: chatMod
                            }
                            delegate: chatDelegate
                        }
                    }
                }

                Rectangle {
                    color: '#EEEEEE'
                    Layout.preferredHeight: 200
                    Layout.fillWidth: true

                    UserInput {}
                }
            }
        }
    }

    Component {
        id: chatDelegate
        Row {
            width: parent.width
            height: childrenRect.height
            Rectangle {
                id: picRec
                //width: childrenRect.width
                //height: childrenRect.height
                //Image {
                //source: '../img/alpha.png'
                //width: 60
                //height: 60
                //}
                color: 'blue'
                width: 60
                height: 60
            }

            Item {
                height: childrenRect.height
                width: childrenRect.width
                RectangularGlow {
                    anchors.fill: rec
                    anchors.topMargin: 4
                    anchors.leftMargin: 4
                    glowRadius: 5
                    spread: 0.2
                    color: "#80000000"
                }
                Rectangle {
                    property int tmargin: 10
                    id: rec
                    color: 'white'
                    height: mesgText.paintedHeight + tmargin * 2
                    width: mesgText.paintedWidth + tmargin * 2
                    Text {
                        anchors {
                            centerIn: parent
                        }
                        id: mesgText
                        text: sender + ": " + mesg
                        wrapMode: Text.Wrap
                        width: Math.min(parent.parent.parent.width - rec.tmargin * 2 - picRec.width, paintedWidth)
                        Component.onCompleted: {
                            console.log(implicitWidth)
                        }
                    }
                }
            }
        }
    }

}
