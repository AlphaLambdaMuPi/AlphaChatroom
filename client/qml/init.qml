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
    property variant chatModels: new Object()
    property variant chatUsersModels: new Object()
    property variant tokenToProgress: new Object()

    function receive_msg(ch, s) {

        if (!(ch in chatModels)) {
            channelAdd(ch, false)
        }
        chatModels[ch].append(s);
        if ( ch == activeChannel ) {
            var timer = _timerToBottom
            timer.start()
        } else {
            console.log(mainView.cl)
            mainView.cl.newMessage(ch)
        }
    }

    function receiveUserJoin(ch, x) {
        chatUsersModels[ch].append(x);
    }

    function onLoggedIn() {
        loader.source = ""
        loader.sourceComponent = waitingComp
        rootApp.width = 900
    }

    function channelAdd(ch) {
        mainView.channelMod.append({channel: ch})
        var newModel = listDelegate.createObject(rootApp)
        chatModels[ch] = newModel

        newModel = listDelegate.createObject(rootApp)
        chatUsersModels[ch] = newModel
        refreshUsersList(ch)
    }

    function channelAddActive(ch) {
        channelAdd(ch)
        setActiveChannel(ch)
    }

    function refreshUsersList(ch) {
        medium.QgetUsers(ch)
    }

    function receiveChatUsersList(ch, ls) {
        mainView.userView.model = chatUsersModels[ch]
        var mod = chatUsersModels[ch]
        mod.clear()
        ls.forEach( function(x) {
            mod.append(x)
        });
    }

    Component {
        id: listDelegate
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
        mainView.userView.model = chatUsersModels[ch]
        mainView.cl.changeActiveChannel(ch)
        scrollToBottom()
    }

    function leaveChannel(ch, index) {
        if(activeChannel == ch) {
            activeChannel = 'Lobby'
            mainView.cl.changeActiveChannel('Lobby')
        }
        mainView.channelMod.remove(index)
        delete chatModels[ch]
        delete chatUsersModels[ch]
        medium.QleaveChannel(ch)
    }

    Timer {
        id: _timerToBottom
        interval: 100
        repeat: false
        onTriggered: {
            scrollToBottom()
        }
    }

    function scrollToBottom() {
        //mainView.chatScroll.flickableItem.contentY = 1000000
        //console.log(mainView.chatScroll.flickableItem.contentHeight)
        mainView.chatScroll.animation.to = Math.max(mainView.chatScroll.flickableItem.contentHeight -
                                           mainView.chatScroll.height, 0)
        //mainView.chatScroll.animation.to = 10
        mainView.chatScroll.animation.start()
    }

    function refreshProgress(token, l) {
        tokenToProgress[token].addByte(l)
    }
}
