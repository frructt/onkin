document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('connect', () => {
        socket.send('I\'m connected!');
    })

    socket.on('message', data => {
        console.log(`Message received: ${data}`)
    });

    socket.on('some event', data => {
        console.log(data);
    });

    var video = document.getElementById("videoId")
    video.onplay = () => {
        console.log("video is playing");
        socket.emit("play-video", true);
    };

    socket.on('onplay event', onplay => {
        // console.log("got video element!");
        if (onplay["onplay"]) {
            document.getElementById("videoId").play()
        }
    });

    var video = document.getElementById("videoId")
    video.onpause = () => {
        console.log("video is paused");
        socket.emit("pause-video", true);
    };

    socket.on('onpause event', onpause => {
        if (onpause["onpause"]) {
            document.getElementById("videoId").pause()
        }
    });
})