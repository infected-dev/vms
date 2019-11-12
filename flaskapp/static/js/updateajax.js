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

$(document).ready(function(){

    $('.updatevehicles').on('click', function(){
        
        var id = $(this).attr('attributes');
    
       var out_time = $('#outtime'+id).val()
    
       //alert(out_time);
       req = $.ajax({
        url : '/vehicles/update',
        type : 'POST',
        data : {VeID : id , outtime:out_time}
        });

        $('#datasectionveh'+id).fadeOut(1000).fadeIn(1000);

    });
       
});

$(document).ready(function(){

    $('.updatemill').on('click', function(){
        
        var id = $(this).attr('attributes');
    
       var in_time = $('#intime'+id).val()
    
       req = $.ajax({
        url : '/vehicles/mill/update',
        type : 'POST',
        data : {vid : id , intime:in_time}
        }); 

        $('#datasectionmill'+id).fadeOut(1000).fadeIn(1000);

    });
       
});