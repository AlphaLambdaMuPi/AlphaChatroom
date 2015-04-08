import QtQuick 2.4
import QtQuick.Controls 1.3
import QtQuick.Layouts 1.1
import QtQuick.Controls.Styles 1.3
import QtQuick.Dialogs 1.2

Column {
    anchors.fill: parent
    Row {
        id: _row
        anchors {
            left: parent.left
            right: parent.right
            top: parent.top
            leftMargin: 20
            rightMargin: 20
        }
        spacing: 2
        Rectangle {
            id: _recE
            border {
                width: 2
                color: 'grey'
            }
            width: 100
            height: 36
            color: '#EEE'
            radius: 3
            Image {
                anchors.centerIn: parent
                source: '../img/smile.png'
                height: 32
                width: 32
            }
            MouseArea {
                id: _ma
                cursorShape: Qt.PointingHandCursor
                hoverEnabled: true 
                anchors.fill: parent
                onClicked: {
                    _recES.visible = !_recES.visible
                }
            }

            states: [
                State {
                    name: 'mouse-over'
                    when: _ma.containsMouse
                    PropertyChanges { target: _recE; color: '#99CCFF'; }
                }
            ]


            Rectangle {
                id: _recES
                width: childrenRect.width
                height: childrenRect.height
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.bottom: parent.top
                visible: false
                ScrollView {
                    width: 315
                    height: 100
                    Grid {
                        columns: 10
                        Repeater {
                            model: 29*29
                            Image {
                                source: 'Image://emoticon/' + Math.floor(index/29) + '-' + (index%29)
                                MouseArea {
                                    anchors.fill: parent
                                    cursorShape: Qt.PointingHandCursor
                                    onClicked: {
                                        ta.insert(ta.cursorPosition,
                                            '\\((emoticon:' + Math.floor(index/29) + '-' + (index%29) + '))'
                                        )
                                    }
                                }
                            }
                        }
                    }
                }
                color: 'white'
                border {
                    color: '#555'
                    width: 2
                }
                radius: 5

            }
        }
        Rectangle {
            id: _recF
            border {
                width: 2
                color: 'grey'
            }
            width: 100
            height: 36
            color: '#EEE'
            radius: 3
            Image {
                anchors.centerIn: parent
                source: '../img/file.png'
                height: 24
                width: 24
            }
            MouseArea {
                id: _maF
                cursorShape: Qt.PointingHandCursor
                hoverEnabled: true 
                anchors.fill: parent
                onClicked: {
                    fileDialog.visible = true
                }
            }

            states: [
                State {
                    name: 'mouse-over'
                    when: _maF.containsMouse
                    PropertyChanges { target: _recF; color: '#99CCFF'; }
                }
            ]
            FileDialog {
                id: fileDialog
                title: 'Choose file to send'
                //modality: Qt.NonModal
                onAccepted: {
                    medium.QsendFile(fileDialog.fileUrl, activeChannel)
                }
            }
        }
    }
    RowLayout {
        spacing: 20
        anchors {
            left: parent.left
            right: parent.right
            bottom: parent.bottom
            top: _row.bottom
            margins: 20
        }
        TextArea {
            id: ta
            Layout.fillHeight: true
            Layout.preferredWidth: parent.width * 0.75
            anchors.margins: 20
            Keys.onReturnPressed: {
                if(!(event.modifiers & Qt.ShiftModifier)) {
                    ta.send()
                    event.accepted = true
                } else {
                    ta.append('')
                }
            }
            function send() {
                medium.Qsend(activeChannel, ta.text)
                ta.text = ''
            }
        }
        Button {
            Layout.fillHeight: true
            Layout.fillWidth: true
            anchors.margins: 20
            text: 'Send'
            onClicked: {
                ta.send()
            }
        }
    }
}
