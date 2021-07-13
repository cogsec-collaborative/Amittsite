
function fillGrid(params) {

	var grid_div = params[0]; 
	var topcolor = params[1];
	var techniques = params[2]; 

	// grab dataset
	console.log(grid_div);
	console.log(topcolor);
	console.log(techniques);
	console.log("those were the inputs")

	var numrows = techniques.length;
	var numcols = techniques[0].length;

	var data = new Array();
	var xpos = 1; //starting xpos and ypos at 1 so grid edges are visible
	var ypos = 1;
	var boxwidth = 75;
	var boxheight = 25;
	var boxclick = 0;
	
	// set position, width/height/text/number of clicks per box
	for (var row = 0; row < numrows; row++) {
		for (var col = 0; col < numcols; col++) {
			var text = techniques[row][col];
			var color = (row == 0) ? topcolor : '#D0D3D4';
      if (text != '') {
				data.push({
					x: xpos,
					y: ypos,
					width: boxwidth,
					height: boxheight,
					text: text,
					startcolor: color,
					click: boxclick
				})
		  }
			xpos += boxwidth;
		}
		xpos = 1;
		ypos += boxheight;	
	}


	// grab dataset
	console.log(data);

	//Create the grid
	var grid = d3.select(grid_div)
		.append("svg")
		.attr("width",boxwidth*numcols+10+"px")
		.attr("height",boxheight*numrows+10+"px");
	
	// Fill the grid
	var box = grid.selectAll("g")
		.data(data)
		.enter().append("g")
		.attr("class", "row");
		
	box.append("rect")
		.attr("class","square")
		.attr("x", function(d) { return d.x; })
		.attr("y", function(d) { return d.y; })
		.attr("text", function(d) { return d.text; })
		.attr("width", function(d) { return d.width; })
		.attr("height", function(d) { return d.height; })
		.style("fill", function(d) { return d.startcolor; })
		.style("stroke", "#222")
		.style("font-size", "10px")
		.on('click', function(d) {
	       d.click ++;
	       if ((d.click)%2 == 0 ) { d3.select(this).style("fill",function(d) { return d.startcolor;}); }
		   if ((d.click)%2 == 1 ) { d3.select(this).style("fill","#50C878"); }
	  });

	box.append("text")
		.attr("x", function(d) { return d.x + 3; })
		.attr("y", function(d) { return d.y + boxheight/2; })
		.attr("dy", ".35em")
		.text(function(d) { return d.text; });

}




