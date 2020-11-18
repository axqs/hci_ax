from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse
from django.template import loader
import pandas as pd
from datetime import date, datetime, timedelta

# Create your views here.
current_country = ''
today = str(date.today())
yesterday = str(date.today() - timedelta(days=1))

def getData():
    d = pd.read_csv('https://covid19.who.int/WHO-COVID-19-global-data.csv', sep=',', skipinitialspace=True)
    d.replace(to_replace=['United States of America', 'Russian Federation', 'The United Kingdom','Iran (Islamic Republic of)','Syrian Arab Republic','Viet Nam','Venezuela (Bolivarian Republic of)','Bolivia (Plurinational State of)','United Republic of Tanzania',],
           value= ['United States', 'Russia', 'United Kingdom','Iran','Syria','Vietnam','Venezuela','Bolivia','Tanzania',], 
           inplace=True)
    if d[d['Date_reported']==today].empty:
        return d[d['Date_reported']==yesterday]
    return d[d['Date_reported']==today]

data = getData()

def getCountries(): 
    return data.Country.unique().tolist()

countries = getCountries()

def getWorldData():
    world_data = data[["Country","Cumulative_deaths"]]

    world_data = world_data.values.tolist()
    world_data.insert(0,["Country","Total Deaths"])

    
    return world_data

def getCountryData():
    with open("./covid_site/static/covid_site/country.txt","r") as f:
        current_country = f.readlines()[0]
        
    cData = data[data['Country']==current_country]
    return {"cases":cData.iloc[0]['New_cases'],
            "deaths":cData.iloc[0]['New_deaths']}

def populate():
    charts = []
    charts.append({
        "size" : "wholeSpan",
        "id" : "worldwide",
        "title" : "Zero",
        "type" : "map",
        "data" : getWorldData(),
    })
    charts.append({
        "size" : "wholeSpan",
        "id" : "chart1",
        "title" : current_country+" Closed Cases",
        "type" : "line",
        "data" : [
            ['Month', 'Recoveries', 'Deaths'],
            ["Mar", 1090, 520],
            ["Apr", 700, 400],
            ["May", 1170, 460],
            ["Jun", 660, 1120],
            ["Jul", 1030, 540],
            ["Aug", 1000, 400],
            ["Sep", 1170, 460],
            ["Oct", 660, 1120],
            ["Nov", 1030, 540],
        ],
    })
    charts.append({
        "size" : "halfSpan",
        "id" : "chart3",
        "title" : "Total Deaths per Age Range",
        "type" : "pie",
        "data" : [
            ['Age Range', 'Deaths'],
            ["0-18", 1000],
            ["19-30", 100],
            ["31-45", 1170],
            ["46-65", 660],
            ["66+", 1030]
        ],
    })
    return charts

def index(request):
    if request.method == 'POST':
        current_country = request.POST.get('country')
        with open("./covid_site/static/covid_site/country.txt","w") as f:
            f.write(current_country)
    else:
        with open("./covid_site/static/covid_site/country.txt","r") as f:
            current_country = f.readlines()[0]

    charts = populate()
    context = {}
    context["countries"] = sorted(countries)
    context["date"] = datetime.now().strftime("%d %B, %Y")
    context["current"] = current_country
    context["country_data"] = getCountryData()
    
    if len(charts) > 0:
        context["charts"] = charts
        
    return render(request, 'covid_site/index.html', context)