$(document).ready(function() {




  var url = $(".center").attr("src");
  var urlSplit = url.split("=");
  var c = urlSplit[2];

  setInterval(function() {
    $.post("sessionChecker/", {code: c}, function(data) {
      data = data.trim();
      if(data === "Good") {
        window.location = window.location.href + "/moneyInput.html?param=" + c;
      }
    })
  }, 3000);

})
