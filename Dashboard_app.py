from dash import Dash, html, dash_table , dcc , Input, Output
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from plotly import graph_objects as go
import json

df = pd.read_csv('20_Victims_of_rape.csv')
df = df[df['Subgroup'] != 'Total Rape Victims']
df['Unreported_Cases'] = df['Victims_of_Rape_Total'] - df['Rape_Cases_Reported']
df['total_cases'] = df.groupby(['Area_Name','Year'])['Victims_of_Rape_Total'].transform('sum')




df1=df.groupby(['Area_Name'])[['Victims_of_Rape_Total']].sum().reset_index()
print(df1)


india_states = json.load(open("f:\Abhijit\Documents\SUBBU\choropleth-python-tutorial-cf325ac8f42602746c1b8c399178c3b445649df4\choropleth-python-tutorial-cf325ac8f42602746c1b8c399178c3b445649df4\states_india.geojson", "r"))

print(india_states['features'][0]['properties'].keys())

fig_map = px.choropleth(
    df1,
    locations="Area_Name",
    geojson=india_states,
    featureidkey= 'properties.st_nm',
    color="Victims_of_Rape_Total",
    hover_name="Area_Name",

)
fig_map.update_geos(fitbounds="locations", visible=False)




fig1 = px.line(df,x='Year',y='total_cases',color='Area_Name')
#this will create a select/deselect option for area_name in the graph
fig1.update_layout(dict(updatemenus=[
                        dict(
                            type = "buttons",
                            direction = "left",
                            buttons=list([
                                dict(
                                    args=["visible", "legendonly"],
                                    label="Deselect All",
                                    method="restyle"
                                ),
                                dict(
                                    args=["visible", True],
                                    label="Select All",
                                    method="restyle"
                                )
                            ]),
                            pad={"r": 10, "t": 10},
                            showactive=False,
                            x=1,
                            xanchor="right",
                            y=1.1,
                            yanchor="top"
                        ),
                    ]
                    # width = 600,
                    # height =400
              ))


fig2 = px.histogram(df,x='Area_Name', y = 'Unreported_Cases' )
fig2.update_layout(
    xaxis_title = "Area Name",
    yaxis_title = "Total Number of Unreported Rape Victims from \n( 2001 to 2010)",
    title = {
             "font":{
                 "family": "Arial",
                 "size": 20,
                 "color": "black"
                 },
                 "x":0.5 #center align
             },
            
    height = 700,
    autosize = True,
)

#heatmap
df=df.groupby(['Area_Name'])[['Victims_Upto_10_Yrs','Victims_Between_10-14_Yrs','Victims_Between_14-18_Yrs','Victims_Between_18-30_Yrs','Victims_Between_30-50_Yrs','Victims_Above_50_Yrs']].sum().reset_index()
df = pd.melt(df,id_vars=['Area_Name'],value_vars=['Area_Name','Victims_Upto_10_Yrs','Victims_Between_10-14_Yrs','Victims_Between_14-18_Yrs','Victims_Between_18-30_Yrs','Victims_Between_30-50_Yrs','Victims_Above_50_Yrs'],
             var_name='Age')
print(df)
df = df.pivot(index='Age',columns='Area_Name',values='value')
fig3 = px.imshow(df,color_continuous_scale=px.colors.sequential.amp)

fig3.update_traces(hoverongaps=False,
                  hovertemplate = "Age : %{y}"
                                  "<br>Area_Name : %{x}"
                                  "<br>Cases : %{z} <extra></extra>"
                  )
fig3.update_layout(
    height=500
)

app = Dash()
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container([

#intro text
    dbc.Row([
        dbc.Col([
            dcc.Markdown('# Rape Cases in India', style={'textAlign':'center'})
        ],width=12)
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Markdown(
                '''  _The issue of rape and sexual violence is a grave concern that transcends cultural, geographical, and societal boundaries. In India, the discourse around rape has grown increasingly prominent over the past few decades, urging society and policymakers to address the epidemic of sexual violence against women. This report delves into the statistical analysis of reported rape cases in India from 2001 to 2010—a critical decade that witnessed both heightened awareness and legislative changes aimed at combating sexual violence._

 '''
            )
        ])
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Markdown('###### Key Objectives', style={'textAlign':'left'})
        ],width=12)
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Markdown(''' * Provide a state-wise comparison of reported rape cases.
* Analyze trends over the years to identify any significant patterns or anomalies.
* Provide insights into the demographic impacts, including age variations.
''')
        ])
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Markdown('###### Overview', style={'textAlign':'left'})
        ],width=12)
    ]),  

    dbc.Row([
        dbc.Col([
            dcc.Markdown('''
* Total Incidents                 
* Yearly Trends & State Comparison
* Demographic Insights
                         ''')
        ],width=12)
    ]),  

    dbc.Row([
        dbc.Col([
            dcc.Markdown('''

_The **chloropeth map** below shows the state wise total cases throughout the decade                      **|**                            The **line graph** below shows the state wise comparison of total cases in each each year_ 

''',style={'textAlign':'center'})
        ])
    ]),

# line graph of total rape cases  
    dbc.Row([
        dbc.Col(dcc.Graph(id ='map',figure = fig_map),width=5),
        dbc.Col(dcc.Graph(id = 'graph1',figure=fig1),width=7)

        ]),

    dbc.Row([
        dbc.Col([
            dcc.Markdown('''

_Our dataset provides us with the **Demographic Insights** of the data , which can be best visualised through the heatmap below_ 

''',style={'textAlign':'center'})
        ])
    ]),
#heatmap
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id = "graph3",
                figure=fig3
            )
        ])
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Markdown('''

_Out of the amount of cases we've analysed statistically, there's a significant amount of cases that are still unreported. In India, it's estimated that a staggering **99%** of sexual assault cases go unreported.The silence surrounding these cases not only hinders justice but also perpetuates a cycle of violence and impunity_ 

''',style={'textAlign':'left'})
        ])
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Markdown('''

_The **Histogram** below shows the state wise Unreported Cases throughout the decade_ 

''',style={'textAlign':'center'})
        ])
    ]),

# statewise unreported rape victins graph
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id = 'graph2',
                figure = fig2
            )
        ])
    ]),


],fluid=True)


if __name__ == '__main__':
    app.run(debug=True)

