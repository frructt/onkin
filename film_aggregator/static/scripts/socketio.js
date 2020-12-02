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

    // var vid = document.getElementById("videoId");
    // function myFunction() {
    //     alert(vid.paused);
    // }



    document.getElementById("videoId").onplay = () => {
        socket.send(document.getElementById("videoId").onpause)
    }

    socket.on('play_video', (data) => {
        if (!data) {
            document.getElementById("videoId").play();
        } else {
            document.getElementById("videoId").pause();
        }
        console.log(data);
            // document.getElementById("videoId").play();
    });

    // socket.on('play video event', () => {
    //     document.getElementById("videoId").play();
    // });

    // socket.on('play_video', data => {
    //     var vid = document.getElementById("videoId");
    //     socket.send("Got it");
    //     vid.onplay = function() {
    //         socket.send("The video has started to play");
    //         console.log(`The video has started to play: ${data}`);
    //     };
    // })
})