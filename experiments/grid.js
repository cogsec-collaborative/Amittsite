
var techniques = [
  ['TA01', 'TA02', 'TA03', 'TA04', 'TA05', 'TA06', 'TA07', 'TA08', 'TA09', 'TA10', 'TA11', 'TA12'],
  ['T0001', 'T0005', 'T0007', 'T0010', 'T0016', 'T0019', 'T0029', 'T0039', 'T0047', 'T0057', 'T0058', 'T0062'],
  ['T0002', 'T0006', 'T0008', 'T0011', 'T0017', 'T0020', 'T0030', 'T0040', 'T0048', 'T0061', 'T0059', 'T0063'],
  ['T0003', '', 'T0009', 'T0012', 'T0018', 'T0021', 'T0031', 'T0041', 'T0049', '', 'T0060', 'T0064'],
  ['T0004', '', '', 'T0013', '', 'T0022', 'T0032', 'T0042', 'T0050', '', '', ''],
  ['', '', '', 'T0014', '', 'T0023', 'T0033', 'T0043', 'T0051', '', '', ''],
  ['', '', '', 'T0015', '', 'T0024', 'T0034', 'T0044', 'T0052', '', '', ''],
  ['', '', '', '', '', 'T0025', 'T0035', 'T0045', 'T0053', '', '', ''],
  ['', '', '', '', '', 'T0026', 'T0036', 'T0046', 'T0054', '', '', ''],
  ['', '', '', '', '', 'T0027', 'T0037', '', 'T0055', '', '', ''],
  ['', '', '', '', '', 'T0028', 'T0038', '', 'T0056', '', '', '']
  ];


var grid_div = "#redgrid";
fillGrid(techniques, grid_div);


function fillGrid(techniques, gridname) {

	var numrows = techniques.length;
	var numcols = techniques[0].length;

	function gridData() {
		var data = new Array();
		var xpos = 1; //starting xpos and ypos at 1 so the stroke will show when we make the grid below
		var ypos = 1;
		var boxwidth = 50;
		var boxheight = 50;
		var boxclick = 0;
		
		// iterate for rows	
		for (var row = 0; row < numrows; row++) {
			data.push( new Array() );
			
			// iterate for cells/columns inside rows
			for (var col = 0; col < numcols; col++) {
				data[row].push({
					x: xpos,
					y: ypos,
					width: boxwidth,
					height: boxheight,
					text: techniques[row][col],
					click: boxclick
				})
				// increment the x position. I.e. move it over by 50 (width variable)
				xpos += boxwidth;
			}
			// reset the x position after a row is complete
			xpos = 1;
			// increment the y position for the next row. Move it down 50 (height variable)
			ypos += boxheight;	
		}
		return data;
	}


	var gridData = gridData();	
	// log data to console for quick debugging
	console.log(gridData);

	var grid = d3.select(grid_div)
	//Create the grid
		.append("svg")
		.attr("width",50*numcols+10+"px")
		.attr("height",50*numrows+10+"px");
		
	var row = grid.selectAll(".row")
		.data(gridData)
		.enter().append("g")
		.attr("class", "row");
		
	var column = row.selectAll(".square")
		.data(function(d) { return d; })
		.enter().append("rect")
		.attr("class","square")
		.attr("x", function(d) { return d.x; })
		.attr("y", function(d) { return d.y; })
		.attr("text", function(d) { return d.text; })
		.attr("width", function(d) { return d.width; })
		.attr("height", function(d) { return d.height; })
		.style("fill", "#fff")
		.style("stroke", "#222")
		.on('click', function(d) {
	       d.click ++;
	       if ((d.click)%2 == 0 ) { d3.select(this).style("fill","#fff"); }
		   if ((d.click)%2 == 1 ) { d3.select(this).style("fill","#2C93E8"); }
	    });
}




