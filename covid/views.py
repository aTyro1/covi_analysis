from tokenize import Pointfloat
from turtle import color
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
import pandas as pd
from plotly.offline import plot
import plotly.graph_objects as go
import plotly.graph_objects as go
import plotly.io as pio
import numpy as np
plotly_template = pio.templates["plotly_white"]
plotly_template['layout']['plot_bgcolor']='#FFF7ED'
pio.templates.default=plotly_template
covid_world=pd.read_csv("static/csv/time-series-19-covid-combined_csv.csv")
flags=pd.read_csv("static/csv/flags_iso.csv")
def homepage(request):
    template=loader.get_template("covid/home.html")
    countries=set(covid_world['Country/Region'])
    total_cases=0
    for count in countries:
        total_cases+=covid_world[covid_world['Country/Region']==count]['Confirmed'].iloc[-1]
    total_death=0
    for count in countries:
        total_death+=covid_world[covid_world['Country/Region']==count]['Deaths'].iloc[-1]
    total_recovered=total_cases-total_death
    vaccination=pd.read_csv('static/csv/country_vaccinations.csv')
    vaccinated_countries=list(set(vaccination['country']))
    b=0
    for i in vaccinated_countries:
        a=vaccination[vaccination['country']==i]
        if(np.isnan(a.iloc[-1]['total_vaccinations'])==False):
            b+=a.iloc[-1]['total_vaccinations']
    pv=0
    for i in vaccinated_countries:
        a=vaccination[vaccination['country']==i]
        if(np.isnan(a.iloc[-1]['people_vaccinated'])==False):
            pv+=a.iloc[-1]['people_vaccinated']
    pfv=0
    for i in vaccinated_countries:
        a=vaccination[vaccination['country']==i]
        if(np.isnan(a.iloc[-1]['people_fully_vaccinated'])==False):
            pfv+=a.iloc[-1]['people_fully_vaccinated']
    total_dates=list(set(covid_world['Date']))
    x=covid_world.groupby(['Date']).sum()
    y=list(x['Confirmed'])
    i=1
    covid_per_date=[]
    covid_per_date.append(y[0])
    for i in range(1,len(y)):
        j=i-1
        covid_per_date.append(y[i]-y[j])
    world_df=pd.DataFrame(list(zip(total_dates,covid_per_date)),columns=['Dates','No of cases'])
    graphs=[]
    graphs.append(go.Bar(x=world_df['Dates'],y=world_df['No of cases'],name='no of cases in world since 2020-12-21',marker=dict(
        color='#0D9488'
    )))
    layout={
        'title':'no of cases in world since 2020-12-21',
        'xaxis_title':'dates',
        'yaxis_title':'total cases',
        'height':520,
        'width':1260,
        'paper_bgcolor':'#FFF7ED',
        'title_x':0.5,
        'title_font_family':"Ramaraja-Regular",
        'font_family':'Ramaraja-Regular',
        'font_color':'#115E59'
    }
    plot_div=plot({'data':graphs,'layout':layout},
    output_type='div'
    )
    context= {
        'countries_list' :countries ,
        'plot_div':plot_div,
        'total_cases':total_cases,
        'total_recovered':total_recovered,
        'total_deaths':total_death,
        'total_vaccinations':b,
        'total_full_vaccinations':pfv,
        'total_half_vaccinations':pv
    }

    return HttpResponse(template.render(context,request))

