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
    var marginSize = 0.021;
    switch(size) {
        case "threeQuarterSpan":
            w = window.innerWidth*(0.75 - marginSize);
            break;
        case "twoThirdSpan":
            w = window.innerWidth*(0.66 - marginSize);
            break;
        case "halfSpan":
            w = window.innerWidth*(0.5 - marginSize);
            break;
        case "oneThirdSpan":
            w = window.innerWidth*(0.33 - marginSize);
            break;
        case "quarterSpan":
            w = window.innerWidth0*(0.25 - marginSize);
            break;
        default:
            w = window.innerWidth*(1 - marginSize);
            break;
    }
    return w - 17;
}

function drawChart(chart){
    switch(chart["type"]) {
        case "map":
            return drawMap(chart["id"],chart["data"],{backgroundColor: { fill:'transparent' },title:chart["title"],height:300,width:getSize(chart["size"])});
        case "line":
            return drawLine(chart["id"],chart["data"],{backgroundColor: { fill:'transparent' },title:chart["title"],height:300,width:getSize(chart["size"])});
        case "bar":
            return drawBar(chart["id"],chart["data"],{backgroundColor: { fill:'transparent' },title:chart["title"],height:300,width:getSize(chart["size"])});
        case "pie":
            return drawPie(chart["id"],chart["data"],{backgroundColor: { fill:'transparent' },title:chart["title"],height:300,width:getSize(chart["size"])});
        case "area":
            return drawArea(chart["id"],chart["data"],{backgroundColor: { fill:'transparent' },title:chart["title"],height:300,width:getSize(chart["size"])});
        default:
            return drawLine("default",chart["data"],{backgroundColor: { fill:'transparent' },title:chart["title"],height:300,width:getSize(chart["size"])});
    }
}