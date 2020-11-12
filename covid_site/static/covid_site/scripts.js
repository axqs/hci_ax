function drawMap(id,data,options) {
    var worldwide = google.visualization.arrayToDataTable(data);
    var worldwide_options = options;
    var world_map = new google.visualization.GeoChart(document.getElementById(id));
    world_map.draw(worldwide, worldwide_options);
}

function drawLine(id,data,options){
    var linegraph = google.visualization.arrayToDataTable(data);
    var graph_options = options;
    var graph = new google.visualization.LineChart(document.getElementById(id));
    graph.draw(linegraph, graph_options);

}
function drawPie(id,data,options){
    var piegraph = google.visualization.arrayToDataTable(data);
    var graph_options = options;
    var graph = new google.visualization.PieChart(document.getElementById(id));
    graph.draw(piegraph, graph_options);

}
function drawBar(id,data,options){
    var bargraph = google.visualization.arrayToDataTable(data);
    var graph_options = options;
    var graph = new google.visualization.BarChart(document.getElementById(id));
    graph.draw(bargraph, graph_options);

}
function drawArea(id,data,options){
    var areagraph = google.visualization.arrayToDataTable(data);
    var graph_options = options;
    var graph = new google.visualization.AreaChart(document.getElementById(id));
    graph.draw(areagraph, graph_options);

}

function getSize(size){
    var w = 0;
    switch(size) {
        case "threeQuarterSpan":
            w = window.innerWidth*(0.75);
            break;
        case "twoThirdSpan":
            w = window.innerWidth*(0.66);
            break;
        case "halfSpan":
            w = window.innerWidth*(0.5);
            break;
        case "oneThirdSpan":
            w = window.innerWidth*(0.33);
            break;
        case "quarterSpan":
            w = window.innerWidth0*(0.25);
            break;
        default:
            w = window.innerWidth*(1);
            break;
    }
    return w;
}

function drawChart(chart){
    switch(chart["type"]) {
        case "map":
            return drawMap(chart["id"],chart["data"],{backgroundColor: { fill:'transparent' },height:350,width:getSize(chart["size"])});
        case "line":
            return drawLine(chart["id"],chart["data"],{backgroundColor: { fill:'transparent' },height:350,width:getSize(chart["size"])});
        case "bar":
            return drawBar(chart["id"],chart["data"],{backgroundColor: { fill:'transparent' },height:350,width:getSize(chart["size"])});
        case "pie":
            return drawPie(chart["id"],chart["data"],{backgroundColor: { fill:'transparent' },height:350,width:getSize(chart["size"])});
        case "area":
            return drawArea(chart["id"],chart["data"],{backgroundColor: { fill:'transparent' },height:350,width:getSize(chart["size"])});
        default:
            return drawLine("default",chart["data"],{backgroundColor: { fill:'transparent' },height:350,width:getSize(chart["size"])});
    }
}

function changeCountry(country){
    const fs = require('fs');
    console.log(country);
    
    // Write data in 'Output.txt' . 
    fs.writeFile('country.txt', country, (err) => { 
        
        // In case of a error throw err. 
        if (err) throw err; 
    });
    window.location.reload();
}