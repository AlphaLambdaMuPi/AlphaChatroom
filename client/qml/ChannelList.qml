import QtQuick 2.4
import QtQuick.Controls 1.3
import QtQuick.Layouts 1.1
import QtQuick.Controls.Styles 1.3
import QtGraphicalEffects 1.0
import QtQuick.Dialogs 1.2

Item {
    id: _clRoot
    anchors.fill: parent
    property alias channelMod: channelMod
    signal newMessage(string ch)
    signal changeActiveChannel(string ch)
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

        add: Transition {
            id: _t
            NumberAnimation {
                properties: 'y'
                from: _t.ViewTransition.destination.y + 100
                easing.type: Easing.OutBounce
                duration: 500
            }
        }

        delegate: Item {
            width: parent.width
            height: childrenRect.height
            property int newMessageNum: 0
            Connections {
                target: _clRoot
                onNewMessage: {
                    if(ch == channel) {
                        newMessageNum += 1
                        _bani1.to = _redCirc.y - 30
                        _bani2.to = _redCirc.y
                        _bani.start()
                    }
                }
            }
            Connections {
                target: _clRoot
                onChangeActiveChannel: {
                    if(ch == channel) {
                        newMessageNum = 0
                    }
                }
            }
            Rectangle {
                id: indRec
                anchors {
                    fill: parent
                    margins: 8
                }
                radius: 5
                color: '#AAAAAA'
            }
            Item {
                id: textRect
                width: parent.width
                height: childrenRect.height + 20
                MouseArea {
                    id: _ma
                    anchors.fill: parent
                    onClicked: {
                        setActiveChannel(channel)
                    }
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                }
                Image {
                    id: _img
                    anchors.left: parent.left
                    anchors.leftMargin: 10
                    anchors.verticalCenter: parent.verticalCenter
                    source: '../img/delete.png'
                    width: 32
                    height: 32
                    visible: false

                    MouseArea {
                        z: 100
                        id: _imgma
                        anchors.fill: parent
                        onClicked: {
                            leaveChannel(channel, index)
                        }
                        cursorShape: Qt.PointingHandCursor
                    }

                    states: [
                        State {
                            when: _ma.containsMouse
                            PropertyChanges {
                                target: _img
                                visible: true
                            }
                        }
                    ]
                }
                Text {
                    anchors.centerIn: parent
                    font {
                        pointSize: 16
                    }
                    text: channel
                    color: 'black'
                }

                Item {
                    anchors {
                        right: parent.right
                        verticalCenter: parent.verticalCenter
                        rightMargin: 10
                    }
                    width: 30
                    height: 30
                    Rectangle {
                        id: _redCirc
                        color: 'red'
                        width: 30
                        height: 30
                        radius: 15
                        visible: false
                        //y: parent.verticalCenter
                        Text {
                            anchors.centerIn: parent
                            text: '' + newMessageNum
                            color: 'white'
                            font.bold: true
                        }
                        SequentialAnimation {
                            id: _bani
                            NumberAnimation { 
                                id: _bani1
                                target: _redCirc; 
                                property: 'y'; 
                                duration: 200;
                                easing.type: Easing.OutQuad
                            }
                            NumberAnimation { 
                                id: _bani2
                                target: _redCirc; 
                                property: 'y'; 
                                duration: 350;
                                easing.amplitude: 2
                                easing.type: Easing.OutBounce
                            }
                        }
                        states: [
                            State {
                                name: 'on'
                                when: newMessageNum != 0
                                PropertyChanges {
                                    target: _redCirc
                                    visible: true
                                }
                            }
                        ]
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
                    when: activeChannel == channel || _ma.containsMouse
                    PropertyChanges {
                        target: indRec
                        visible: true
                    }
                },
                State {
                    name: 'nonActive'
                    when: activeChannel != channel && !_ma.containsMouse
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
}
