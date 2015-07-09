<script>
       /* $(".form-control").click(function(){
		alert("working")
		$.ajax({
			url: 'http://localhost:8000/analytics/uves/virtual-machines',
			success: function(result){
				alert(result)
			}
		})
	}) */
	
	// tells the option which was selected
	function optionSelected(optionName) {
  		if (optionName=="") return
		//alert(optionName)
	}	
	
	window.onload = function() {
		//alert("working")
		$.ajax({
			url: 'http://localhost:8000/analytics/uves/virtual-machines',
			dataType: 'json',
			success: function(result){
				//alert(result)
				processVMList(result)
			}
		})
		
		function processVMList(result){
			select = document.getElementById('51')
			for (var i = 0; i<result.length; i++){
    				//alert(result[i].name)
    				var opt = document.createElement('option')
    				opt.value = result[i].name
    				opt.innerHTML = result[i].name
    				select.appendChild(opt)
			}
		}

		$.ajax({
			url: 'http://localhost:8000/analytics/uves/virtual-networks',
			dataType: 'json',
			success: function(result){
				//alert(result)
				processVNList(result)
			}
		})

		function processVNList(result){
			select = document.getElementById('52')
			for (var i = 0; i<result.length; i++){
    				//alert(result[i].name)
    				var opt = document.createElement('option')
    				opt.value = result[i].name
    				opt.innerHTML = result[i].name
    				select.appendChild(opt)
			}
		}
	};
    </script>

    <script>
	var g1, g2, g3, g4
	var state_G3 = 'B'
	var state_G4 = 'B'
	var vm_name = ''
	$( document ).ready(function() {

        g1 = new JustGage({
          id: "g1",
          value: 0,
          min: 0,
          max: 100,
          title: "CPU Utilization",
          label: "%"
        });

        g2 = new JustGage({
          id: "g2",
         value: 0,
          min: 0,
          max: 100,
          title: "Memory Utilization",
          label: "%"
        });

	g3 = new JustGage({
          id: "g3",
         value: 0,
          min: 0,
          max: 1024,
          title: "Total Inbound Traffic",
          label: "KB/hr"
        });

	g4 = new JustGage({
          id: "g4",
         value: 0,
          min: 0,
          max: 1024,
          title: "Total Outbound Traffic",
          label: "KB/hr"
        });
        setInterval(function() {
	  if (vm_name != '') {
		processVMInfo(vm_name)
	  } else {
	  	g1.refresh(Math.round(Math.random()*100))
	  	g2.refresh(Math.round(Math.random()*100))
	  	g3.refresh(Math.round(Math.random()*1024))
	  	g4.refresh(Math.round(Math.random()*1024))
	  }
        }, 5000);
      });


      $('select').change(function(evt){
	    if (evt.currentTarget.selectedOptions[0].parentElement.label == "Virtual Machines") {
		vm_name = evt.currentTarget.selectedOptions[0].label    
		processVMInfo(vm_name)
	    } else if (evt.currentTarget.selectedOptions[0].parentElement.label == "Virtual Networks") { 
		processVNInfo(evt.currentTarget.selectedOptions[0].label)
	    }
    	});
	
	function processVMInfo(vmName) {
		$.ajax({
			url: 'http://localhost:8000/analytics/getVMStats/' + vmName,
			dataType: 'json',
			success: function(result){
				g1.refresh(Math.round(result.cpu_usage))
				if (result.total_memory > 0) {
					g2.refresh(Math.round((result.used_memory*100)/result.total_memory))
				} else {
					g2.refresh(0)				
				}

				if (result.in_bytes < 1024) {
					if (state_G3 != 'B') {
						state_G3 = 'B'
						g3.config.label = 'B/hr'
					}
					g3.refresh(Math.round(result.in_bytes))
				} else if (result.in_bytes > 1024 && result.in_bytes < 1024*1024) { // KB
					if (state_G3 != 'K') {
						state_G3 = 'K'
						g3.config.label = 'KB/hr'
					}
					g3.refresh(Math.round(result.in_bytes/1024))
				} else if (result.in_bytes > 1024*1024 && result.in_bytes < 1024*1024*1024) { // MB
					if (state_G3 == 'M') {
						state_G3 = 'M'
						g3.config.label = 'MB/hr'
					}
					g3.refresh(Math.round(result.in_bytes/(1024*1024)))
				} else if (result.in_bytes > 1024*1024*1024) { // GB
					if (state_G3 == 'G') {
						state_G3 == 'G'
						g3.config.label = 'GB/hr'
					}
					g3.refresh(Math.round(result.in_bytes/(1024*1024*1024)))
				}

				if (result.out_bytes < 1024) {
					if (state_G4 != 'B') {
						state_G4 = 'B'
						g4.config.label = 'B/hr'
					}
					g4.refresh(Math.round(result.out_bytes))
				} else if (result.out_bytes > 1024 && result.out_bytes < 1024*1024) { // KB
					if (state_G4 != 'K') {
						state_G4 = 'K'
						g4.config.label = 'KB/hr'
					}
					g4.refresh(Math.round(result.out_bytes/1024))
				} else if (result.out_bytes > 1024*1024 && result.out_bytes < 1024*1024*1024) { // MB
					if (state_G4 == 'M') {
						state_G4 = 'M'
						g4.config.label = 'MB/hr'
					}
					g4.refresh(Math.round(result.out_bytes/(1024*1024)))
				} else if (result.out_bytes > 1024*1024*1024) { // GB
					if (state_G4 == 'G') {
						state_G4 == 'G'
						g4.config.label = 'GB/hr'
					}
					g4.refresh(Math.round(result.out_bytes/(1024*1024*1024)))
				}
			}
		})
	}

	function processVNInfo(vnName) {
		//alert("VN Name" + vnName)
	}
    	 
</script>
