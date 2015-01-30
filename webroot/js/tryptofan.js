(function() {
    var websocket;
    var lastUrl = "";
    var bladeSelect = $("#blade-select");
    var bladeMode = $("#blade-mode");
    var bladeSpeed = $("#blade-speed");
    var bladeColor = $("#blade-color");
    var currentBlade = 0;
    var state = [[0, 0, 0], [0, 0, 0], [0, 0, 0]];


    function connect() {
        if (websocket !== undefined) {
            websocket.close();
        }

        websocket = new WebSocket("ws://" + document.location.host + "/ws");
        websocket.onopen = onWebsocketOpen;
        websocket.onclose = onWebsocketClose;
        websocket.onmessage = onWebsocketMessage;
        websocket.onerror = onWebsocketError;
    }

    function sendState() {
        websocket.send(JSON.stringify(state));
    }

    function onWebsocketOpen(event) {
        console.log("Websocket open");
    }

    function onWebsocketClose(event) {
        console.log("Websocket closed...");
    }

    function onWebsocketMessage(event) {
        state = JSON.parse(event.data);

        bladeSpeed.val(state[currentBlade][1]);
        bladeColor.val(state[currentBlade][2]);
    }

    function onWebsocketError(event) {
        alert("Could not connect to Tryptofan!")
    }

    bladeMode.on("click", function() {
        state[currentBlade][0] += 1;
        state[currentBlade][0] %= 255;
        sendState();
    });

    bladeSpeed.on("change", function(event) {
        state[currentBlade][1] = parseInt(event.target.value);
        sendState();
    });

    bladeColor.on("change", function(event) {
        state[currentBlade][2] = parseInt(event.target.value);
        sendState();
    });

    bladeSelect.on("change", function(event) {
        currentBlade = parseInt(event.target.value);
        bladeSpeed.val(state[currentBlade][1]);
        bladeColor.val(state[currentBlade][2]);
    });

    // silly hack for touch
    $(".btn").mouseup(function(){
        $(this).blur();
    });

    connect();

})();
