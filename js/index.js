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
function getTags(){
	$.getJSON('src/getData.php?get=tags', function(data){
		for(var i =0; i < 20; i++){
			$("#tagcloud").append("<a href=\"#\" rel=\""+(Math.ceil((Math.random()+0.001)*8)).toString()+"\">"+data[i]['tag']+"</a>\n");
		}
		$('#tagcloud a').tagcloud();
		
	});
}
function map(id){
}
window.onload(getTags());

$("#map_canvas").gmap3({
	map:{
		options:{
			center: [55.938056, -3.199889],
			zoom: 12
		}
	},
	marker:{
		options:{
			latlng: [55.938050, -3.199880],
		}
	},
	
});
