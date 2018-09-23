$(document).ready(function() {
    // Use a "/test" namespace.
    // An application can open a connection on multiple namespaces, and
    // Socket.IO will multiplex all those connections on a single
    // physical channel. If you don't care about multiple channels, you
    // can set the namespace to an empty string.
    namespace = '/test';

    // Connect to the Socket.IO server.
    // The connection URL has the following format:
    //     http[s]://<domain>:<port>[/<namespace>]
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);

    var _table_ = document.createElement('table'),
    _tr_ = document.createElement('tr'),
    _th_ = document.createElement('th'),
    _td_ = document.createElement('td');
    _table_.className = 'table table-dark';

    // Builds the HTML Table out of json data.
     function buildHtmlTable(arr) {
         var table = _table_.cloneNode(false),
             columns = addAllColumnHeaders(arr, table);

         for (var i=0, maxi=arr.length; i < maxi; ++i) {
             var tr = _tr_.cloneNode(false);

             for (var j = 0, maxj = columns.length; j < maxj ; ++j) {
                 var td = _td_.cloneNode(false);
                     cellValue = arr[i][columns[j]];

                 td.appendChild(document.createTextNode(arr[i][columns[j]] || ''));
                 tr.appendChild(td);
             }
             table.appendChild(tr);
         }
         return table;
     }

     // Adds a header row to the table and returns the set of columns.
     // Need to do union of keys from all records as some records may not contain
     // all records
     function addAllColumnHeaders(arr, table)
     {
         var columnSet = [],
             tr = _tr_.cloneNode(false);

         for (var i = 0, l = arr.length; i < l; i++) {

             for (var key in arr[i]) {
                 if (arr[i].hasOwnProperty(key) && columnSet.indexOf(key) === -1) {
                     columnSet.push(key);
                     var th = _th_.cloneNode(false);
                     th.appendChild(document.createTextNode(key));
                     tr.appendChild(th);
                 }
             }
         }
         table.appendChild(tr);
         return columnSet;
     }

    // Event handler for new connections.
    // The callback function is invoked when a connection with the
    // server is established.
    socket.on('connect', function() {
        socket.emit('my_event', {data: 'New connection'});
    });

    // Event handler for server sent data.
    // The callback function is invoked whenever the server emits data
    // to the client. The data is then displayed in the "Received"
    // section of the page.
    socket.on('my_response', function(msg) {
        var output = $.parseJSON(msg);
        if (output !== null){
            $('#rt-table').html(buildHtmlTable(output));
        }
    });

    // Handlers for the different forms in the page.
    // These accept data from the user and send it to the server in a
    // variety of ways
    $('form#disconnect').submit(function(event) {
        socket.emit('disconnect_request');
        return false;
    });
});