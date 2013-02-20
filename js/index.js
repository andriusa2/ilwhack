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
			$("#tagcloud").append("<a href=\"#\" rel=\""+(Math.ceil((Math.random()+0.001)*8)).toString()+"\">"+data[i]['tag']+"&nbsp;</a>\n");
		}
		$('#tagcloud a').tagcloud();
		
	});
}
function map(id){
}
window.onload = getTags();

function populateMap(id){
	if (id == 0)
	$.getJSON('src/getData.php?get=items',function(data){
	});
	$.getJSON('src/getData.php?get=items&id='+id.toString, function(data){
		resultDict = new Array();
		for (var i = 0; i< data.length; i++){
			var coords = data[i].location.split(',').map(parseFloat);
			resultDict.push({
				latlng: coords,
			});
		}
	});


	$("#map_canvas").gmap3({
		map:{
			options:{
				center: [55.938056, -3.199889],
				zoom: 12
			}
		},
		marker:{
			values:resultDict,
		},	
	});
}