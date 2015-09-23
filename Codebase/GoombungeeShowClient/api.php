<?php

    /*
     * The name is somewhat of a lie. This is simply an intermedairy
     * between JavaScript and python.
     */
    
    /* JavaScript Code:
     * 
    $.ajax({
       type: "POST",
       url: "api.php",
       data: {message: "{'command':'Ping'}"},
       success: function(data){console.log(data);},
       dataType: "text"
      });
     * 
     */

    $host = "localhost";
    $port = 1998;
    
    if(!($sock = socket_create(AF_INET, SOCK_STREAM, 0)))
    {
        $errorcode = socket_last_error();
        $errormsg = socket_strerror($errorcode);     
        die("Couldn't create socket: [$errorcode] $errormsg \n");
    }
    
    if(!socket_connect($sock , $host , $port))
    {
        $errorcode = socket_last_error();
        $errormsg = socket_strerror($errorcode);
        die("Could not connect: [$errorcode] $errormsg \n");
    }

    
    $message = $_POST["message"];
    if(!socket_send( $sock, $message, strlen($message), 0))
    {
        $errorcode = socket_last_error();
        $errormsg = socket_strerror($errorcode);         
        die("Could not send data: [$errorcode] $errormsg \n");
    }
        
    $rx = socket_read($sock, 512, PHP_NORMAL_READ);
    echo $rx;
    
    socket_close($sock);

?>