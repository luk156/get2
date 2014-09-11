$(document).ready(function() {
	if(window.staff && !window.superuser ){
		$('.persone, .utenti, .impostazioni','#menu1').remove();
		$('.cal-action').remove();
		$('.edit-turno').remove();
		$('.gruppo-turno').css('right','10px');
	}
});