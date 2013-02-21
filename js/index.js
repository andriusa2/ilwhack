$(document).ready(
	function() { 
	$('body').hide();
	$('body').fadeIn();	
	}
);

$.fn.tagcloud.defaults = {
	size: {start: 22, end: 40, unit: 'pt'},
	color: {start: '#cde', end: '#f52'}
};
function selectTag(id){
	$("#selection").slideUp(500);
	resultDict = new Array();
	if (id == 0)
	$.getJSON('src/getData.php?get=items',function(data){
	});
	$.getJSON('src/getData.php?get=items&tag_id='+id.toString(), function(data){
		for (var i = 0; i< data.length; i++){
			var coords = data[i].location.split(',').map(parseFloat);
			resultDict.push({
				latLng: coords,
			});
		}
	});
	$("#mapview").delay(600).slideDown(500, function() {
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
		$("#map_canvas").gmap3(function(){trigger:"resize"});
	});
}
function getTags(){
	$("#tagcloud").replaceWith = "";
	$.getJSON('src/getData.php?get=tags', function(data){
		for(var i =0; i < 20; i++){
			$("#tagcloud").append("<a href=\"#\" onclick=\"selectTag("+data[i].id+")\" rel=\""+(Math.ceil((Math.random()+0.001)*8)).toString()+"\">"+data[i]['tag']+"&nbsp;</a>\n");
		}
		$('#tagcloud a').tagcloud();
		
	});
}
window.onload = getTags();

$("#retry").click(
	function(){
		getTags();
		$("#mapview").slideUp(500);
		$("#selection").delay(600).slideDown(500);
		$("#map_canvas").gmap3({
			clear:{},
		});
	}
);

$("#tryagain").click(
	function(){
		$("#empty").slideUp(500);
		$("#selection").delay(600).slideDown(500);
	}
);
