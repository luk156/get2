$(document).ready(function() {

    $('.turno').each(function(){
		var verificato = $('.titolo-turno-True',this).length > 0;
		if (verificato && $('.persone-requisito-10 li',this).length==0)
			$('.titolo-turno',this).css('border','1px solid rgb(252, 101, 0)').css('background','none repeat scroll 0% 0% #F89E3D');
	});

});
