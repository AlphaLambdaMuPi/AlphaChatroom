import QtQuick 2.4
import QtQuick.Controls 1.3
import QtQuick.Layouts 1.1
import QtMultimedia 5.4
import VideoProbe 1.0

ApplicationWindow {
    width: 300
    height: 300
    visible: true

    VideoOutput {
        source: media
    }

    MediaPlayer {
        id: media
        source: "rtsp://140.112.18.212:7122/test.sdp"
        autoPlay: true
      
    }
    Timer {
        running: true
        repeat: true
        interval: 1000
        onTriggered: {
            console.log(media.hasAudio)
            console.log(media.hasVideo)
        }
    }
}
