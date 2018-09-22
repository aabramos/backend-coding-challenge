var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('connect', function(){
    socket.emit('client_connected', {data: 'New client!'});
});