$(document).ready(
	function() { 
	$('body').hide(),
	$('body').fadeIn()	
	}
);

$.fn.tagcloud.defaults = {
	size: {start: 22, end: 40, unit: 'pt'},
	color: {start: '#cde', end: '#f52'}
};

$("#map_canvas").gmap3({
	map:{
		options:{
			center: [55.938056, -3.199889],
			zoom: 12
		}
	}
});

$("#tagcloud a").click(
	function() 
	{
		$("#selection").slideUp(500),
		$("#mapview").delay(600).slideDown
		(500,function()
		{
			$("#map_canvas").gmap3({trigger:"resize"}),
			$("#map_canvas").gmap3
			({
				map:{
					options:{
						center: [55.938056, -3.199889],
						zoom: 12
					}
				}
			})
					
		})
	}
);

$("#retry").click(
	function(){
		$("#mapview").slideUp(500),
		$("#selection").delay(600).slideDown(500)
	}
);

$("#tryagain").click(
	function(){
		$("#empty").slideUp(500),
		$("#selection").delay(600).slideDown(500)
	}
);
