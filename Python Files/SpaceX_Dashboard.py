#!/usr/bin/env python
# coding: utf-8

# # Dashboard

# **In this section we are going to explore that how we can create Interactive <code>Dashboards</code> from SpaceX data with the help of Plotly Dash**
# 
# Data visualization is the visual presentation of data or information. The goal of data visualization is to communicate data or information clearly and effectively to readers. Typically, data is visualized in the form of a chart, infographic, diagram or map. The field of data visualization combines both art and data science. While a data visualization can be creative and pleasing to look at, it should also be functional in its visual communication of the data.

# # Objectives
# 
# Perform exploratory Data Analysis and Feature Engineering using Pandas and Matplotlib
# - Data Visualization
# - Exploratory Data Analysis
# - Dashboards
# 
# ![spaceX data](https://www.teslarati.com/wp-content/uploads/2020/04/Falcon-Heavy-Demo-Feb-2018-SpaceX-1-crop-2048x956.jpg)

# In[2]:


# Libraries to read csv files and perform data processing.
import pandas as pd
import numpy as np

# Dashboard Related Libraries
import plotly.express as px
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input,Output


# After importing the necessary libraries Now we have to read the spaceX Launces Data.

# In[13]:


spacex = pd.read_csv("C:\\Users\\003EPO744\\Desktop\\projects\\SpaceX-End-To-End-Machine-Learning-Project\\Data\\dataset_part_2.csv")


# In[47]:


spacex.head()


# In[50]:


max_payload = spacex['PayloadMass'].max()
min_payload = spacex['PayloadMass'].min()
all_sites = [{'label': 'All Sites', 'value': 'ALL'}]
all_sites.extend([{'label':item,'value':item} for item in list(spacex['LaunchSite'].unique())])


# In[68]:


# Get Total Number Launches
total_launches = spacex.shape[0]
success_launches = spacex[spacex['Class']==1].shape[0]
failure_launches = spacex[spacex['Class']==0].shape[0]


# The Dashboard will help us to understand the useful insights of above data.

# # Initilization of Dashboard App
# 
# The app will get initialize with the help of <code>dash.Dash</code>. We can use the <code>Dash</code> class to initialize the Dashboard Instance.

# In[3]:


app = dash.Dash(__name__)


# # Define the Layout of Dashboard.
# 
# Before you create a layout in Dash, it would be a good idea to have a sketch of what the app would look like, for example draw it on the paper (what I did) or even use powerpoint to design the layout. You could also look at the Dash Gallery for some inspration. I'm using use the following template for my app.

# ```python
# app.layout = html.Div(children=[
#     html.Div(children=[
#         html.H2(children='SpaceX Past Launches Data'),
#         html.H4(children='Launches overview 2010-2020', style={'marginTop': '-15px', 'marginBottom': '30px'})
#     ], style={'textAlign': 'center'})
# ], style={'padding': '2rem'})
# ```

# # Add Heading Of Dashboard.

# # Add Layout of Dashboard

# In[73]:


from datetime import datetime as dt
app.layout = html.Div(children=[
    # Headings     
    html.Div(children=[
        html.H2(children='SpaceX Past Launches Data'),
        html.H4(children='Launches overview 2010-2020', style={'marginTop': '-15px', 'marginBottom': '30px'})
    ], style={'textAlign': 'center'}),
    
        # Filter     
        html.Div(children=[
        ################### Filter box ###################### 
        html.Div(children=[
            html.Label('Filter by date (M-D-Y):'),
            dcc.DatePickerRange(
                id='input_date',
                month_format='DD/MM/YYYY',
                show_outside_days=True,
                minimum_nights=0,
                initial_visible_month=dt(2010, 1, 1),
                min_date_allowed=dt(2010, 1, 1),
                max_date_allowed=dt(2020, 12, 31),
                start_date=dt.strptime("2020-06-01", "%Y-%m-%d").date(),
                end_date=dt.strptime("2020-12-31", "%Y-%m-%d").date()
            ),

            html.Label('Launch Sites:', style={'paddingTop': '2rem'}),
            dcc.Dropdown(
                id='input-dropdown',
                options=all_sites,
                value='ALL',
                placeholder="Select a Launch Site here",
                searchable=True
            ),

            html.Label('PayLoad Mass (KG):', style={'paddingTop': '2rem'}),
            dcc.RangeSlider(
                    id='payload-limit',
                    min=min_payload,
                    max=max_payload,
                    step=1,
                    value=[min_payload,max_payload],
                    marks={
                        0: '0',
                        2500: '2500',
                        5000: '5000',
                        7500: '7500',
                        10000: '10000'
                    },
            ),

        ], className="four columns",
        style={'padding':'2rem', 'margin':'1rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px', 'marginTop': '2rem'} )

        ##### HERE insert the code for four boxes & graph #########
    ]),
    
    # Number statistics & number of accidents each day

    html.Div(children=[
        html.Div(children=[
            html.Div(children=[
                html.H3(children=total_launches,id='total_launches', style={'fontWeight': 'bold'}),
                html.Label('Total Launches', style={'paddingTop': '.3rem'}),
            ], className="two columns number-stat-box"),

            html.Div(children=[
                html.H3(children=success_launches,id='success_launches', style={'fontWeight': 'bold', 'color': '#00aeef'}),
                html.Label('Successful Launches', style={'paddingTop': '.3rem'}),
            ], className="two columns number-stat-box"),

            html.Div(children=[
                html.H3(children=failure_launches,id='failure_launches', style={'fontWeight': 'bold', 'color': '#f73600'}),
                html.Label('Unsuccessful Launches', style={'paddingTop': '.3rem'}),
            ], className="two columns number-stat-box"),

            html.Div(children=[
                dcc.Graph(id="pie-chart")

            ], className="six columns number-stat-box"),
        ], style={'margin':'1rem', 'display': 'flex', 'justify-content': 'space-between', 'width': '100%', 'flex-wrap': 'wrap'}),

        # Line chart for accidents per day
        html.Div(children=[
            dcc.Graph(id='scatter-plot')
        ], className="twleve columns", style={'padding':'.3rem', 'marginTop':'1rem', 'marginLeft':'1rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px', 'backgroundColor': 'white', }),

    ], className="eight columns", style={'backgroundColor': '#f2f2f2', 'margin': '1rem'}),
], style={'padding': '2rem'})


# # Add Callbacks

# In[60]:


# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='pie-chart', component_property='figure'),
    Input(component_id='input-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    filtered_df = spacex
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='Class', names='LaunchSite', title='Total Success Launces By Site')
        return fig
    else:
        filtered_df = filtered_df[filtered_df['LaunchSite'] == entered_site]
        fig = px.pie(values=filtered_df['Class'].value_counts().to_list(), names=[0,1], title=f'Total Success Launces For Site {entered_site}')
        return fig
    

# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='scatter-plot', component_property='figure'),
    [Input(component_id='input-dropdown', component_property='value'),
     Input(component_id="payload-limit", component_property="value")]
)
def update_output(entered_site, payload_kg):
    filtered_df = spacex[(spacex['PayloadMass'] >= payload_kg[0]) & (spacex['PayloadMass'] <= payload_kg[1])]
    if entered_site == 'ALL':
        figure = px.scatter(filtered_df,x='PayloadMass',y='Class',color='BoosterVersion')
        return figure
    else:
        df = filtered_df[filtered_df['Launch Site'] == entered_site]
        figure = px.scatter(df, x='Payload Mass (kg)', y='Class',color='BoosterVersion')
        return figure


# # Can I run dash app in jupyter?
# The <code>show_app</code> function will help to run the dash app in JupyterNotebook without any issue.
# But you an extension also to do the same thing.\
# 
# ```python
# pip install jupyterlab_dash
# 
# 
# import jupyterlab_dash
# import dash
# import dash_html_components as html
# 
# viewer = jupyterlab_dash.AppViewer()
# 
# app = dash.Dash(__name__)
# 
# app.layout = html.Div('Hello World')
# 
# viewer.show(app)
# 
# ```
# ### But here I have used the Function to run the dash app in Jupyter notebook.

# In[15]:


from IPython import display
def show_app(app,  # type: dash.Dash
             port=9999,
             width=700,
             height=350,
             offline=True,
             style=True,
             **dash_flask_kwargs):
    """
    Run the application inside a Jupyter notebook and show an iframe with it
    :param app:
    :param port:
    :param width:
    :param height:
    :param offline:
    :return:
    """
    url = 'http://localhost:%d' % port
    iframe = '<iframe src="{url}" width={width} height={height}></iframe>'.format(url=url,
                                                                                  width=width,
                                                                                  height=height)
    display.display_html(iframe, raw=True)
    if offline:
        app.css.config.serve_locally = True
        app.scripts.config.serve_locally = True
    if style:
        external_css = ["https://fonts.googleapis.com/css?family=Raleway:400,300,600",
                        "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
                        "http://getbootstrap.com/dist/css/bootstrap.min.css", ]

        for css in external_css:
            app.css.append_css({"external_url": css})

        external_js = ["https://code.jquery.com/jquery-3.2.1.min.js",
                       "https://cdn.rawgit.com/plotly/dash-app-stylesheets/a3401de132a6d0b652ba11548736b1d1e80aa10d/dash-goldman-sachs-report-js.js",
                       "http://getbootstrap.com/dist/js/bootstrap.min.js"]

        for js in external_js:
            app.scripts.append_script({"external_url": js})

    return app.run_server(debug=True,  # needs to be false in Jupyter
                          port=port,
                          **dash_flask_kwargs)


# Note: For use in JupyterLab, JupyterDash makes use of the <code>jupyterlab-dash</code> JupyterLab extension that was originally developed and maintained by solving the issue that we were facing while running dash app in Juypyter. Development of this extension has also been moved to the JupyterDash repository.

# ## Run the Application

# In[75]:


if __name__ == '__main__':
    show_app(app)


# # Final Result.

# # End
