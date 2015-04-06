import QtQuick 2.4
import QtQuick.Controls 1.3
import QtQuick.Layouts 1.1
import QtMultimedia 5.4

ApplicationWindow {
    width: 300
    height: 300
    visible: true
    VideoOutput {
        source: camera
        Camera {
            id: camera
        }
    }
}

