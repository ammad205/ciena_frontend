
//alert("alert works")

$(function(){

 $( "#firefly-drop" ).click(function(){

alert("working");

var xhr = new XMLHttpRequest();
xhr.open("GET", "http://www.codecademy.com/", false);
xhr.send();

alert(xhr);
alert(xhr.status);
alert(xhr.statusText);

console.log(xhr.status);
console.log(xhr.statusText);

});
});