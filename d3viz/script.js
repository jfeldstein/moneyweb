var svg = d3.select("svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height");

var color = d3.scaleOrdinal(d3.schemeCategory20);

var manyBody = d3.forceManyBody()
    .strength(function(node) {
    	return (node.group+10)*-14;
    })

var svgEle = document.getElementsByTagName('svg')[0].parentNode;
var idToClass = function(id) {
  return id.replace(/[^A-Z]+/ig, '-');
}

var simulation = d3.forceSimulation()
    .force("link", d3.forceLink().id(function(d) { return d.id; }))
    .force("charge", manyBody)
    .force("center", d3.forceCenter(svgEle.offsetWidth / 2 + 100, svgEle.offsetHeight + 200));

var SIMULATE = true;
d3.json("http://localhost:8000/data_examples/floridafinal.json", function(error, graph) {
  if (error) throw error;

  window.graph = graph;

  svg.on('mousedown', clearFocus);

// build the arrow.
svg.append("svg:defs").selectAll("marker")
    .data(["end"])      // Different link/path types can be defined here
  .enter().append("svg:marker")    // This section adds in the arrows
    .attr("id", String)
    .attr("viewBox", "0 -5 10 10")
    .attr("refX", 15)
    .attr("refY", -1.5)
    .attr("markerWidth", 1)
    .attr("markerHeight", 1)
    .attr("orient", "auto")
  .append("svg:path")
    .attr("d", "M0,-5L10,0L0,5");

  var link = svg.append("g")
      .attr("class", "links")
    .selectAll("line")
    .data(graph.links)
    .enter().append("line")
      .attr("stroke-width", function(d) { return Math.max(1, Math.sqrt(d.value) / 100); })
      .attr("marker-end", "url(#end)")
      .attr("class", function(d) {
        return ['line', 'source-'+idToClass(d.source), 'target-'+idToClass(d.target)].join(' ');
      })

  var circles = svg
    .append("g")
      .attr("class", "nodes")
    .selectAll('.nodes');

  var circleGroups = circles
    .data(graph.nodes)
    .enter()
    .append('g')
      .attr('class', function(d) {
        return ['circle', idToClass(d.id)].join(' ');
      });

  circleGroups
      .insert("circle")
        .attr("fill", function(d) { return color(d.group+10); })
        .attr("r", function(d) { return isNaN(d.value) ? 10 : Math.sqrt(d.value); })
        .on('mouseover', showCallout)
        .on('mouseout', hideCallout)
        .on('mousedown', setFocus)
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended));

  circleGroups
      .insert("text")
        .text(function (d) { return d.id; });

  circleGroups
      .insert("title")
        .text(function(d) { return d.id; });

  simulation
      .nodes(graph.nodes)
      .on("tick", ticked);

  simulation.force("link")
      .links(graph.links);

  function ticked() {
    if (!SIMULATE) return;
    link
        .attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    circleGroups
        .attr("transform", function(d) { return "translate("+d.x+", "+d.y+")"; })
        //.attr("y", function(d) { return d.y; });
  }

});


setTimeout(function () {
  SIMULATE = false;
}, 1700);


function dragstarted(d) {
  if (!d3.event.active) simulation.alphaTarget(0.3).restart();
  d.fx = d.x;
  d.fy = d.y;
}

function dragged(d) {
  d.fx = d3.event.x;
  d.fy = d3.event.y;
}

function dragended(d) {
  if (!d3.event.active) simulation.alphaTarget(0);
  d.fx = null;
  d.fy = null;
}
