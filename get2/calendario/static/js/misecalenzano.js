$(document).ready(function() {

    window.allinea_calendario = function(){
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
        $('.row-fluid.calendario').height(h-th+60);
        };
    };
    window.setTimeout(window.allinea_calendario,500);

});