$(document).ready(function() {
    var div_persone = $('#persone');
    $('select', div_persone).attr('disabled', 'disabled');
    $('.box-header.persone > .btn-group', div_persone).html('<a href="#" class="btn" onclick="Dajaxice.persone.sync_misecampi(Dajax.process,{});"><i class="icon-refresh"> </i> Sincronizza</a>"')
    $('td[data-title=Operazioni]', div_persone).html('');
    var div_utenti = $('#utenti');
    $('.utente_persona', div_utenti).attr('disabled', 'disabled');
    $('td[data-title=Operazioni]', div_utenti).html('');
    $('.btn', div_utenti).remove();
    var th=0;
    var h=0;
    if ($(window).width()>756){
     for (var i=1;i<9;i++)
        {
            var h_max=0;
            $(".turno."+i).each(function(){
                th = $(this).height();
                h=$(this).offset().top + th + 8;
                if (h>h_max){h_max=h;}
            });
            $(".turno."+(i+1).toString()).each(function(){ $(this).offset({top:h_max}) });
        }
    $('.row-fluid.calendario').height(h-th-8);
    };
    $('#footer').prepend('<div class="campi_footer">Per qualsiasi necessità o per richiedere i dati d’accesso utilizzare l’apposito modello o inviare una mail a <a href="mailto:informatico@misericordia-campi-bisenzio.it">informatico@misericordia-campi-bisenzio.it</a></div><hr>')
});