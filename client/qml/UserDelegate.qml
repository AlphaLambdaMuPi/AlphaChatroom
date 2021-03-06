import QtQuick 2.4
import QtQuick.Controls 1.3
import QtQuick.Layouts 1.1
import QtQuick.Controls.Styles 1.3
import QtGraphicalEffects 1.0
import QtQuick.Dialogs 1.2

Rectangle {
    width: parent.width
    height: 50
    color: 'white'
    id: _rec
    Image {
        id: __avatar
        anchors {
            verticalCenter: parent.verticalCenter
            left: parent.left
            leftMargin: 10
        }
        source: 'Image://avatarImage/' + name 
        width: 40
        height: 40
    }
    Item {
        anchors {
            top: parent.top
            bottom: parent.bottom
            right: parent.right
            left: __avatar.right
            leftMargin: 8
        }
        Text {
            anchors.verticalCenter: parent.verticalCenter
            text: name
        }

        states: [
            State {
                name: 'hover'
                when: _ma.containsMouse
                PropertyChanges {
                    target: _rec
                    color: '#99CCFF'
                }
            }
        ]
    }
    MouseArea {
        id: _ma
        anchors.fill: parent
        hoverEnabled: true
        cursorShape: Qt.PointingHandCursor

        onClicked: {
            if(name != selfName) channelAddActive('User:' + name);
        }
    }
}
