import QtQuick 2.4
import QtQuick.Controls 1.3
import QtQuick.Layouts 1.1
import QtQuick.Controls.Styles 1.3

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
            color: '#222222'

            ListView {
                id: channelView
                anchors.fill: parent
                model: ListModel {
                    id: channelMod
                }

                delegate: Rectangle {
                    width: parent.width
                    height: 100
                    color: 'transparent'
                    Text {
                        anchors.centerIn: parent
                        font {
                            pointSize: 20
                        }
                        text: name
                        color: 'white'
                    }
                }

                highlight: Rectangle {
                    color: '#557799'
                    radius: 10
                }
                focus: true
                
            }


        }
        Rectangle {
            width: 200
            Layout.fillHeight: true
            Layout.fillWidth: true
            color: '#444444'

            ListView {
                id: chatView
                anchors.fill: parent
                model: ListModel {
                    id: chatMod
                }

                delegate: textComponent
                focus: true
                
            }

            Item {
                width: parent.width
                height: 200
                anchors.bottom: parent.bottom
                TextArea {
                    id: tar
                    anchors {
                        left: parent.left
                        top: parent.top
                        bottom: parent.bottom
                        margins: 15
                    }
                    width: parent.width * 0.7
                }
                Button {
                    anchors {
                        left: tar.right
                        right: parent.right
                        top: parent.top
                        bottom: parent.bottom
                        margins: 15
                    }
                    text: 'send'
                    onClicked: {
                        logic.send(tar.text)
                    }
                }
            }

            Component {
                id: chatDelegate

                Loader {
                    sourceComponent: type == 'text' ? textComponent : alphaComponent
                    width: parent.width
                    height: childrenRect.height
                }
            }

            Component {
                id: textComponent
                Rectangle {
                    width: parent.width
                    height: childrenRect.height + 10
                    color: 'transparent'

                    ColumnLayout {
                        width: parent.width
                        Item {
                            Layout.fillWidth: true
                            height: childrenRect.height
                            anchors.topMargin: 100
                            //anchors.verticalCenter: parent.verticalCenter
                            RowLayout {
                                Layout.fillWidth: true
                                //height: childrenRect.height
                                anchors {
                                    left: parent.left
                                    leftMargin: 10
                                    right: parent.right
                                    rightMargin: 10
                                }

                                Rectangle {
                                    id: imgRect
                                    width: 90
                                    height: 90
                                    anchors.verticalCenter: parent.verticalCenter
                                    color: 'white'
                                    Image {
                                        width: 80
                                        height: 80
                                        anchors.centerIn: parent

                                        source: '../img/alpha.png'
                                    }
                                    //border {
                                        //width: 10
                                        //color: '#5588CC'
                                    //}
                                    radius: 10
                                }

                                Rectangle {
                                    Layout.minimumHeight: 100
                                    radius: 10
                                    anchors {
                                        right: parent.right
                                        left: imgRect.right
                                        leftMargin: 10
                                        rightMargin: 10
                                    }
                                    Text {
                                        anchors {
                                            margins: 10
                                            fill: parent
                                        }
                                        text: '<b>' + sender + ': </b> ' + mesg
                                    }
                                }
                            }
                        }
                    }
                    Component.onCompleted: {
                        console.log(1231231);
                    }
                }
            }
        }
    }
}
