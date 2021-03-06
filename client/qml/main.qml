import QtQuick 2.4
import QtQuick.Controls 1.3
import QtQuick.Layouts 1.1
import QtQuick.Controls.Styles 1.3
import QtGraphicalEffects 1.0
import QtQuick.Dialogs 1.2
import QtMultimedia 5.4

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
                                    delegate: Loader {
                                        id: _loader
                                        width: childrenRect.width
                                        height: childrenRect.height
                                        property var modelData: model
                                        sourceComponent: {
                                            print(model.type)
                                            if( type == 'text' ) return chatTextDelegate;
                                            else if( type == 'file' ) return chatFileDelegate;
                                            else if( type == 'streaming' ) return chatStreamingDelegate;
                                            else if( type == 'streamingIndicate' ) return streamingIndicator;
                                        }
                                    }
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
                                //delegate: Loader {
                                    //id: _loader
                                    //width: 100
                                    //height: 100
                                    //property var modelData: model
                                    //sourceComponent: {
                                        //if( model.type == 'text' ) return chatTextDelegate;
                                    //}
                                //}
                                add: Transition {
                                    id: _t
                                    ParallelAnimation {
                                        NumberAnimation {
                                            properties: 'y'
                                            from: _t.ViewTransition.destination.y + 100
                                            easing.type: Easing.OutBounce
                                            duration: 500
                                        }
                                        NumberAnimation {
                                            properties: 'scale'
                                            from: 0.0
                                            to: 1.0
                                            easing.type: Easing.OutBounce
                                            duration: 500
                                        }
                                    }
                                }
                                displaced: Transition {
                                    id: _t2
                                    SequentialAnimation {
                                        NumberAnimation {
                                            properties: 'y'
                                            easing.type: Easing.OutBounce
                                            duration: 500
                                        }
                                    }
                                }
                                remove: Transition {
                                    id: _t3
                                    SequentialAnimation {
                                        NumberAnimation {
                                            properties: 'scale'
                                            from: 1.0
                                            to: 0
                                            easing.type: Easing.InBack
                                            easing.overshoot: 1.8
                                            duration: 500
                                        }
                                    }
                                }
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
        id: chatTextDelegate
        Row {
            property var datas: parent.modelData.data
            Component.onCompleted: {
                print(datas.mesg)
            }
            width: parent.width
            height: childrenRect.height
            spacing: 0
            Image {
                id: picRec
                source: 'Image://avatarImage/' + datas.sender
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
                        text: datas.mesg
                        wrapMode: Text.Wrap
                        width: Math.min(parent.parent.parent.parent.width - rec.tmargin * 2 - picRec.width, implicitWidth)
                        textFormat: Text.RichText
                        Component.onCompleted: {
                            //console.log(implicitWidth, parent.parent.parent.parent.parent.width - rec.tmargin*2 - picRec.width, width)
                        }
                        onLinkActivated: {
                            Qt.openUrlExternally(link)
                        }
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
                        text: datas.sender + ' @' + datas.timeStr
                        color: '#444'
                    }
                }
            }
        }
    }

    Component {
        id: chatFileDelegate
        Row {
            property var datas: parent.modelData.data
            width: parent.width
            height: childrenRect.height
            spacing: 0
            Image {
                id: picRec
                source: 'Image://avatarImage/' + datas.sender
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
                    id: rec
                    width: childrenRect.width + 30
                    height: childrenRect.height + 22
                    Image {
                        id: _img
                        source: '../img/file_cute.png'
                        width: 80
                        height: 80
                        anchors {
                            horizontalCenter: parent.horizontalCenter
                            top: parent.top
                            topMargin: 20
                        }
                    }
                    Text {
                        id: _tx
                        text: datas.file_name + ' (' + (datas.file_size/1000).toFixed(2) + 'KB)'
                        anchors {
                            horizontalCenter: parent.horizontalCenter
                            top: _img.bottom
                        }
                    }
                    Rectangle {
                        id: _o
                        width: 24
                        height: 24
                        radius: 24
                        color: 'green'
                        anchors {
                            top: _tx.bottom
                            topMargin: 10
                            left: parent.left
                            leftMargin: 20
                            //bottom: parent.bottom
                            //bottomMargin: 10
                        }
                        Image {
                            source: '../img/check.png'
                            width: 20
                            height: 20
                            anchors.centerIn: parent
                        }
                        MouseArea {
                            anchors.fill: parent
                            cursorShape: Qt.PointingHandCursor
                            onClicked: {
                                medium.QstartGetFile(datas.file_name, datas.token);
                                rec.state = 'progressing'
                            }
                        }
                    }

                    Rectangle {
                        id: _x
                        width: 24
                        height: 24
                        radius: 24
                        color: 'red'
                        anchors {
                            top: _tx.bottom
                            topMargin: 10
                            right: parent.right
                            rightMargin: 20
                            //bottom: parent.bottom
                            //bottomMargin: 10
                        }
                        Image {
                            source: '../img/delete.png'
                            width: 20
                            height: 20
                            anchors.centerIn: parent
                        }
                    }

                    ProgressBar {
                        id: _pb
                        value: 0
                        anchors {
                            top: _tx.bottom
                            topMargin: 10
                            horizontalCenter: parent.horizontalCenter
                        }
                        visible: false
                        Component.onCompleted: {
                            tokenToProgress[datas.token] = _pb
                        }
                        function addByte(l) {
                            value += l/datas.file_size;
                        }
                        Text {
                            anchors.centerIn: parent
                            text: Math.round(parent.value * 100) + '%'
                        }
                    }

                    Rectangle {
                        id: _l
                        anchors {
                            top: _o.bottom
                            left: parent.left
                            right: parent.right
                            topMargin: 10
                            leftMargin: 5
                            rightMargin: 5
                            bottomMargin: 0
                        }
                        height: 1
                        color: 'grey'
                    }

                    Text {
                        id: senderText
                        anchors {
                            top: _l.bottom
                            left: parent.left
                            right: parent.right
                            topMargin: 0
                            leftMargin: 20
                            rightMargin: 7
                            bottomMargin: 0
                        }
                        text: datas.sender + ' @' + datas.timeStr
                        color: '#444'
                    }

                    states: [
                        State {
                            name: 'progressing'
                            PropertyChanges {
                                target: _pb
                                visible: true
                            }
                            PropertyChanges {
                                target: _o
                                visible: false
                            }
                            PropertyChanges {
                                target: _x
                                visible: false
                            }
                        }
                    ]
                }
            }

        }
    }

    Component {
        id: chatStreamingDelegate
        Row {
            property var datas: parent.modelData.data
            width: parent.width
            height: childrenRect.height
            spacing: 0
            Image {
                id: picRec
                source: 'Image://avatarImage/' + datas.sender
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
                    id: rec
                    width: childrenRect.width + 30
                    height: childrenRect.height + 30
                    Image {
                        id: _img
                        source: '../img/video_cute.png'
                        width: 80
                        height: 80
                        anchors {
                            horizontalCenter: parent.horizontalCenter
                            top: parent.top
                            topMargin: 20
                        }
                    }
                    Text {
                        id: _tx
                        text: datas.sender + ' has started a broadcast'
                        anchors {
                            horizontalCenter: parent.horizontalCenter
                            top: _img.bottom
                        }
                    }
                    Rectangle {
                        id: _o
                        width: 24
                        height: 24
                        radius: 24
                        color: 'green'
                        anchors {
                            top: _tx.bottom
                            topMargin: 10
                            left: parent.left
                            leftMargin: 20
                            //bottom: parent.bottom
                            //bottomMargin: 10
                        }
                        Image {
                            source: '../img/check.png'
                            width: 20
                            height: 20
                            anchors.centerIn: parent
                        }
                        MouseArea {
                            anchors.fill: parent
                            cursorShape: Qt.PointingHandCursor
                            onClicked: {
                                //medium.QstartGetStreaming(datas.url);
                                //rec.state = 'progressing'
                                _d.open()
                                _mp.play()
                            }
                        }
                        MediaPlayer {
                            id: _mp
                            autoLoad: false
                            autoPlay: false
                            source: datas.url
                        }
                        Dialog {
                            id: _d
                            visible: false
                            title: datas.sender + "'s broadcast"
                            width: 600
                            height: 600
                            modality: Qt.NonModal

                            VideoOutput {
                                width: 600
                                height: 450
                                anchors {
                                    top: parent.top
                                    left: parent.left
                                    right: parent.right
                                }
                                source: _mp
                                Component.onCompleted: {
                                    console.log(_mp)
                                }
                            }
                            standardButtons: StandardButton.Close
                            onRejected: {
                                _mp.stop()
                            }
                        }
                    }

                    Rectangle {
                        id: _x
                        width: 24
                        height: 24
                        radius: 24
                        color: 'red'
                        anchors {
                            top: _tx.bottom
                            topMargin: 10
                            right: parent.right
                            rightMargin: 20
                            //bottom: parent.bottom
                            //bottomMargin: 10
                        }
                        Image {
                            source: '../img/delete.png'
                            width: 20
                            height: 20
                            anchors.centerIn: parent
                        }
                    }


                }
            }

        }
    }

    Component {
        id: streamingIndicator

        Rectangle {
            id: _rec
            color: 'blue'
            width: 400
            height: 60
            radius: 4

            Behavior on height {
                NumberAnimation {
                    easing.type: Easing.InOutQuad
                }
            }

            Text {
                id: _t
                anchors.centerIn: parent
                color: 'white'
                text: 'You have just started a streaming, click to stop'
            }

            MouseArea {
                anchors.fill: parent
                onClicked: {
                    medium.QcallReleaseFeed(activeChannel)
                    _rec.height = 0
                    _t.visible = false
                }
                cursorShape: Qt.PointingHandCursor
            }
        }
    }

}
