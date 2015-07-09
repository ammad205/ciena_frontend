(function(){ // TOP FUNC start
$( "#ab-container2" ).slideUp();
$( "#ab-container0" ).click(function() {
$('html, body').animate({scrollTop: '5000px'}, 800)
$(this).toggleClass("mb20");
$( "#ab-container2" ).slideToggle( "slow", function() {
// Animation complete.
});

});
var sor;
var counts = [0];
    var resizeOpts = {
      handles: "all" ,autoHide:true
    };

   $(".ditem").draggable({
                         helper: "clone",
                         cursor:"move",
                         start: function() { counts[0]++; }
                         //alert("working");
                         //$(this).attr('src', '/static/images/2a.png')
                        });

    var a=$("#myModal");
    var source = "";
    $( "#aaa" ).droppable({
      drop: function( event, ui ) {
      y= ui.draggable.clone();
       var draggable = ui.draggable;
       var id = draggable.attr("id");
            if (id=="a") { sor="/static/images/firewall.png"}
            if (id=="b") { sor="/static/images/router.png"}
            if (id=="c") { sor="/static/images/bc.png"}
            if (id=="d") { sor="/static/images/internet.png"}
            if (id=="e") { sor="/static/images/nfv-images/new-nfv-images/1i.png"}
            if (id=="f") { sor="/static/images/nfv-images/new-nfv-images/1h.png"}

       a.modal("show")
        }

    });


  //  $("#myModal").modal("show");
$('#launch-button').click(function(){

 $("#ab-container2").append("<div style='margin-left:5px;margin-top:5px;border:1px solid #3C5061;width:99%' class='row grad2' ><div style='text-align:center;font-weight:bold; color:#3C5061;padding-top:15px;' class='col-md-3'>"+$('#M-name').val() +"</div>  <div style='font-weight:bold; color:#3C5061;padding-top:15px' class='col-md-6'><div style='background-color:#DCDCDC' class='progress '><div class='abcd progress-bar progress-bar-success progress-bar-striped' role='progressbar' aria-valuenow='40' aria-valuemin='100' aria-valuemax='100' style='width: 0%'></div></div></div><div data-toggle='modal' data-target='#modelHealthMonitoring' style='font-weight:bold; color:#3C5061;text-align: right;padding-top:15px;' class='col-md-2'><div title='CPU Utilization' class='lll led-box'><div class='led-yellow'></div>CPU</div><div title='Memory Utilization' class='lll led-box'><div class='led-yellow'></div>Memory</div><div title='Network Utilization' class='lll led-box'><div class='led-yellow'></div>Network </div><div title='SLA Violation' class='lll led-box'><div class='led-yellow'></div> SLA</div></div><div style='float:right;color:#3C5061;text-align: right;padding-top:15px; font-size:20px' class='col-md-1'><strong  style='cursor:pointer;'>x</strong></div></div>");

  $.ajax({
             type: 'GET',
             url: 'ammad',
             data: {},
             success: function(result){
              alert(result)
             },
             error: function(result){

             }
     });

/*
 $.ajax({
                        type: 'POST',
                        url: 'spawnModeler',
                        data: {instance_name: $("#M-name").val(),  mngt_ntwrk: $("#M-mi").val(), left_ntwrk: $("#M-li").val(), right_ntwrk: $("#M-ri").val(), telnet:$('#telnet').is(":checked"), ssh:$('#ssh').is(":checked"), netconf:$('#netconf').is(":checked")  },
                        success: function(result){

                        },
                        error: function(){
                        }
                });


*/


$('#ab-container2>div:last>div').first().next().children().children().animate({width:'100%'},150000,function() {
// Animation complete.

var light= $(this);
var light_width = "16px"
light.parent().parent().next().children().first().children().animate({width:light_width},2000,function() {
$(this).removeClass('led-yellow').addClass('led-green');

light.parent().parent().next().children().first().next().children().animate({width:light_width},5000,function() {
$(this).removeClass('led-yellow').addClass('led-green');
light.parent().parent().next().children().first().next().next().children().animate({width:light_width},3000,function() {
$(this).removeClass('led-yellow').addClass('led-green');
light.parent().parent().next().children().first().next().next().next().children().animate({width:light_width},6000,function() {
$(this).removeClass('led-yellow').addClass('led-green');

});});});});


});








});

////////////////////////////// Check the data on windows load //////////////////////////////////////

  $.ajax({
       url: 'allData',
       success: function(result){
            for(i = 0; i < result.length; i++){

             $("#ab-container2").append("<div style='margin-left:5px;margin-top:5px;border:1px solid #3C5061;width:99%' class='row grad2' ><div style='font-weight:bold; color:#3C5061;padding-top:15px; text-align:center' class='col-md-3'>"+result[i].fields.instance_name+"</div>  <div style='font-weight:bold; color:#3C5061;padding-top:15px' class='col-md-6'><div style='background-color:#DCDCDC' class='progress '><div class='abcd progress-bar progress-bar-success progress-bar-striped' role='progressbar' aria-valuenow='40' aria-valuemin='100' aria-valuemax='100' style='width: 100%'></div></div></div><div data-toggle='modal' data-target='#modelHealthMonitoring' style='font-weight:bold; color:#3C5061;text-align: right;padding-top:15px;' class='col-md-2'><div  title='CPU Utilization' class='lll led-box'><div class='led-green'></div>CPU</div><div title='Memory Utilization' class='lll led-box'><div class='led-green'></div>Memory</div><div title='Network Utilization' class='lll led-box'><div class='led-green'></div> Network</div><div  title='SLA Violation' class='lll led-box'><div class='led-green'></div> SLA</div></div><div style='float:right;color:#3C5061;text-align: right;padding-top:15px;font-size:20px' class='col-md-1'><strong  style='cursor:pointer'>x</strong></div></div>");

            }
       },
       error: function(){

       }
    });


///////////////////////////////////////////////////////////////////////////////////////////////////////


function register_div() { // REGISTER DIV start
$(".axe" ).click(function(){
$(this).parent().parent().parent().fadeOut()

});
}  // REGISTER DIV end


})(); // TOP FUNC end
