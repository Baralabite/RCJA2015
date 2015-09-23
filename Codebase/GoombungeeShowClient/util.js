
function api(command) {
    function callback(data){
        data = JSON.parse(data);
        console.log(data);
        if (data.response=="turnDone") {
            $.mobile.changePage("turnupdialog.html");
        }
    }
    $.ajax({
        type: "POST",
        url: "api.php",
        data: {message: "~'command':'{}'~".format(command)},
        success: callback,
        dataType: "text"
    });
}

if ("connections" in $.cookie()) {
    $.cookie("connections", parseInt($.cookie("connections"))+1, { expires:20 });
} else {
    $.cookie("connections", 1, { expires: 20 });
}

String.prototype.format = function () {
    var i = 0, args = arguments;
    return this.replace(/{}/g, function () {
        return typeof args[i] != 'undefined' ? args[i++] : '';
    });
}

/* Randomly generates a string ID thingy. */
function generateID(){
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    for( var i=0; i < 5; i++ )
        text += possible.charAt(Math.floor(Math.random() * possible.length));            
    return text;
}

   
function turnOn(){
    api("robot {} {}".format(clientID, "turnOn"));
}

function turnOff(){
    api("robot {} {}".format(clientID, "turnOff"));
}
   
function closeJaw(){
    api("robot {} {}".format(clientID, "closeJaw"));
}

function openJaw(){
    api("robot {} {}".format(clientID, "openJaw"));
}

function rollJaw() {
    api("robot {} {} {}".format(clientID, "rollJaw", $("#jawRollSlider").val()));
}

function pitchJaw() {
    api("robot {} {} {}".format(clientID, "pitchJaw", $("#jawPitchSlider").val()));
}

function yawJaw() {
    api("robot {} {} {}".format(clientID, "yawJaw", $("#jawYawSlider").val()));
}

/* Tail Modification Code */
function pitchTail() {
    api("robot {} {} {}".format(clientID, "pitchTail", $("#tailPitchSlider").val()));
}

function yawTail() {
    api("robot {} {} {}".format(clientID, "yawTail", $("#tailYawSlider").val()));
}

/* Sequence Code */
function shakeTail() {
    api("robot {} {}".format(clientID, "shakeTail"));
}

function mexicanWave() {
    api("robot {} {}".format(clientID, "mexicanWave"));
}   