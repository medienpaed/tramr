var intervall = 100;
var counter = 0;
var red = 256;
var green = 256;
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
    var factor = zeit/256;
    $('#button').hide();
    if (zeit == 9999) {
      $('#anzeige').text('...erst morgen frueh wieder verfuegbar. :-)');
    } else {
      counter = setInterval(function(){
        zeit = zeit - 0.1;
        if (zeit < 0) {
          $('#anzeige').hide();
          $('#button').show();
        } else {
          red = 256 - (Math.round(Math.round(zeit)/factor));
          green = 256 - red;
          hexred = ('00' + red.toString(16).toUpperCase()).slice(-2);
          hexgreen = ('00' + green.toString(16).toUpperCase()).slice(-2);
          colstring = '#'+hexred+hexgreen+'00';
          $('#anzeige').text(fancyTimeFormat(zeit));
          $('body').css('background-color', colstring);
        }
      },intervall);
    }
});
