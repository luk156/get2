$(document).ready(function() {
    $('.persona-turno.hide').each(function() {
        if ($(this).parent().parent().hasClass('persone-requisito-3')) {
            $(this).removeClass('hide');
        }
    });
});