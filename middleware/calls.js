
$( document ).ready(function() {

  $( "#image1" ).click(function() {
    var inputs = getUsernameAndPass();

    if(!inputs[0] || !inputs[1]) {
      alert("Must enter a password & username");
    }
    else {
      registrationPostCall(inputs, 1)
    }
  });

  $( "#image2" ).click(function() {
    var inputs = getUsernameAndPass();

    if(!inputs[0] || !inputs[1]) {
      alert("Must enter a password & username");
    }
    else {
      registrationPostCall(inputs, 2)
    }
  });

  $( "#image3" ).click(function() {
    var inputs = getUsernameAndPass();

    if(!inputs[0] || !inputs[1]) {
      alert("Must enter a password & username");
    }
    else {
      registrationPostCall(inputs, 3)
    }
  });

  $( "#loginButton" ).click(function() {
    var inputs = getUsernameAndPass();

    if(!inputs[0] || !inputs[1]) {
      alert("Must enter a password & username");
    }
    else {

      $.post( "login/", { username: inputs[0], password: inputs[1] }, function( data ) {
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

  }); // Close loginButton function

}); // Close Document ready

function getUsernameAndPass() {
  var uname = $( "#usernameInput" ).val().trim();
  var pword = $( "#passwordInput" ).val().trim();
  var fullList = [uname, pword];
  return fullList;
}


function registrationPostCall(inputs, imgNumber) {
  $.post( "createAccount/", { username: inputs[0], password: inputs[1], imageNumber: imgNumber }, function( data ) {

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
