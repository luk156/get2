$(document).ready(function() {

	if ($(window).width()>756){
	 for (var i=1;i<9;i++)
	    {
	        var h_max=0;
	        $(".turno."+i).each(function(){
	            h=$(this).offset().top + $(this).height() + 8;
	            if (h>h_max){h_max=h;}
	        });
	        console.log(h_max);
	        $(".turno."+(i+1).toString()).each(function(){ $(this).offset({top:h_max}) });
	    }};
});