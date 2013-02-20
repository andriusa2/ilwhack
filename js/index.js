$(document).ready(
	function() { 
	$('body').hide(),
	$('#mapview').hide(),
	$('#empty').hide(),
	$('body').fadeIn()
	
	}
);

$.fn.tagcloud.defaults = {
	size: {start: 22, end: 40, unit: 'pt'},
	color: {start: '#cde', end: '#f52'}
};

$(function () {
	$('#tagcloud a').tagcloud();
});

$("#map_canvas").gmap3({
	map:{
		options:{
			center: [55.938056, -3.199889],
			zoom: 12
		}
	},
});
