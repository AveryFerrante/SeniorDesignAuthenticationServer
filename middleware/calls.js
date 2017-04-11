
$( document ).ready(function() {

  $( "#createAccountButton" ).click(function() {
    var uname =   $( "#usernameInput" ).val(); // 50 chars max, check this
    var pword =   $( "#passwordInput" ).val();
    var pphrase = $( "#passphraseInput" ).val(); // 255 chars max, check this

    if(!uname || !pword || !pphrase) {
      alert("Must enter ALL required data");
    }
    else{
      $.post( "createAccount/", { username: uname, password: pword, phrase: pphrase }, function( data ) {

        data = data.trim();
        if( data === "Success" ) {
            alert( "Successfully Registered" );
        }
        else if( data === "UsernameError") {
          alert("This username cannot be used, please select a different one");
        }
        else { // Error attempting to sign up
          alert("There was an error registering");
        }
      });
    }
  });




  $( "#loginButton" ).click(function() {
    var uname = $( "#usernameInput" ).val();
    var pword = $( "#passwordInput" ).val();
    var code = $( "#qrCode" ).val().trim();

    if(!uname || !pword) {
      alert("Must enter a password & username");
    }
    else {

      $.post( "login/", { username: uname, password: pword }, function( data ) {
        if( data.trim() === "Granted" ) {
            alert( "Successfully Logged In" );
        }
        else if( data.trim() === "MissingArgument" ){ // Error attempting to sign in
          alert("Missing Argument: Username or Password");
        }
        else { // Only other response possible is "NotFound"
          alert("No matching credentials")
        }
      });

    }

    if(!code)
      alert("Please enter the scanned QR code");
    else {

      $.post( "qrScan/", { qrCode: code }, function( data ) {
        alert(data);
      });

    }

  }); // Close loginButton function

}); // Close Document ready
