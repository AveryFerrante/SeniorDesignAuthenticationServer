
$( document ).ready(function() {

  $('[data-toggle="tooltip"]').tooltip();

  $( "#register" ).click(function() {
    var uname     = $( "#username" ).val(); // 50 chars max, check this
    var pword     = $( "#password" ).val(); // 20 max
    var pwordconf = $( "#confirm" ).val();
    var pinNumb   = $( "#pin").val(); // 4 digits max
    var pphrase   = $( "#passphrase" ).val(); // 255 chars max, check this

    if(!uname || !pword || !pphrase || !pinNumb || !pwordconf) {
      alert("Must enter ALL required data");
    }
    else if(!(pword === pwordconf)) {
      alert("Passwords MUST match");
    }
    else if(uname.length > 50) {
      alert("Username cannot exceed 50 characters");
    }
    else if(pword.length > 200) {
      alert("Password cannot exceed 20 characters");
    }
    else if(pphrase.length > 255) {
      alert("Passphrase cannot exceed 255 characters");
    }
    else if(isNaN(pinNumb)) {
      alert("PIN must only contain numbers");
    }
    else if(pinNumb.length != 4) {
      alert("PIN must be exactly 4 digits.")
    }
    
    else{
      $.post( "createAccount/", { username: uname, password: pword, pin: pinNumb, passphrase: pphrase }, function( data ) {

        data = data.trim();
        if( data === "Success" ) {
            alert( "Successfully Registered" );
        }
        else if(data === "NonNumericalPin") {
          alert("Must enter a pin containing only numbers.");
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

}); // Close Document ready
