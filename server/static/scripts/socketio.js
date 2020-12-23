document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    var video = document.getElementById("videoId");
    var isPlaying = false;

    let other_username = username
    let room = "Room1";
    joinRoom("Room1");

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
            if (newRoom === room) {
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

    // Play video function
    function playVid() {
        if (video.paused && !isPlaying) {
            console.log("start playing for user " + username);
            video.play();
        } else {
            console.log("video is already played for user " + username);
        }
    }

    // Pause video function
    function pauseVid() {
        if (!video.paused && isPlaying) {
            console.log("start stopping for user " + username);
            video.pause();
        } else {
            console.log("video is already stopped for user " + username);
        }
    }

    // On video playing toggle values
    video.onplay = () => {
        isPlaying = true;
        if (other_username === username){
            console.log("video is playing from user " + username);
            socket.emit("play-video", {"username": username, "room": room});
        } else {
            console.log(" " + other_username + " != " + username);
            other_username = username;
        }
    }

    // On video pause toggle values
    video.onpause = () => {
        isPlaying = false;
        if (other_username === username){
            if (!video.seeking) {  // if seeking don't send pause event to server
                console.log("video is paused by user " + username);
                socket.emit("pause-video", {"username": username, "room": room});
            }
        } else {
            console.log(" " + other_username + " != " + username);
            other_username = username;
        }
    }

    socket.on('onplay event', data => {
        if (data["room"] === room) {
            other_username = data["username"]
            playVid();
        }
    });

    socket.on('onpause event', data => {
        if (data["room"] === room) {
            other_username = data["username"]
            pauseVid();
        }
    });

    // Change video position
    video.onseeked = () => {
        if (other_username === username){
            console.log(video.currentTime);
            socket.emit("change-video-position", {"current_position": video.currentTime, "username": username, "room": room});
        } else {
            console.log(" " + other_username + " != " + username);
            other_username = username;
        }
    };

    socket.on('change video position event', data => {
        console.log("difference in positions (sec): " + Math.abs((data["current_position"] - video.currentTime)))
        if ((video.currentTime != data["current_position"]) && data["username"] != username && data["room"] === room) {
            other_username = data["username"];
            console.log("video.currentTime: " + video.currentTime + " current_position: " + data["current_position"]);
            video.currentTime = data["current_position"];
        }
        else {
            other_username = data["username"];
            console.log("position in the same");
        }
    })
})