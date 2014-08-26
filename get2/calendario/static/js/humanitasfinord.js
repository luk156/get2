$(document).ready(function() {

    $('.turno').each(function(){
		var not_verificato = $('.titolo-turno-False',this).length > 0;
		if (not_verificato && $('.h6-mansione-10 span.badge-important',this).length==1 && $('.span.badge-important',this).length==1)
			$('.titolo-turno',this).css('border','1px solid rgb(252, 101, 0)').css('background','none repeat scroll 0% 0% #F89E3D');
	});

});
