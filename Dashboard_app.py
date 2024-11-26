from dash import Dash ,dcc,html, Output , Input , State
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import json
import plotly.graph_objects as go


df = pd.read_csv('20_Victims_of_rape.csv')
df = df[df['Subgroup'] != 'Total Rape Victims']
df['Unreported_Cases'] = df['Victims_of_Rape_Total'] - df['Rape_Cases_Reported']
df['total_cases'] = df.groupby(['Area_Name','Year'])['Victims_of_Rape_Total'].transform('sum')

#Line Graph (Annual Trend of Total Rape Cases)
df1=df.groupby(['Year'])[['total_cases']].sum().reset_index()

fig01 = px.line(df1,x='Year',y = 'total_cases')
fig01.update_layout(plot_bgcolor = 'rgba(0,0,0,0)',
                    paper_bgcolor = 'rgba(0,0,0,0)',
                    #line along x axis
                    xaxis = dict(
                        showline = True,
                        linecolor = 'black',
                        linewidth = 2,
                        automargin = True,
                        tickfont=dict(size=9),
                    ),
                    #line along y axis
                    yaxis = dict(
                        showline = True,
                        linecolor = 'black',
                        linewidth = 2, 
                        automargin = True,
                        tickfont=dict(size=9)  
                    ),
                    margin = dict(l=0,r=0,t=10,b=95,pad=5),
                    height = 400,
                    width = 400,
                    )
fig01.update_traces(line_color = "#1f77b4") # graph line color


#chloropeth map
df2=df.groupby(['Area_Name'])[['Victims_of_Rape_Total']].sum().reset_index()

india_states = json.load(open("F:\Abhijit\Documents\SUBBU\choropleth-python-tutorial-cf325ac8f42602746c1b8c399178c3b445649df4\choropleth-python-tutorial-cf325ac8f42602746c1b8c399178c3b445649df4\states_india.geojson", "r"))

fig02 = px.choropleth(
    df2,
    locations="Area_Name",
    geojson=india_states,
    featureidkey= 'properties.st_nm',
    color="Victims_of_Rape_Total",
    labels = {"Victims_of_Rape_Total":""},
    color_continuous_scale="Teal",
    hover_name="Area_Name",
    projection="azimuthal equidistant" #choose from below
)
#  sinusoidal', 'natural earth', 'natural earth1', 'natural
#             earth2', 'nell hammer', 'nicolosi', 'orthographic',
#             'patterson', 'peirce quincuncial', 'polyconic',
#             'rectangular polyconic', 'robinson', 'satellite', 'sinu
#             mollweide', 'sinusoidal', 'stereographic', 'times',
#             'transverse mercator', 'van der grinten', 'van der
#             grinten2', 'van der grinten3', 'van der grinten4',
#             'wagner4', 'wagner6', 'wiechel', 'winkel tripel',
#             sinusoidal', 'natural earth', 'natural earth1', 'natural
#             earth2', 'nell hammer', 'nicolosi', 'orthographic',
#             'patterson', 'peirce quincuncial', 'polyconic',
#             'rectangular polyconic', 'robinson', 'satellite', 'sinu
#             mollweide', 'sinusoidal', 'stereographic', 'times',
#             earth2', 'nell hammer', 'nicolosi', 'orthographic',
#             'patterson', 'peirce quincuncial', 'polyconic',
#             'rectangular polyconic', 'robinson', 'satellite', 'sinu
#             'rectangular polyconic', 'robinson', 'satellite', 'sinu
#             mollweide', 'sinusoidal', 'stereographic', 'times',
#             'transverse mercator', 'van der grinten', 'van der
#             grinten2', 'van der grinten3', 'van der grinten4',
#             'wagner4', 'wagner6', 'wiechel', 'winkel tripel',
#             'winkel3']
fig02.update_geos(fitbounds="locations", visible=False)
fig02.update_layout(
    coloraxis_colorbar = dict(thickness = 9,len = 0.7),
    coloraxis_colorbar_x = 0.01,
    plot_bgcolor = 'rgba(0,0,0,0)',
    paper_bgcolor = 'rgba(0,0,0,0)',
    geo = dict(bgcolor = 'rgba(0,0,0,0)'),
    autosize = True,
    margin = dict(l=20,r=0,t=0,b=6,pad=2),
    height = 375,
    width  = 450
)


#Line Graph showing yearly trend
fig03 = px.line(df,x='Year',y='total_cases',color ='Area_Name',color_discrete_sequence=px.colors.sequential.Teal)
#this will create a select/deselect option for area_name in the graph
fig03.update_layout(dict(updatemenus=[
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
              ),plot_bgcolor = 'rgba(0,0,0,0)',paper_bgcolor = 'rgba(0,0,0,0)',geo = dict(bgcolor = 'rgba(0,0,0,0)'),
                    #line along x axis
                    xaxis = dict(
                        showline = True,
                        linecolor = 'black',
                        linewidth = 2,
                        
                    ),
                    #line along y axis
                    yaxis = dict(
                        showline = True,
                        linecolor = 'black',
                        linewidth = 2,
                       
                    ),margin = dict(l=20,r=0,t=10,b=95,pad=5),height=400)

#Histogram of unreported cases
fig2 = px.histogram(df,x='Area_Name', y = 'Unreported_Cases',color_discrete_sequence=["#1f77b4"] )
fig2.update_layout(
    title = {
             "font":{
                 "family": "Arial",
                 "size": 10,
                 "color": "black"
                 },
                 "x":0.5 #center align
             },
            
    height = 300,
    autosize = True,
    #line along x axis
    xaxis = dict(
        showline = True,
        linecolor = 'black',
        linewidth = 2,
        automargin = True,
        tickfont=dict(size=9),
    ),
    #line along y axis
    yaxis = dict(
        showline = True,
        linecolor = 'black',
        linewidth = 2, 
        automargin = True,
        tickfont=dict(size=9)  
    ),
    plot_bgcolor = 'rgba(0,0,0,0)',
    paper_bgcolor = 'rgba(0,0,0,0)',
    xaxis_title =  "",
    yaxis_title =  ""
)

#heatmap
df3=df.groupby(['Area_Name'])[['Victims_Upto_10_Yrs','Victims_Between_10-14_Yrs','Victims_Between_14-18_Yrs','Victims_Between_18-30_Yrs','Victims_Between_30-50_Yrs','Victims_Above_50_Yrs']].sum().reset_index()
df3 = pd.melt(df3,id_vars=['Area_Name'],value_vars=['Victims_Upto_10_Yrs','Victims_Between_10-14_Yrs','Victims_Between_14-18_Yrs','Victims_Between_18-30_Yrs','Victims_Between_30-50_Yrs','Victims_Above_50_Yrs'],
             var_name='Age')

df3 = df3.pivot(index='Age',columns='Area_Name',values='value')
fig3 = px.imshow(df3,color_continuous_scale="Teal",aspect = "auto")
fig3.update_traces(hoverongaps=False,
                  hovertemplate = "Age : %{y}"
                                  "<br>Area_Name : %{x}"
                                  "<br>Cases : %{z} <extra></extra>"
                  )
fig3.update_layout(coloraxis_colorbar = dict(thickness = 10,len = 1),
    height=350,
    xaxis_tickfont = dict(size=9),
    yaxis_tickfont = dict(size=9),
    plot_bgcolor = 'rgba(0,0,0,0)',
    paper_bgcolor = 'rgba(0,0,0,0)',
    xaxis_tickangle = 55,
    xaxis_title =  "",
    yaxis_title =  ""
    )

#bar graph
df4=df.groupby(['Year'])[['Victims_Upto_10_Yrs','Victims_Between_10-14_Yrs','Victims_Between_14-18_Yrs','Victims_Between_18-30_Yrs','Victims_Between_30-50_Yrs','Victims_Above_50_Yrs','total_cases']].sum().reset_index()
df4 = pd.melt(df4,id_vars=['Year'],value_vars=['Victims_Upto_10_Yrs','Victims_Between_10-14_Yrs','Victims_Between_14-18_Yrs','Victims_Between_18-30_Yrs','Victims_Between_30-50_Yrs','Victims_Above_50_Yrs'],
                var_name='Age')
fig4 = px.bar(df4, x = 'Year' , y = 'value' , color = 'Age',color_discrete_sequence=px.colors.sequential.Teal)
fig4.update_layout(
    autosize = True,
    margin = dict(l=50,r=50,t=50,b=50),
    height = 350,
    legend = dict(orientation = "h",
                  entrywidth =110,
                  yanchor = "bottom",
                  y=1,
                  xanchor = "left",
                  x=0,
                  font = dict(size=9)
                  ),
    plot_bgcolor = 'rgba(0,0,0,0)',
    paper_bgcolor = 'rgba(0,0,0,0)'

)


#Age Group Trends Over Time: Line graphs for each age group, 


#SCATTER PLOT  showing the trend of reported cases over the years.
fig6 = px.line(df4,x='Year',y='value',color='Age',markers = True,color_discrete_sequence=px.colors.sequential.Teal)
#this will create a select/deselect option for Age in the graph
fig6.update_layout(dict(updatemenus=[
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
              ),
              legend = dict(orientation = "h",
                            entrywidth =110,
                            yanchor = "bottom",
                            y=1,
                            xanchor = "left",
                            x=0,
                            font = dict(size=9)
                            ),
              plot_bgcolor = 'rgba(0,0,0,0)',paper_bgcolor = 'rgba(0,0,0,0)')



#Sun Burst Chart
sunburst_df = df.melt(id_vars=['Year','Area_Name','Subgroup'],value_vars=['Victims_Upto_10_Yrs','Victims_Between_10-14_Yrs','Victims_Between_14-18_Yrs','Victims_Between_18-30_Yrs','Victims_Between_30-50_Yrs','Victims_Above_50_Yrs'],
                      var_name='age group',value_name='victim count')
fig8 = px.sunburst(sunburst_df,path=['Year','Area_Name','Subgroup','age group'],values= 'victim count')
fig8.update_layout(plot_bgcolor = 'rgba(0,0,0,0)',
                   paper_bgcolor = 'rgba(0,0,0,0)')
#Stacked Area Chart
df6 = df.groupby(['Year','Subgroup'])['Rape_Cases_Reported'].sum().unstack(fill_value=0).reset_index()
df6_melted = df6.melt(id_vars=['Year'], var_name= 'Subgroup' , value_name= 'Total Victims' )
fig9 = px.area(df6_melted,x='Year',y='Total Victims',color='Subgroup',color_discrete_map={"Victims of Incest Rape":"#0B6162" , "Victims of Other Rape":"#469B9D"})
fig9.update_layout (
    legend = dict(orientation = "h",
                  entrywidth =110,
                  yanchor = "bottom",
                  y=1,
                  xanchor = "left",
                  x=0,
                  font = dict(size=9)
                  ),
    plot_bgcolor = 'rgba(0,0,0,0)',
                    paper_bgcolor = 'rgba(0,0,0,0)')


df10 = df.groupby(['Year','Area_Name','Subgroup'])[['Victims_Upto_10_Yrs','Victims_Between_10-14_Yrs','Victims_Between_14-18_Yrs','Victims_Between_18-30_Yrs','Victims_Between_30-50_Yrs','Victims_Above_50_Yrs','total_cases']].sum().reset_index()
df10_melted = df10.melt(id_vars=['Year','Area_Name','Subgroup'] , value_vars=['Victims_Upto_10_Yrs','Victims_Between_10-14_Yrs','Victims_Between_14-18_Yrs','Victims_Between_18-30_Yrs','Victims_Between_30-50_Yrs','Victims_Above_50_Yrs'] ,var_name='Age')
print(df10_melted)

fig10 = px.treemap(df10_melted,
                   path=['Year','Area_Name','Subgroup','Age'],values='value')
fig10.update_traces(texttemplate='<b>%{label}</b><br>Value:%{value}')
fig10.update_traces(marker=dict(cornerradius=5))
fig10.update_layout(plot_bgcolor = 'rgba(0,0,0,0)',
                    paper_bgcolor = 'rgba(0,0,0,0)')

# define the app
app = Dash()
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container([ 
#Header

    # dash_table.DataTable(
    #     data=df10_melted.to_dict('records'),
    #     columns=[{'name':i,'id':i} for i in df10_melted.columns]
    # ),


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

_The **Figures** below shows the trends in cases throughout the decade with respect to diffrent parameters_ 

''',style={'textAlign':'center'})
        ])
    ]),


    dbc.Row([
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    dcc.Graph(id='Annual Trend Line Graph',figure=fig01)
                ]),
            className="shadow rounded",  # Adds shadow and margin bottom
            style={"backgroundColor":"#e8f5e9","border": "1px solid #6c757d", "border-radius": "10px","height":"380px"},  # Rounded corners            
            )
        ],width=3),


        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    dcc.Graph(id='graph',figure=fig03),
                ]),
            className="shadow rounded",  # Adds shadow and margin bottom
            style={"backgroundColor":"#e8f5e9","border": "1px solid #6c757d", "border-radius": "10px","height":"380px"},  # Rounded corners
            outline=True,                 
            )
        ]),


        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    dcc.Graph(id='graph', figure=fig02 , style={"height":"100%","width" : "100%"}),
                ]),
            className="shadow rounded",  # Adds shadow and margin bottom
            style={"backgroundColor":"#e8f5e9","border": "1px solid #6c757d", "border-radius": "10px","height":"380px"},  # Rounded corners 
            )], width=3),
    ]),
# line graph of total rape cases  


    dbc.Row([
        dbc.Col([
            dcc.Markdown('''

_Our dataset provides us with the **Demographic Insights** of the data , which can be best visualised through the *Graphs* below_ 

''',style={'textAlign':'center'})
        ])
    ]),
#heatmap

    dbc.Row([
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.H5("Heat Map",className="card-title-3"),
                    dcc.Graph(id = "graph3",figure = fig3)
                ]),
            className="shadow rounded",  # Adds shadow and margin bottom
            style={"backgroundColor":"#e8f5e9","border": "1px solid #6c757d", "border-radius": "10px","height":"370px"},  # Rounded corners
            outline=True, 
            )
        ],width=5),
        dbc.Col([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(id='graph5', figure=fig4 ),
            ]),
            className="shadow rounded",  # Adds shadow and margin bottom
            style={"backgroundColor":"#e8f5e9","border": "1px solid #6c757d", "border-radius": "10px","height":"370px"},  # Rounded corners
            #, outline=True, 
        )
        ],width=4),
        dbc.Col([
        dbc.Card(
            dbc.CardBody([
                dcc.Dropdown(
                    id='year-dropdown',
                    options = [{'label':year,'value':year} for year in df4['Year'].unique()],
                    value = df4['Year'].unique()[0],#default value
                    clearable=False,
                    style={'width':'100%'}
                ),
                dcc.Graph(id='pie-chart')
            ]),
            className="shadow rounded",  # Adds shadow and margin bottom
            style={"backgroundColor":"#e8f5e9","border": "1px solid #6c757d", "border-radius": "10px", 'height' : '370px', 'width' : '450px'},  # Rounded corners
        )
        ]),
    ],className='mb-4'),

    dbc.Row([
        dbc.Col([
        dbc.Card(
            dbc.CardBody([
                html.H5("Scatter Plot",className="card-title-8"),
                dcc.Graph(id = "graph8",figure = fig6)
            ]),
        className="shadow rounded",  # Adds shadow and margin bottom
        style={"backgroundColor":"#e8f5e9","border": "1px solid #6c757d", "border-radius": "10px",},  # Rounded corners
        outline=True,
            ) 
        ]),
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.H5("Area Chart",className="card-title-10"),
                    dcc.Graph(id = "graph10",figure = fig9)
                ]),
            className="shadow rounded",  # Adds shadow and margin bottom
            style={"backgroundColor":"#e8f5e9","border": "1px solid #6c757d", "border-radius": "10px",},  # Rounded corners
            outline=True, 
            )
        ]),
        dbc.Col([
            dcc.Markdown('''

_Out of the amount of cases we've analysed statistically, there's a significant amount of cases that are still unreported. In India, it's estimated that a staggering **99%** of sexual assault cases go unreported.The silence surrounding these cases not only hinders justice but also perpetuates a cycle of violence and impunity_ 

''',style={'textAlign':'left'}),

            dcc.Markdown('''

_The **Histogram** below shows the state wise Unreported Cases throughout the decade_ 

''',style={'textAlign':'center'}),

            dbc.Card(
                dbc.CardBody([
                    html.H5("Unreported Cases",className = "card-title-4"),
                    dcc.Graph(id = "graph4" , figure = fig2)
                ]),
            className="shadow rounded",  # Adds shadow and margin bottom
            style={"backgroundColor":"#e8f5e9","border": "1px solid #6c757d", "border-radius": "10px",},  # Rounded corners
            outline=True, 
            )
        ])

    ],className='mb-4'),

# statewise unreported rape victims graph
    dbc.Row([

    ],className='mb-4'),


    dbc.Row([
        dbc.Col([
            dcc.Markdown('''

_**The entire dataset can be studied upon using the folowing graphs**_ 

''',style={'textAlign':'center'})
        ])
    ]),



    dbc.Row([
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.H5("SunBurst CHart",className="card-title-9"),
                    dcc.Graph(id = "graph9",figure = fig8)
                ]),
            className="shadow rounded",  # Adds shadow and margin bottom
            style={"backgroundColor":"#e8f5e9","border": "1px solid #6c757d", "border-radius": "10px",},  # Rounded corners
            outline=True, 
            )
        ],width=4),
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.H5("Tree Map",className="card-title-11"),
                    dcc.Graph(id = "graph11",figure = fig10)
                ]),
            className="shadow rounded",  # Adds shadow and margin bottom
            style={"backgroundColor":"#e8f5e9","border": "1px solid #6c757d", "border-radius": "10px",},  # Rounded corners
            outline=True, 
            )
        ])
    ]),
        dbc.Row([

    ])
  



],fluid=True) # Use fluid=True to make it responsive for all screen sizes



#define callback

@app.callback(
    Output('pie-chart','figure'),
    [Input('year-dropdown','value')]
)


#pie chart
def update_pie_chart(selected_year):
    year_input =  df4[df4['Year'] == selected_year]
    fig5 = px.pie(year_input,values='value',names = 'Age', title = f'Victims by Age Group in {selected_year}',color_discrete_sequence=px.colors.sequential.Teal)
    fig5.update_layout(
    autosize = True,
    margin = dict(l=20,r=20,t=50,b=20),
    height = 300,
    plot_bgcolor = 'rgba(0,0,0,0)',
    paper_bgcolor = 'rgba(0,0,0,0)',
    legend = dict(font = dict(size=10))
    )
    return fig5

if __name__ == '__main__':
    app.run(debug=True)

