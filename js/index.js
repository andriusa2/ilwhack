function unique(dict){
	var a =[];
	var l = dict.length;
	for(var i = 0;i < l; i++){
		for(var j = i+1 ; j < l; j++){
			if(dict[i] === dict[j])
				j = ++i;
		}
		a.push(dict[i]);
	}
	return a;
};
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
		var resultDict = new Array();
		$.ajax({
			url: 'src/getData.php?get=items&tag_id='+id.toString(),
			async: false,
			dataType: 'json',
			success:function(data){
				for (var i = 0; i< data.length; i++){
					var coords = data[i].location.split(',').map(parseFloat);
					resultDict.push({
						latLng: coords,
						data:{
							id: data[i].id,
							shortName: data[i].shortName,
						},
					});
				}
			},
		});
		return resultDict;
	}
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
		map:{},
		panel:{
			options:{
				content:
					'<div id="overlay">'+
					'	<div class="exit_button"></div> ' +
					'	<div class="name"></div>' + 
					'	<div class="phone"></div>' +
					'	<div class="website"></div>' +
					'	<div class="address"></div>' +
					'	<div class="email"></div>' +
					'   <div class="origin"></div>' +
					'</div>',
				middle: true,
				center: true,
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
						infowindow.setContent(context.data['shortName']+"<br/><b style=\"font-size:10px;\" >Click on the marker to see more</b>");
					} else {
						$(this).gmap3({
							infowindow:{
								anchor:marker, 
								options:{
									content: context.data['shortName']+"<br/><b style=\"font-size:10px;\">Click on the marker to see more</b>",
									disableAutoPan: true,
								}
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
					showPanel(context.data['id']);
				},
			},
		},
		autofit:{},
	});
	$('#overlay').hide();
	$('#overlay .exit_button').click(function(){
		$('#overlay').fadeOut(function(){
			clearPanel();
		});
	});
}
function clearPanel(){
	$('#overlay .name').empty();
	$('#overlay .phone').empty();
	$('#overlay .website').empty();
	$('#overlay .address').empty();
	$('#overlay .email').empty();
	$('#overlay .origin').empty();
};
function showPanel(id){
	$.ajax({
		url: 'src/getData.php?get=items&id='+id,
		async: false,
		dataType: 'json',
		success:function(data){
			clearPanel();
			if(data["shortName"]) $('#overlay .name').append("<h2>Name: </h2>"+data["shortName"]);
			else { alert("item not found!"); return;};
			if(data["phone"]) $('#overlay .phone').append("<h3>Phone: </h3>" + data["phone"]);
			if(data["address"]) $('#overlay .address').append("<h3>Address: </h3>"+data["address"]);
			if(data["website"]) $('#overlay .website').append("<h3>Website: </h3><a href=\""+data['web']+"\">"+data['web']+"</a>");
			if(data["email"]) $('#overlay .email').append("<h3>E-mail: </h3><a href=\"mailto:"+data['email']+"\">"+data['email']+"</a>");
			if(data["origin"]) $('#overlay .origin').append("Data from: "+data["origin"]);
		},
	});
	$('#overlay').fadeIn();
}
//Given an array of tags switches to mapview and displays them
function selectTags(ids){
	var resultDict = new Array();
	for (var i = 0; i< ids.length; i++){ 
		resultDict.push.apply(resultDict, getItems(ids[i]));
	}
	resultDict = unique(resultDict);
	goodChoice(ids);
	$("#selection").slideUp(500);
	$("#mapview").slideDown(500);
	drawMap(resultDict);
	
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
function getTags(){
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











