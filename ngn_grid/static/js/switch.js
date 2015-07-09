function initialize() {
  var mapOptions = {
    zoom: 4,
    center: {lat: 38.8833 , lng: -92.0167}
  };

  var map = new google.maps.Map(document.getElementById('map-canvas'),
      mapOptions);


var aa={name:'ddd'}
var datacenters = [
  ['New York', 40.7127, -74.0059,1],
  ['San Francisco', 37.7833, -122.4167,2],
  ['Seattle', 47.6097, -122.3331,3]
];
var marker =[];
for (var i = 0; i < datacenters.length; i++) {
    var  slice = datacenters[i];

    marker[i] = new google.maps.Marker({
    position: new google.maps.LatLng(slice[1], slice[2]),
    map: map,
    title: slice[0],
    datacentername:slice[3],
    icon : '/static/images/datacenter.png'
  });
  register(marker[i])
}




  function register(marker) {
  google.maps.event.addListener(marker, 'click', function() {

    aa.name=marker.datacentername
    vms(marker.datacentername)
    var a=$("#myModal");
    a.modal("show");
    spawn(marker.datacentername)
    connect()


  });
  }





function vms(n) {

    $.ajax({
             url: 'ammad/',
             type: 'POST',
             data: {datacentername:n},
             success: function(result){
                 $('#myModal .modal-title').empty().html("<h4><b>"+ datacenters[n-1][0] +"</b></h4>")
                 $('#vms .list-group').empty()
                for (var i = 0; i < result.length; i++) {
                    $('#vms .list-group').append("<li class='list-group-item'><span class='badge'>Active</span>"+result[i]['fields']['name']+"</li>")
                    }
             },
             error: function(result){

             }
     });
}
//------------------------------------------2nd Tab ---------------------------------------------------------------------

function spawn(n) {
    $.ajax({
             url: 'ammad2/',
             type: 'POST',
             data: {datacentername:n},
             success: function(result){
             $('#spawn #in').empty()
             for (var i = 0; i < result['images'].length; i++) {

             //alert(result['images'][i]['id'])
             $('#spawn #in').append("<div class='row a'><div class='col-lg-8'><div class='input-group'><span class='input-group-addon'><input identity="+ result['images'][i]['id'] + " class='input1' type='checkbox' aria-label='...'></span><span style='width:32%' class='input-group-addon' id='basic-addon1'>"+result['images'][i]['name']+"</span><input type='text' class='form-control input3' placeholder='Enter Number' aria-describedby='basic-addon1'></div></div></div>")

             }




             },

             complete: function (data,n) {
             lu()
             },

             error: function(result){

             }
     });
}



function lu() {
//alert(aa.name)
$('#spawn #in .input3').prop('disabled', true);
$('#spawn #in .input1').click(function(e){
        if (($(this).is(':checked'))){
             $(this).parent().next().next().prop('disabled', false);
        }
        else{
        $(this).parent().next().next().prop('disabled', true);
        }
})

$('#spawn-button').click(function(e){
  var aab=[]

  $("#spawn #in .input1").each(function(){
        if (($(this).is(':checked'))){
             aab.push({name:$(this).parent().next().text(),value:$(this).parent().next().next().val(),id:$(this).attr('identity')})
        }
  }).complete(fu(aab));
//alert(aab.toSource())
});
} //lu ends


function fu(aab) {
$(".spawn-img").show();
var a=JSON.stringify(aab)
$.ajax({
             url: 'spawn/',
             type: 'POST',
             data: {a},
             headers: {
            "D_NAME":aa.name,
             },

             success: function(result){
             $(".spawn-img").hide();

             },
             error: function(result){
 alert("e")
             }
     });
}

//------------------------------------------------ 3rd Tab  -------------------------------
function connect(n) {
    $.ajax({
             url: 'connect/',
             type: 'POST',
             data: {datacentername:aa.name},
             success: function(result){

             $('#connect #in').empty()
             for (var i = 0; i < result.length; i++) {

            // alert(result['images'][i]['name'])
             $('#connect #in').append("<div class='row a'><div class='col-lg-6'><div class='input-group'><span class='input-group-addon'><input class='input1' type='checkbox' aria-label='...'></span><span style='width:32%' class='input-group-addon' id='basic-addon1'>"+result[i]['fields']['name']+"</span><input type='text' class='form-control input3' placeholder='IP' aria-describedby='basic-addon1'></div></div></div>")

             }

             //alert(result.toSource())



             },

             complete: function () {
             connect1()
             },

             error: function(result){

             }
     });
}


function connect1() {
//alert(aa.name)
$('#connect #in .input3').prop('disabled', true);
$('#connect #in .input1').click(function(e){
        if (($(this).is(':checked'))){
             $(this).parent().next().next().prop('disabled', false);
        }
        else{
        $(this).parent().next().next().prop('disabled', true);
        }
})

$('#connect-button').click(function(e){
  var aab2=[]
  $("#connect #in .input1").each(function(){
        if (($(this).is(':checked'))){
             aab2.push({name:$(this).parent().next().text(),ip:$(this).parent().next().next().val()})
        }

  }).complete(connect2(aab2));

});
} //connect ends


function connect2(aab2) {
var a=JSON.stringify(aab2)
$.ajax({
             url: 'connect2/',
             type: 'POST',
             data: {a},
             headers: {
            "D_NAME":aa.name,
             },
             success: function(result){
             },
             error: function(result){

             }
     });
}
//----------------------------------------------CLICK----------------------------------------
$('.vms').click(function(e){
 vms(aa.name)
});

//-----------------------------------------------------------------------------------
} // Intialize End
google.maps.event.addDomListener(window, 'load', initialize);