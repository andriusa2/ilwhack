//Iniatial animation
$(document).ready(
	function() { 
	$('body').hide();
	$('body').fadeIn();	
	getTags();
	}
);
//Tagcloud sizes and colours
$.fn.tagcloud.defaults = {
	size: {start: 22, end: 40, unit: 'pt'},
	color: {start: '#cde', end: '#f52'}
};
//Function for getting iteam objects from s single tag
function getItems(id){
	if (id == 0) {$.getJSON('src/getData.php?get=items',function(data){});}
	else{
		resultDict = new Array();
		for (var i = 0; i< data.length; i++){
			var coords = data[i].location.split(',').map(parseFloat);
			resultDict.push({
				latLng: coords,
				data:{
					id: data[i].id,
					name: data[i].name,
				},
			});
		}
	}
	return resultDict;
}

//Function for adding empty markers to edinburgh
function addDefaultMarkers(resultDict){
	resultDict.push({
		latLng: [55.945163, -3.282852],
		options: {
			visible:false,
		}
	});
	resultDict.push({
		latLng: [55.952468, -3.146038],
		options: {
			visible:false,
		}
	});
	return resultDict;
}

//Function to draw a map
function drawMap(resultDict){
	resultDict=addDefaultMarkers(resultDict);
	$("#map_canvas").gmap3({
		map:{
			options:{
				center: [55.938056, -3.199889],
				zoom: 12
			}
		},
		marker:{
			values:resultDict,
			events:{
				mouseover: function(marker, even, context){
					var map = $(this).gmap3("get"),
						infowindow = $(this).gmap3({get:{name:"infowindow"}});
					if (infowindow){
						infowindow.open(map,marker);
						infowindow.setContent(context.data['name']+"<br/><b>Click on the marker to see more</b>");
					} else {
						$(this).gmap3({
							infowindow:{
								anchor:marker, 
								options:{content: context.data['name']+"<br/><b>Click on the marker to see more</b>"}
							}
						});
					}
				},
				mouseout: function(){
					var infowindow = $(this).gmap3({get:{name:"infowindow"}});
					if (infowindow){
						infowindow.close();
					}
				},
				click: function(marker, even, context){
				
			
				},
			},
		},
	});
	$("#map_canvas").gmap3({
		autofit:{},
	});
}

//Given an array of tags switches to mapview and displays them
function selectTags(ids){
	resultDict = new Array();
	for (var i = 0; i< ids.length; i++){ 
		resultDict= concat(resultDict, getItems(ids[i]));
	}
	resultDict = resultDict.unique();
	goodchoice(ids);
	$("#selection").slideUp(500);
	$("#mapview").delay(600).slideDown(500, drawMap(resultDict));
}

//Friendly success message
function goodChoice(ids){
	gz = [
	"Good choice!",
	"Awesome choice!",
	"Cool!",
	"Well done!",
	"Like a boss!",
	];
	id=ids[Math.floor(Math.random()*ids.length)]
	$.getJSON('src/getData.php?get=tags&id='+id.toString(),function(data){
		tag = " ";
		tag = data['tag'];
		str = tag[0].toUpperCase() + tag.slice(1)
		if (ids.length>1){str = str + " and others"}
		str = str + ", " + gz[Math.floor(Math.random()*gz.length)];
		$("#choice").empty().append(str);
	});
}

//Sets tags for the tagcloud
function setTags(){
	$("#tagcloud").empty().hide();
	$.getJSON('src/getData.php?get=tags', function(data){
		for(var i =0; i < 20; i++){
			$("#tagcloud").append("<a href=\"#\" onclick=\"selectTags(["+data[i].id+"])\" rel=\""+(Math.ceil((Math.random()+0.001)*8)).toString()+"\">"+data[i]['tag']+"&nbsp;</a>\n");
		}
		$('#tagcloud a').tagcloud();
		$('#tagcloud').fadeIn(500);
	});
}

//Button for new search from map
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

//Button for new search from emty list
$("#tryagain").click(
	function(){
		$("#empty").slideUp(500);
		$("#selection").delay(600).slideDown(500);
	}
);

//Processing for the seach field
$('#searchform').submit(function() {
	searchq = $("input:first").val()
  	$.getJSON('src/getData.php?get=tags&query='+searchq.toString(),function(data){
  		if (data.length = 0){
  			$("#selection").slideUp(500);
  			$("#empty").delay(600).slideDown(500);
  		} else {
  			selectTags(data);
  		}
	});
});











