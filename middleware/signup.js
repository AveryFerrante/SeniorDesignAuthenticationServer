
$( document ).ready(function() {

  $( "#registerButton" ).click(function() {
    var uname = $( "#usernameInput" ).val().trim();
    var pword = $( "#passwordInput" ).val().trim();


    if(!uname || !pword) {
      alert("Must enter a password & username");
    }
    else {

      $.post( "createAccount/", { username: uname, password: pword }, function( data ) {

        if( data.trim() === "Success" ) {
            alert( "Successfully Registered" );
        }
        else { // Error attempting to sign up
          alert("There was an error registering");
        }
      });

    }
  });

  $( "#loginButton" ).click(function() {
    var uname = $( "#usernameInput" ).val().trim();
    var pword = $( "#passwordInput" ).val().trim();

    if(!uname || !pword) {
      alert("Must enter a password & username");
    }
    else {

      $.post( "login/", { username: uname, password: pword }, function( data ) {

        alert( data );
        if( data.trim() === "Granted" ) {
            alert( "Successfully Logged In" );
        }
        else { // Error attempting to sign up
          alert("There was an error logging in");
        }
      });

    }

  });

});
