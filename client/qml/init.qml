import QtQuick 2.4
import QtQuick.Controls 1.3
import QtQuick.Layouts 1.1

ApplicationWindow {
    width: 300
    height: 600
    id: rootApp
    property alias mainView: loader.item

    Behavior on width {
        NumberAnimation {
            id: __tmp123ani
            duration: 600
            easing.type: Easing.InOutCubic
            onRunningChanged: {
                if (!__tmp123ani.running) {
                    loader.sourceComponent = undefined
                    loader.source = 'qml/main.qml'
                    console.log(loader.item.width)
                    mainView.channelMod.append({name: 'beta'})
                }
            }
        }
    }

    Loader {
        anchors.fill: parent
        visible: true
        id: loader
        source: 'qml/login.qml'
        //sourceComponent: ss
    }

    Component {
        id: waitingComp
        Rectangle {
            color: '#222222'
        }
    }

    function receive_msg(s) {
        console.log(s)
        mainView.chatMod.append(s);
    }

    function onLoggedIn() {
        console.log('zzz')
        loader.source = ""
        loader.sourceComponent = waitingComp
        rootApp.width = 800
    }

    function channelAdd(ch) {
        //mainView.channelMod.push({channel: ch})
    }
}
