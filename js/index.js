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
function goodChoice(id){
	gz = [
	"good choice!",
	"awesome choice!",
	"cool!",
	"well done!",
	"like a boss!",
	];
	$.getJSON('src/getData.php?get=tags&id='+id.toString(),function(data){
		tag = " ";
		tag = data['tag'];
		str = tag[0].toUpperCase() + tag.slice(1) + ", " + gz[Math.floor(Math.random()*gz.length)];
		$("#choice").empty().append(str);
	});
}
function selectTag(id){
	goodChoice(id);
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
		resultDict.push({
			latLng: [55.945163, -3.282852],
			options: {
				visible:true,
			}
		});
		resultDict.push({
			latLng: [55.952468, -3.146038],
			options: {
				visible:true,
			}
		});
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
		$("#map_canvas").gmap3({
			autofit:{},
		});
	});
}
function getTags(){
	$("#tagcloud").empty().hide();
	$.getJSON('src/getData.php?get=tags', function(data){
		for(var i =0; i < 20; i++){
			$("#tagcloud").append("<a href=\"#\" onclick=\"selectTag("+data[i].id+")\" rel=\""+(Math.ceil((Math.random()+0.001)*8)).toString()+"\">"+data[i]['tag']+"&nbsp;</a>\n");
		}
		$('#tagcloud a').tagcloud();
		$('#tagcloud').fadeIn(500);
	});
}
getTags();

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

$('#searchform').submit(function() {
	searchq = $("input:first").val()
  	$.getJSON('src/getData.php?get=tag&item='+searchq.toString(),function(data){
  		if (data.length = 0){
  			$("#selection").slideUp(500);
  			$("#empty").delay(600).slideDown(500);
  		} else {
  			selectTag(data[Math.floor(Math.random()*data.length)]);
  		}
	});
});











