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
})