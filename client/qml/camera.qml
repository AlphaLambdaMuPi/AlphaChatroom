import QtQuick 2.4
import QtQuick.Controls 1.3
import QtQuick.Layouts 1.1
import QtMultimedia 5.4
import VideoProbe 1.0

ApplicationWindow {
    width: 300
    height: 300
    visible: true
    id: zz
    VideoOutput {
        source: vdo
    }
    MediaPlayer {
        id: vdo
        source: "/home/meteor/Videos/big_buck_bunny.mp4"
        autoPlay: true
    }

    VideoProbe {
        id: pb
        source: vdo
        onFramed: {
            console.log('zzz')
        }
        medium: medium
    }
}

