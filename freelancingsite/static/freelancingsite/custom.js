$(document).ready(function(){
    $('a[data-toggle=modal]').click(function () {
        var text;
        var project_name = $(this).attr('data-project-name');
        var type = $('#delete_project').attr('data-type');


        if (type != 'project') {
            text = 'Bid on ' + project_name;
        } else {
            text = project_name;
        }

        $(".modal-body .project-name").text( text );
        $(".modal-title").text( 'Delete ' + type );
    });

    $("#delete_modal").submit(function(event){
        event.preventDefault();
        var url, success_url;
        var type = $('#delete_project').attr('data-type');

        if (type != 'project') {
            url = "/project_bid/delete";
            data = {'project_bid': $('#delete_project').attr('data-project-bid-id')};
            success_url = "/project_bids";
        } else {
            url = "/project/delete";
            data = {'project_id': $('#delete_project').attr('data-project-id')};
            success_url = "/projects";
        }
        $.ajax({
            type:"POST",
            url:url,
            data:data,
            success: function(){
                window.location.href = success_url;
            }
        });
        return false;
    });

});