
$('form').find('button[type=submit]').on('click', function(){
    $("#loader").modal('show');
});
$(window).on('load', function(){
    $("#loader").modal('hide');
});
$(window).ready(function(){
    $("#loader").modal('show');
});