document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    let room = "room1";
    joinRoom("room1");

    // Display incoming messages
    socket.on('message', data => {
        const p = document.createElement('p');
        const span_username = document.createElement('span')
        const span_timestamp = document.createElement('span')
        const br = document.createElement('br');

        if (data.username) {
            span_username.innerHTML = data.username;
            span_timestamp.innerHTML = data.time_stamp;
            p.innerHTML = span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML;
            document.querySelector('#display-message-section').append(p);
        } else {
            printSysMsg(data.msg)
        }
    });

    // Send message
    document.querySelector('#send_message').onclick = () => {
        socket.send({'msg': document.querySelector('#user_message').value,
                    'username': username, 'room': room});
        // Clear input area
        document.querySelector('#user_message').value = '';
    };

    // Room selection
    document.querySelectorAll('.select-room').forEach(p => {
        p.onclick = () => {
            let newRoom = p.innerHTML;
            if (newRoom == room) {
                msg = `You are already in ${room} room.`
                printSysMsg(msg);
            } else {
                leaveRoom(room);
                joinRoom(newRoom);
                room = newRoom;
            }
        }
    });

    // Leave room
    function leaveRoom(room) {
        socket.emit('leave', {'username': username, 'room': room})
    }

    // Join room
    function joinRoom(room) {
        socket.emit('join', {'username': username, 'room': room})
        // Clear message area
        document.querySelector('#display-message-section').innerHTML = ''
        // Autofocus on text box
        document.querySelector('#user_message').focus();
    }

    // Print system message
    function printSysMsg(msg) {
        const p = document.createElement('p');
        p.innerHTML = msg;
        document.querySelector('#display-message-section').append(p);
    }

    var video = document.getElementById("videoId")

    video.onplay = () => {
        console.log("video is playing");
        socket.emit("play-video", true);
    };

    socket.on('onplay event', onplay => {
        console.log("got onplay event!");
        if (onplay["onplay"]) {
//            document.getElementById("videoId").play();
            video.play();
        }

    });

//    var video = document.getElementById("videoId")
    video.onpause = () => {
        console.log("video is paused");
        socket.emit("pause-video", true);
    };

    socket.on('onpause event', onpause => {
        console.log("got onpause event!");
        if (onpause["onpause"]) {
//            document.getElementById("videoId").pause();
            video.pause();
        }
    });

//    var video = document.getElementById("videoId")
    video.ontimeupdate = () => {
        var current_position = video.currentTime;
        socket.emit("change-video-position", current_position);
    };

    socket.on('change video position event', current_position => {
        console.log("got change video position event!");
//        var video = document.getElementById("videoId")
        if (video.currentTime != current_position["current_position"]) {
            video.currentTime = current_position["current_position"];
        }
        else {
            console.log("position in the same");
        }
    })
})