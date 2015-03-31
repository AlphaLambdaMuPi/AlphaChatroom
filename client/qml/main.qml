import QtQuick 2.4
import QtQuick.Controls 1.3
import QtQuick.Layouts 1.1
import QtQuick.Controls.Styles 1.3
import QtGraphicalEffects 1.0

Rectangle {
    height: 600
    width: 800
    property alias channelMod: channelMod
    property alias chatMod: chatMod

    RowLayout {
        spacing: 0
        anchors.fill: parent

        Rectangle {
            width: 200
            Layout.fillHeight: true
            color: '#DDDDDD'

            ListView {
                id: channelView
                anchors.fill: parent
                model: ListModel {
                    id: channelMod
                }

                delegate: Item {
                    width: parent.width
                    height: childrenRect.height
                    Rectangle {
                        id: textRect
                        width: parent.width
                        height: childrenRect.height + 20
                        color: 'transparent'
                        Text {
                            anchors.centerIn: parent
                            font {
                                pointSize: 20
                            }
                            text: name
                            color: 'black'
                        }
                    }
                    Rectangle {
                        id: splitLine
                        width: parent.width
                        anchors{
                            top: textRect.bottom
                            right: parent.right
                            rightMargin: 6
                            left: parent.left
                            leftMargin: 6
                        }
                        height: 2
                        radius: 2
                        color: '#777777'
                    }
                }
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
                                    height: childrenRect.height + tmargin * 2
                                    width: childrenRect.width + tmargin * 2
                                    Text {
                                        anchors {
                                            centerIn: parent
                                        }
                                        id: mesgText
                                        text: sender + ": " + mesg
                                        wrapMode: Text.Wrap
                                        width: Math.min(parent.parent.parent.width - rec.tmargin * 2 - picRec.width, implicitWidth)
                                    }
                                }
                            }
                        }
                    }
                }

                Rectangle {
                    color: '#EEEEEE'
                    Layout.preferredHeight: 200
                    Layout.fillWidth: true

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
                                logic.send(ta.text)
                            }
                        }
                    }
                }
            }
        }
    }
}
