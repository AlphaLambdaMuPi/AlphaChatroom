import QtQuick 2.4
import QtQuick.Controls 1.3
import QtQuick.Layouts 1.1
import QtQuick.Controls.Styles 1.3
import QtGraphicalEffects 1.0

Item {
    anchors.fill: parent
    property alias channelMod: channelMod
    ListView {
        id: channelView
        //anchors.fill: parent
        width: parent.width
        height: childrenRect.height
        anchors {
            top: parent.top
        }
        model: ListModel {
            id: channelMod
        }

        delegate: Item {
            width: parent.width
            height: childrenRect.height
            Rectangle {
                id: indRec
                anchors {
                    fill: parent
                    margins: 8
                }
                radius: 5
                color: '#AAAAAA'
            }
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
                    text: channel
                    color: 'black'
                }
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        setActiveChannel(channel)
                    }
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
            states: [
                State {
                    name: 'active'
                    when: activeChannel == channel
                    PropertyChanges {
                        target: indRec
                        visible: true
                    }
                },
                State {
                    name: 'nonActive'
                    when: activeChannel != channel
                    PropertyChanges {
                        target: indRec
                        visible: false
                    }
                }
            ]
        }
    }

    Rectangle {
        id: textRect
        width: parent.width
        anchors {
            top: channelView.bottom
        }
        height: 60
        color: 'transparent'
        Image {
            source: '../img/add.png'
            sourceSize.height: 80
            anchors.centerIn: parent
        }
        MouseArea {
            anchors.fill: parent
            onClicked: {
                addChannelDialog.open()
            }
        }
    }
}
