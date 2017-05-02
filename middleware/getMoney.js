$(document).ready(function() {

  var urlSplit = window.location.href.split("?");
  var paramSplit = urlSplit[1].split("=");
  var c = paramSplit[1];


  setInterval(function() {
    $.post("moneyChecker/", {code: c}, function(data) {
      $("#amount").text(data);
    })
  }, 3000);




})
