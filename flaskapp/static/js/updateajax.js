$(document).ready(function(){

    $('.update').on('click', function(){
        
        var id = $(this).attr('attributes');

       var exit_time = $('#exittime'+id).val()

       //alert(exittime);

       req = $.ajax({
           url : '/visitors/update',
           type : 'POST',
           data : {vi_id : id , exittime:exit_time}
       });

       $('#datasection'+id).fadeOut(1000).fadeIn(1000);
    });

});