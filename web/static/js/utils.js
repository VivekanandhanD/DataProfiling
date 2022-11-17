function connect(id){
//    $.get({
//        url: 'tables/' + id,
//        data: {id:id}
//    }).done(function(d){
////        console.log(d);
//        document.documentElement.innerHTML = d;
//    }).fail(function(e){
//        console.error(e);
//    });
    $("#loader").modal('show');
    window.location.href = 'tables/' + id;
}

function columns(name){
    $("#loader").modal('show');
    window.location.href = window.location.href + name;
}

function removeConnection(id){
//    $.post({
//        url: '/',
//        data: {action:'delete',id:id}
//    }).done(function(d){
////        console.log(d);
//        document.documentElement.innerHTML = d;
//    }).fail(function(e){
//        console.error(e);
//    });
    $("#action").val('delete');
    $("#conn-id").val(id);
    $("#confirm").modal("show");
}
$(window).on('load', function(){
    $("#test-message").text('Test connection before saving');
    $("#test-connection").on("click", function(){
//        $("#action1").val("test");
//        $("#connection").submit();
        $("#loader").modal('show');
        var action = 'test';
        var dbtype = $("#dbtype").val();
        var username = $("#username").val();
        var password;
        var host = $("#host").val();
        var port = $("#port").val();
        var schema = $("#schema").val();
        var token = $("input[name=csrfmiddlewaretoken]").val();
        $('input[type=password]').each(function(){
            password = $(this).val();
        });
        $.post({
            url: '/',
            data: {action:action,dbtype:dbtype,username:username,password:password,host:host,port:port,schema:schema,csrfmiddlewaretoken:token}
        }).done(function(d){
            console.log(d);
            $("#test-message").text(d);
        }).fail(function(e){
            console.error(e);
            $("#test-message").text(e);
        }).always(function(e){
            $("#loader").modal('hide');
        });
    });
    $("#save").on("click", function(){
        var msg = $("#test-message").text();
        if(msg.trim() === 'Success'){
            $("#loader").modal('show');
            $("#action1").val("add");
            $("#connection").submit();
        }
    });
});