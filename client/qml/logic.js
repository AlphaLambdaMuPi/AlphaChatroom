
var activeChannel = ''
function receive_msg(s) {
  console.log(s)
    mainView.chatMod.append(s);
}

function onLoggedIn() {
  loader.source = ""
    loader.sourceComponent = waitingComp
    rootApp.width = 800
}

function channelAdd(ch) {
  console.log(loader.source)
    mainView.channelMod.append({channel: ch})
}

function loginFinish() {
  loader.sourceComponent = undefined
    loader.source = 'main.qml'
    medium.Qjoin('Lobby')
}

function setActiveChannel(ch) {
  activeChannel = ch
}
