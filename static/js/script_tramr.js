var intervall = 100;
var counter = 0;
var red = 255;
var green = 255;
var hex = '11'

function fancyTimeFormat(time)
{
    // Hours, minutes and seconds
    var hrs = ~~(time / 3600);
    var mins = ~~((time % 3600) / 60);
    var secs = time % 60;

    // Output like "1:01" or "4:03:59" or "123:03:59"
    var ret = "";
    if (hrs > 0) {
        ret += "" + hrs + ":" + (mins < 10 ? "0" : "");
    }
    ret += "" + mins + ":" + (secs < 10 ? "0" : "");
    ret += "" + secs.toFixed(1);
    return ret;
}

$(document).ready(function() {
    var zeit = parseFloat($("#anzeige").text());
    $('body').css('background-color', '#00ff00');
    if (zeit == 9999) {
      $('#anzeige').text('...erst morgen frueh wieder verfuegbar. :-)');
    } else {
      counter = setInterval(function(){
        zeit = zeit - 0.1;
        if (zeit < 0) {
          location.reload();
          zeit = 999;
        } else {
          if (zeit < 255) {
            red = 255 - Math.round(zeit);
            green = 255 - red;
            hexred = ('00' + red.toString(16).toUpperCase()).slice(-2);
            hexgreen = ('00' + green.toString(16).toUpperCase()).slice(-2);
            colstring = '#'+hexred+hexgreen+'00';
            $('body').css('background-color', colstring);
          }
          $('#anzeige').text(fancyTimeFormat(zeit));
        }
      },intervall);
    }
});
