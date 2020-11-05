from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

#chart functions
from graphos.sources.simple import SimpleDataSource
from graphos.renderers.gchart import BarChart
from graphos.renderers.gchart import LineChart
from graphos.renderers.gchart import PieChart


# Create your views here.
def populate():
    print("refresh charts")
    charts = []
    charts.append(LineChart(SimpleDataSource(data=[
        ['Year', 'Sales', 'Expenses'],
        [2004, 1000, 400],
        [2005, 1170, 460],
        [2006, 660, 1120],
        [2007, 1030, 540]
        ]
    )))
    charts.append(BarChart(SimpleDataSource(data=[
        ['Year', 'Sales', 'Expenses'],
        [2004, 1000, 400],
        [2005, 1170, 460],
        [2006, 660, 1120],
        [2007, 1030, 540]
        ]
    )))
    charts.append(PieChart(SimpleDataSource(data=[
        ['Year', 'Sales'],
        ["2004", 1000],
        ["2005", 1170],
        ["2006", 660],
        ["2007", 1030]
        ]
    )))

    return charts

def index(request):
    charts = populate()
    context = {}

    if len(charts) > 0:
        context["charts"] = charts
    
    return render(request, 'covid_site/index.html', context)