$(document).ready(function() {
    $('.persona-turno.hide').each(function() {
        if ($(this).parent().parent().hasClass('persone-requisito-3')) {
            $(this).removeClass('hide');
        }
    });
    $('.persona-turno:not(.hide)').each(function() {
        if ($(this).attr('data-content').search('icon-ambulance')!= -1){
        	this.insertAdjacentHTML('beforeend', '<i class="icon-ambulance"></i>');
        };
    });
});