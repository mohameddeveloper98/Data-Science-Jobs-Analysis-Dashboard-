import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px


# Text field
def drawText(text,paragraph,style):
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.H2(text,style={'color':style}),
                    html.H5(paragraph)
                ], style={'textAlign': 'center'}) 
            ])
        ),
    ])

# Data
data_path = 'data_cleaned_2021.csv'
df2 = pd.read_csv(data_path)

# Cleaning Na and Other Jobs Before Displaying
df2.drop(axis = 0 , index = df2[df2.job_title_sim == 'na'].index , inplace = True )
df2.drop(axis = 0 , index = df2[df2.job_title_sim.str.startswith( 'other')].index , inplace = True )


def draw_average_salary():
    # Group by each job and get the average salary for each job
    # divide by 12 to get the mounthly salary not per salary
    jobs = df2.groupby(['job_title_sim']).median()['Avg Salary(K)'].sort_values(ascending=False)
                    
    return  html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                figure= px.histogram(jobs,x= jobs.index,y = jobs.values,
                    opacity=0.8,text_auto=True,color_discrete_sequence=["#f2f3f4"],range_y=[0,150]).update_layout(
                    template='plotly_dark',
                    plot_bgcolor= 'rgba(0, 0, 0, 0)',
                    paper_bgcolor= 'rgba(0, 0, 0, 0)',
                    title_text='Average Salary per year', # title of plot
                    xaxis_title_text='Job', # xaxis label
                    yaxis_title_text='Average Salary K$', # yaxis label
                    ),
                config={
                        'displayModeBar': False
            }
                ) 
            ]),
            
        ),  
    ])
    

def draw_top_sector():
    return  html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    figure=px.histogram(df2,x= df2['Sector'].value_counts().index[:10],y = df2['Sector'].value_counts().values[:10]
                   ,opacity=0.8,color_discrete_sequence=["#3fff00"],range_y=[0,180]).update_layout(
                        template='plotly_dark',
                        plot_bgcolor= 'rgba(0, 0, 0, 0)',
                        paper_bgcolor= 'rgba(0, 0, 0, 0)',
                        title_text='Top 10 Sectors', # title of plot
                        xaxis_title_text='Sector', # xaxis label
                        yaxis_title_text='Count', # yaxis label
                    ),
                    config={
                        'displayModeBar': True
                    }
                ) 
            ])
        ),  
    ])

def draw_job_titles():
                    
    return  html.Div([
            dbc.Card(
                dbc.CardBody([
                dcc.Graph(
                figure=px.histogram(df2,x= df2['job_title_sim'].value_counts().index[:10],y = df2['job_title_sim'].value_counts().values[:10],
                    opacity=0.8,color_discrete_sequence=["#ff6e4a"]).update_layout(
                    template='plotly_dark',
                    plot_bgcolor= 'rgba(0, 0, 0, 0)',
                    paper_bgcolor= 'rgba(0, 0, 0, 0)',
                    title_text='Job Titles', # title of plot
                    xaxis_title_text='Title', # xaxis label
                    yaxis_title_text='Frequency', # yaxis label
                    ),
                config={
                        'displayModeBar': False
            }
                ) 
            ])
            
        ),  
    ])
    
    
def draw_top_skill():
    df_skills = df2.iloc[:,23:38].copy()
    df_skills
    skill_value = df_skills.sum(axis = 0).sort_values(ascending=False)
    
    return  html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                figure=px.histogram(skill_value, x =skill_value.index,y=skill_value.values,color_discrete_sequence=["#ffae42"]).update_layout(
                    template='plotly_dark',
                    plot_bgcolor= 'rgba(0, 0, 0, 0)',
                    paper_bgcolor= 'rgba(0, 0, 0, 0)',
                    title_text='Skills Needed', # title of plot
                    xaxis_title_text='Skill', # xaxis label
                    yaxis_title_text='Frequency', # yaxis label
                    ),
                config={
                        'displayModeBar': False
            }
                ) 
            ])
        
        ),  
    ])


# Build App
app = JupyterDash(external_stylesheets=[dbc.themes.SLATE])
app.title='Data Science Jobs'
app.layout = html.Div([
    dbc.Card(
        dbc.CardBody([
            dbc.Row(
                [   
                    dbc.Col(dbc.CardImg(src="/static/images/glassdoor-logo.jpg",),width=2),
                    dbc.Col(html.H1("Data Science Jobs Analysis",
                            style={'color':'#f2f3f4'})),#32cd32
                    # dbc.Col(dcc.Dropdown(id='Top 10',options={'Top Skills':'skill','sector':'sector','location':'loc'}))
                    # To be continued with button to go to next page and deploy ML Model
                ],align='center'),
            
            html.Br(),
            
            dbc.Row([
                dbc.Col([
                    drawText("88k $","Average Salary","#f2f3f4")
                ], width=3),
                
                dbc.Col([
                    drawText("IT","Sector","#3fff00")
                ], width=3),
                
                dbc.Col([
                    drawText("Data Scientist","Job","#ff6e4a")
                ], width=3),
                dbc.Col([
                    drawText("Python","Skill","#ffae42") #6a5acd #00b7eb
                ], width=3),
            ], align='center'), 
            
            html.Br(),
            
            dbc.Row([
                
                dbc.Col([
                    draw_average_salary()
                ], width=6),
                dbc.Col([
                    draw_top_sector() 
                ], width=6),
            ], align='center'), 
            
            html.Br(),
            
            dbc.Row([
                dbc.Col([
                    draw_job_titles()
                ], width=6),
                dbc.Col([
                    draw_top_skill()
                ], width=6),
            ], align='center'),      
        ]), color = 'dark'
    )
])

# Run app and display result inline in the notebook
app.run_server(port = 8082)
