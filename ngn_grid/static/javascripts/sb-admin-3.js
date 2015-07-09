

$( document ).ready(function() {


//myFunction()



$( "#mytest" ).click(function() {
			$.ajax({
					url : "dashboard",
					data : {},
					type : "GET",
					success : function(res) {
					    // alert(JSON.stringify(res))
						$("#page-wrapper").html(res).hide().fadeIn(300);
					},
					error : function(res) {
						alert(JSON.stringify(res));
					}
				});
}); // analytics END

$( "#a2" ).click(function() {
			$.ajax({
					url : "../../analytics/test2",
					data : {},
					type : "GET",
					success : function(res) {
					//	alert(JSON.stringify(res))
						$("#page-wrapper").html(res).hide().fadeIn(300);
						//myFunction()
					},
					error : function(res) {
						alert(res);
					}
				});
}); // analytics2 END
				





$( "#nfvj" ).click(function() {
alert("hello")
			/*$.ajax({
					url : "../../analytics/vmpage21",
					data : {},
					type : "GET",
					success : function(res) {
					   //var obj = JSON.parse(res);
					    // alert(toJSON(res))
					     //alert(res)
						$("#page-wrapper").html(res).hide().fadeIn(100);
						//alert("success")
					},
					error : function(res) {
						//alert(JSON.stringify(res));
						//alert(res)
						alert("error")
					}
				});*/
}); // analytics END























}); // document.ready END






















