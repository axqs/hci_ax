from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse
from django.template import loader
import pandas as pd
from datetime import date, datetime, timedelta

# Create your views here.
current_country = ''
compare = ["","",""]
months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

yesterday = str(date.today() - timedelta(days=1))

def getRawData():
    d = pd.read_csv('https://covid19.who.int/WHO-COVID-19-global-data.csv', sep=',', skipinitialspace=True)
    d.replace(to_replace=['United States of America', 'Russian Federation', 'The United Kingdom','Iran (Islamic Republic of)','Syrian Arab Republic','Viet Nam','Venezuela (Bolivarian Republic of)','Bolivia (Plurinational State of)','United Republic of Tanzania',],
           value= ['United States', 'Russia', 'United Kingdom','Iran','Syria','Vietnam','Venezuela','Bolivia','Tanzania',], 
           inplace=True)
    return d

def getData():
    d = getRawData()
    return d[d['Date_reported']==yesterday]


raw_data = getRawData()
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

def getCompareData():
    

    with open("./covid_site/static/covid_site/compare1.txt","r") as f:
        compare[0] = f.readlines()[0]
    with open("./covid_site/static/covid_site/compare2.txt","r") as f:
        compare[1] = f.readlines()[0]
    with open("./covid_site/static/covid_site/compare3.txt","r") as f:
        compare[2] = f.readlines()[0]

    cData1 = raw_data[raw_data['Country']==compare[0]]
    cData2 = raw_data[raw_data['Country']==compare[1]]
    cData3 = raw_data[raw_data['Country']==compare[2]]

    cData1 = cData1[["Date_reported","Country","New_cases","Cumulative_cases"]]
    cData2 = cData2[["Date_reported","Country","New_cases","Cumulative_cases"]]
    cData3 = cData3[["Date_reported","Country","New_cases","Cumulative_cases"]]

    return [cData1,cData2,cData3]

def populateCharts():
    charts = []
    with open("./covid_site/static/covid_site/country.txt","r") as f:
        current_country = f.readlines()[0]
    compareData = raw_data[raw_data['Country']==current_country]
    cases = compareData[compareData.Date_reported.str.contains('01$')]

    cases = list(cases.index.values)
    cases = [c-1 for c in cases]
    cases = [raw_data.iloc[month][["Cumulative_cases"]].item() for month in cases]
    cases.append(compareData.tail(1)["Cumulative_cases"].item())

    deaths = compareData[compareData.Date_reported.str.contains('01$')]

    deaths = list(deaths.index.values)
    deaths = [c-1 for c in deaths]
    deaths = [raw_data.iloc[month][["Cumulative_deaths"]].item() for month in deaths]
    deaths.append((compareData.tail(1)["Cumulative_deaths"].item()))

    timeseries = [['Month', 'Cases', 'Deaths']]
    for i in range(int(datetime.now().strftime("%m"))):
        timeseries.append(["End of "+months[i],cases[i],deaths[i]])

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
        "title" : " Cumulative Cases and Deaths over Time",
        "type" : "line",
        "data" : timeseries,
    })
    charts.append({
        "size" : "halfSpan",
        "id" : "chart3",
        "title" : "Ratio of Cumulative Cases to Worldwide Cumulative Cases",
        "type" : "pie",
        "data" : [
            ['Title', 'Number'],
            [current_country, compareData.tail(1)["Cumulative_cases"].item()],
            ["World", raw_data['New_cases'].sum()-compareData.tail(1)["Cumulative_cases"].item()],

        ],
    })
    return charts

def populateComparisons():
    comparisons = []
    compareData = getCompareData()
    new_cases = []
    for c in compareData:
        new_cases.append(c.tail(1)["New_cases"].item())

    monthData = []

    for c in compareData:
        m = c[c.Date_reported.str.contains('01$')]
        m = list(m.index.values)
        m = [m-1 for m in m]
        m = [raw_data.iloc[month][["Cumulative_cases"]].item() for month in m]
        monthData.append(m)
    
    cumulative_cases = []

    for i in range(int(datetime.now().strftime("%m"))-1):
        cumulative_cases.append([months[i],monthData[0][i],monthData[1][i],monthData[2][i]])
    cumulative_cases.insert(0,["Month",compare[0],compare[1],compare[2]])

    thisMonthData = [months[int(datetime.now().strftime("%m"))-1]]
    for c in compareData:
        thisMonthData.append(c.tail(1)["Cumulative_cases"].item())
    cumulative_cases.append(thisMonthData)
    
    comparisons.append({
        "size" : "halfSpan",
        "id" : "chart4",
        "title" : " Cumulative Cases as of "+(date.today() - timedelta(days=1)).strftime("%d %B, %Y"),
        "type" : "area",
        "data" : cumulative_cases,
    })
    comparisons.append({
        "size" : "halfSpan",
        "id" : "chart5",
        "title" : " New Cases as of "+ (date.today() - timedelta(days=1)).strftime("%d %B, %Y"),
        "type" : "bar",
        "data" : [
            ['Country', 'New Cases'],
            [compare[0], new_cases[0]],           
            [compare[1], new_cases[1]],            
            [compare[2], new_cases[2]],
        ],
    })
    return comparisons

def index(request):
    if request.method == 'POST':
        current_country = request.POST.get('country')
        compare[0] = request.POST.get('country1')
        compare[1] = request.POST.get('country2')
        compare[2] = request.POST.get('country3')

        if current_country != None:
            with open("./covid_site/static/covid_site/country.txt","w") as f:
                f.write(current_country)
        else:
            with open("./covid_site/static/covid_site/country.txt","r") as f:
                current_country = f.readlines()[0]

        if compare[0] != None:
            with open("./covid_site/static/covid_site/compare1.txt","w") as f:
                f.write(compare[0])
        else:
            with open("./covid_site/static/covid_site/compare1.txt","r") as f:
                compare[0] = f.readlines()[0]

        if compare[1] != None:
            with open("./covid_site/static/covid_site/compare2.txt","w") as f:
                f.write(compare[1])
        else:
            with open("./covid_site/static/covid_site/compare2.txt","r") as f:
                compare[1] = f.readlines()[0]

        if compare[2] != None:
            with open("./covid_site/static/covid_site/compare3.txt","w") as f:
                f.write(compare[2])
        else:
            with open("./covid_site/static/covid_site/compare3.txt","r") as f:
                compare[2] = f.readlines()[0]
    else:
        with open("./covid_site/static/covid_site/country.txt","r") as f:
            current_country = f.readlines()[0]
        with open("./covid_site/static/covid_site/compare1.txt","r") as f:
            compare[0] = f.readlines()[0]
        with open("./covid_site/static/covid_site/compare2.txt","r") as f:
            compare[1] = f.readlines()[0]
        with open("./covid_site/static/covid_site/compare3.txt","r") as f:
            compare[2] = f.readlines()[0]

    charts = populateCharts()
    comparisons = populateComparisons()
    context = {}
    context["countries"] = sorted(countries)
    context["date"] = (date.today() - timedelta(days=1)).strftime("%d %B, %Y")
    context["current"] = current_country
    context["country_data"] = getCountryData()
    context["charts"] = charts
    context["comparisons"] = comparisons
    context["compareCountries"] = compare
        
    return render(request, 'covid_site/index.html', context)