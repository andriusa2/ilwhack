function getTags(){
	$.getJSON('src/getData.php?get=tags', function(data){
		for(var i =0; i < 20; i++){
			$("#tagcloud").append("<a href=\"#\" rel=\""+(Math.ceil((Math.random()+0.001)*8)).toString()+"\">"+data[i]['tag']+"</a>\n");
		}
		$('#tagcloud a').tagcloud();
		
	});
}
function map(var id){
	

}
window.onload(getTags());
