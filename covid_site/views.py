from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import json

#chart functions
from graphos.sources.simple import SimpleDataSource
from graphos.renderers.gchart import BarChart
from graphos.renderers.gchart import LineChart
from graphos.renderers.gchart import PieChart

sizeDict = {
    "wholeSpan": {"height" : 400},
    "twoThirdSpan": {"height" : 350},
    "halfSpan": {"height" : 350},
    "quarterSpan": {"height" : 350},
}

# Create your views here.
def populate():
    print("refresh charts")
    charts = []
    charts.append({
        "size" : "wholeSpan",
        "id" : "worldwide",
        "title" : "Zero",
        "type" : "map",
        "data" : [
            ['Country', 'Popularity'],
            ['Germany', 200],
            ['United States', 300],
            ['Brazil', 400],
            ['Canada', 500],
            ['France', 600],
            ['RU', 700],
        ],
    })
    charts.append({
        "size" : "threeQuarterSpan",
        "id" : "chart1",
        "title" : "One",
        "type" : "line",
        "data" : [
            ['Year', 'Sales', 'Expenses'],
            [2004, 1000, 400],
            [2005, 1170, 460],
            [2006, 660, 1120],
            [2007, 1030, 540]
        ],
    })
    charts.append({
        "size" : "twoThirdSpan",
        "id" : "chart2",
        "title" : "Two",
        "type" : "bar",
        "data" : [
            ['Year', 'Sales', 'Expenses'],
            [2004, 1000, 400],
            [2005, 1170, 460],
            [2006, 660, 1120],
            [2007, 1030, 540]
        ],
    })
    charts.append({
        "size" : "halfSpan",
        "id" : "chart3",
        "title" : "Three",
        "type" : "pie",
        "data" : [
            ['Year', 'Sales'],
            ["2004", 1000],
            ["2005", 1170],
            ["2006", 660],
            ["2007", 1030]
        ],
    })
    charts.append({
        "size" : "oneThirdSpan",
        "id" : "chart4",
        "title" : "Four",
        "type" : "area",
        "data" : [
            ['Year', 'Sales', 'Expenses'],
            [2014, 1300, 500],
            [2015, 170, 260],
            [2016, 1660, 120],
            [2017, 2030, 1540]
        ],
    })

    with open("./covid_site/static/covid_site/data.json", 'w') as f:
        json.dump(charts , f)

    return charts

def index(request):
    charts = populate()
    context = {}

    if len(charts) > 0:
        context["charts"] = charts
    
    return render(request, 'covid_site/index.html', context)