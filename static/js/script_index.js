var urlTramr='http://'+window.location.hostname;
var delay = (function(){
  var timer = 0;
  return function(callback, ms){
    clearTimeout (timer);
    timer = setTimeout(callback, ms);
  };
})();

$(document).ready(function(){
  $('.result_halt').hide();
  $('.result_ziel').hide();
  $('#ziel').prop( "disabled", true );
  $('#zeit').prop( "disabled", true );
  $('#output').prop( "disabled", true );
  $('#go').prop( "disabled", true );
  $('#output').val(urlTramr);

  $('#haltestelle').keyup(function() {
      delay(function(){
        haltsearch('#haltestelle','#rh','result_halt');
      }, 400 );
  });
  $('#ziel').keyup(function() {
      delay(function(){
        haltsearch('#ziel','#rz','result_ziel');
      }, 400 );
  });
  $('.result_halt').click(function(){
    $('#haltestelle').val($(this).text()+' ('+$(this).attr('dataid')+')');
    urlTramr=urlTramr+'/'+$(this).attr('dataid');
    $('#output').val(urlTramr);
    $('.result_halt').hide();
    $('#haltestelle').prop( "disabled", true );
    $('#ziel').prop( "disabled", false );
    $('#bereich_halt').removeClass('panel-info');
    $('#bereich_ziel').removeClass('panel-default');
    $('#bereich_ziel').addClass('panel-info');
    $('#bereich_halt').addClass('panel-default');
  });
  $('.result_ziel').click(function(){
    $('#ziel').val($(this).text()+' ('+$(this).attr('dataid')+')');
    urlTramr=urlTramr+'/'+$(this).attr('dataid');
    $('#output').val(urlTramr);
    $('.result_ziel').hide();
    $('#ziel').prop( "disabled", true );
    $('#zeit').prop( "disabled", false );
    $('#bereich_ziel').removeClass('panel-info');
    $('#bereich_zeit').removeClass('panel-default');
    $('#bereich_zeit').addClass('panel-info');
    $('#bereich_ziel').addClass('panel-default');
  });
  $('.result_zeit').click(function(){
    var zeitall = $(this).text().split(':');
    var min = parseInt(zeitall[0]);
    var sek = parseInt(zeitall[1]);
    var gesamt = (min*60)+sek;
    urlTramr=urlTramr+'/'+gesamt.toString();
    $('#output').val(urlTramr);
    $('#bereich_zeit').removeClass('panel-info');
    $('#bereich_zeit').addClass('panel-default');
    $('#bereich_output').removeClass('panel-default');
    $('#bereich_output').addClass('panel-success');
    $('#zeit').prop( "disabled", true );
    $('#output').prop( "disabled", false );
    $('#go').prop( "disabled", false );
  });

  $('#go').click(function(){
    window.location.href = urlTramr;
  });

});

function haltsearch(string_id,result_id,result_class) {
    $.post('/abfrage', {
        haltstring: '%'+$(string_id).val()+'%'
    }).done(function(daten) {
      var j = 0;
        $('.'+result_class).hide();
        $.each(daten,function(i,item){
            item.forEach(function(element){
              j = j+1;
              $(result_id+j.toString()).text(element[1].split('$')[0]);
              $(result_id+j.toString()).attr('dataid',element[0]);
              $(result_id+j.toString()).show();
            });
        });
    }).fail(function() {
        $(string_id).text("Error");
    });

};
