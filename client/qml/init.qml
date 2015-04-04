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
                    loginFinish()
                }
            }
        }
    }

    Loader {
        anchors.fill: parent
        visible: true
        id: loader
        source: 'login.qml'
        //sourceComponent: ss
    }

    Component {
        id: waitingComp
        Rectangle {
            color: '#222222'
        }
    }


    property string activeChannel: ''
    property variant chatModels: {'a': 10}
    property variant zzz: {'a': 10}
    function receive_msg(ch, s) {
        console.log(ch, s)
        chatModels[ch].append(s);
        console.log(chatModels[ch])
        console.log(mainView.chatView.model)
    }

    function onLoggedIn() {
        loader.source = ""
        loader.sourceComponent = waitingComp
        rootApp.width = 800
    }

    function channelAdd(ch) {
        console.log(ch)
        mainView.channelMod.append({channel: ch})
        var newModel = chatDelegateComponent.createObject(rootApp)
        console.log(newModel)
        chatModels[ch] = newModel
        console.log('ZZZZ: ', chatModels)
    }

    Component {
        id: chatDelegateComponent
        ListModel {
        }
    }

    function loginFinish() {
        loader.sourceComponent = undefined
        loader.source = 'main.qml'
        medium.Qjoin('Lobby')
    }

    function setActiveChannel(ch) {
        activeChannel = ch
        mainView.chatView.model = chatModels[ch]
    }
}
