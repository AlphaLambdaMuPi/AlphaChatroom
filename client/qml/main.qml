import QtQuick 2.4
import QtQuick.Controls 1.3
import QtQuick.Layouts 1.1
import QtQuick.Controls.Styles 1.3
import QtGraphicalEffects 1.0

Rectangle {
    height: 600
    width: 800
    property alias cl: cl
    property alias channelMod: cl.channelMod
    property alias chatView: chatView
    property alias userView: userView
    property alias chatScroll: chatScroll

    RowLayout {
        spacing: 0
        anchors.fill: parent

        Rectangle {
            Layout.preferredWidth: 250
            Layout.fillHeight: true
            color: '#DDDDDD'
            ChannelList {
                id: cl
            }
        }



        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            ColumnLayout {
                anchors.fill: parent
                spacing: 0
                RowLayout {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    Layout.minimumHeight: 200
                    spacing: 0

                    Rectangle {
                        color: '#BBBBBB'
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        Layout.minimumWidth: 300

                        ScrollView {
                            id: chatScroll
                            anchors.fill: parent
                            flickableItem.anchors.margins: 20
                            property alias animation: __ani
                            NumberAnimation on flickableItem.contentY {
                                id: __ani
                                duration: 400
                                easing.type: Easing.OutBounce
                            }
                            Item {
                                width: parent.parent.width
                                height: childrenRect.height
                                ListView {
                                    id: chatView
                                    width: parent.width
                                    height: childrenRect.height
                                    anchors {
                                        top: parent.top
                                    }
                                    spacing: 20
                                    model: ListModel {
                                        id: chatMod
                                    }
                                    delegate: chatDelegate
                                } 
                                Item {
                                    id: bugFixRect
                                    width: parent.width
                                    height: 40
                                    anchors {
                                        top: chatView.bottom
                                    }
                                }
                            }
                        }

                        Rectangle {
                            id: _rec
                            anchors {
                                horizontalCenter: parent.horizontalCenter
                                bottom: parent.bottom
                                bottomMargin: 20
                            }
                            radius: 20
                            height: 40
                            width: 300
                            opacity: 0
                            Behavior on opacity {
                                NumberAnimation { duration: 500 }
                            }
                            states: [
                                State {
                                    when: (chatScroll.flickableItem.contentHeight - chatScroll.flickableItem.contentY -
                                                chatScroll.height) > 100
                                    PropertyChanges {
                                        target: _rec
                                        opacity: 0.8
                                    }
                                    PropertyChanges {
                                        target: _ma
                                        visible: true
                                    }
                                },
                                State {
                                    when: (chatScroll.flickableItem.contentHeight - chatScroll.flickableItem.contentY -
                                                chatScroll.height) <= 100
                                    PropertyChanges {
                                        target: _rec
                                        opacity: 0
                                    }
                                }
                            ]

                            Text {
                                anchors.centerIn: parent
                                text: "Click to scroll to the bottom"
                                color: 'white'
                            }
                            MouseArea {
                                id: _ma
                                anchors.fill: parent
                                cursorShape: Qt.PointingHandCursor
                                onClicked: {
                                    scrollToBottom()
                                }
                                visible: false
                            }
                            color: '#444'
                        }
                    }

                    Rectangle {
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        Layout.preferredWidth: 120
                        Layout.maximumWidth: 180

                        ScrollView {
                            anchors.fill: parent
                            horizontalScrollBarPolicy: Qt.ScrollBarAlwaysOff
                            ListView {
                                id: userView
                                anchors {
                                    fill: parent
                                    topMargin: 10
                                }
                                spacing: 0
                                model: ListModel {
                                    id: userMod
                                }
                                delegate: UserDelegate{}
                            }
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
            spacing: 0
            Image {
                id: picRec
                //width: childrenRect.width
                //height: childrenRect.height
                //Image {
                //width: 60
                //height: 60
                //}
                source: 'Image://avatarImage/' + sender
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
                    property int tmargin: 15
                    property int lineHeight: 1
                    id: rec
                    color: 'white'
                    height: mesgText.paintedHeight + tmargin + lineHeight + senderText.paintedHeight + 10
                    width: Math.max(mesgText.paintedWidth, senderText.paintedWidth) + tmargin * 2
                    Text {
                        anchors {
                            //horizontalCenter: parent.horizontalCenter
                            //verticalCenter: parent.verticalCenter
                            top: parent.top
                            topMargin: rec.tmargin
                            bottomMargin: rec.tmargin
                            left: rec.left
                            leftMargin: rec.tmargin
                        }
                        id: mesgText
                        text: mesg
                        wrapMode: Text.Wrap
                        width: Math.min(parent.parent.parent.parent.width - rec.tmargin * 2 - picRec.width, implicitWidth)
                        textFormat: Text.RichText
                        Component.onCompleted: {
                            //console.log(implicitWidth, parent.parent.parent.parent.parent.width - rec.tmargin*2 - picRec.width, width)
                        }
                        onLinkActivated: Qt.openUrlExternally(link)
                    }

                    Rectangle {
                        id: line
                        anchors {
                            top: mesgText.bottom
                            left: parent.left
                            right: parent.right
                            topMargin: 10
                            leftMargin: 5
                            rightMargin: 5
                            bottomMargin: 0
                        }
                        height: rec.lineHeight
                        color: 'grey'
                    }

                    Text {
                        id: senderText
                        anchors {
                            top: line.bottom
                            left: parent.left
                            right: parent.right
                            topMargin: 0
                            leftMargin: 20
                            rightMargin: 7
                            bottomMargin: 0
                        }
                        text: sender + ' @' + timeStr
                        color: '#444'
                    }
                }
            }
        }
    }

}
