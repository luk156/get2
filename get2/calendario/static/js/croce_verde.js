$(document).ready(function() {
    $('.persona-turno.hide').each(function() {
        if ($(this).parent().parent().hasClass('persone-requisito-6')) {
            $(this).removeClass('hide');
        }
    });
    window.setTimeout(function() {
        $('.persona-mansione-turno:not(.hide)').each(function() {
            if ($(this).attr('data-content').search('icon-ambulance') != -1) {
                this.insertAdjacentHTML('beforeend', '<i class="icon-ambulance"></i>');
            };
        });
    }, 200);
});