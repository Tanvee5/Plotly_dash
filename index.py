# -*- coding: utf-8 -*-
"""
Created on Sat Feb  5 20:56:27 2022

@author: DELL
"""

from login import app
from login import server
import dash_html_components as html
import dash_core_components as dcc
import dash
from dash import dependencies, no_update
import json, ast


import base64
import io


import pandas as pd
from components import *
from graph import *
from data import *
import column as col



#from userss import USERNAME_PASSWORD_PAIRS

app.layout = html.Div([
  dcc.Location(id='url', refresh=False),
  html.Div(id='page-content')
                     ])

register_page = html.Div([
html.Div(dcc.Link('Signin', href='index_page ',
style={'color':'#bed4c4','font-family': 'serif', 
'font-weight': 'bold', "text-decoration": "none",'font-size':'20px'}),
style={'padding-left':'80%','padding-top':'10px'}),
html.Div(
dcc.Input(id="user", type="text", placeholder="Enter Username",className="inputbox1",
style={'margin-left':'35%','width':'450px','height':'45px','padding':'10px','margin-top':'60px',
'font-size':'16px','border-width':'3px','border-color':'#a0a3a2'
}),
),
html.Div(
dcc.Input(id="passw", type="password", placeholder="Enter Password",className="inputbox2",
style={'margin-left':'35%','width':'450px','height':'45px','padding':'10px','margin-top':'10px',
'font-size':'16px','border-width':'3px','border-color':'#a0a3a2',
}),
),
html.Div(
dcc.Input(id="passw", type="password", placeholder="Again enter Password",className="inputbox2",
style={'margin-left':'35%','width':'450px','height':'45px','padding':'10px','margin-top':'10px',
'font-size':'16px','border-width':'3px','border-color':'#a0a3a2',
}),
),
html.Div(
html.Button('Register', id='register', n_clicks=0, style={'border-width':'3px','font-size':'14px'}),
style={'margin-left':'45%','padding-top':'30px'}),
html.Div(id='output2')
])

@app.callback(
    dependencies.Output('output2', 'children'),
    dependencies.Input('register', 'n_clicks'),
    dependencies.State("user", "value"),
    dependencies.State("passw", "value"),
        prevent_initial_call=True)
def register(n_clicks, user, passw):
    file = open("userss.py","r")
    contents= file.read()
    oli = ast.literal_eval(contents)
    if user =='' or user == None or passw =='' or passw == None:
        return html.Div(children='',style={'padding-left':'550px','padding-top':'10px'})
    if user in oli:
        return html.Div(children='User is already',style={'padding-left':'550px','padding-top':'40px','font-size':'16px'})
    else:
        nli = {user : passw}
        oli.update(nli)
        with open("userss.py","w") as inp:
            inp.write(json.dumps(oli))
        return html.Div(dcc.Link('Access Granted!', href='/index_page',style={'color':'#183d22','font-family': 'serif', 'font-weight': 'bold', "text-decoration": "none",'font-size':'20px'}),style={'padding-left':'605px','padding-top':'40px'})
        

index_page = html.Div([
html.Div(
dcc.Input(id="user", type="text", placeholder="Enter Username",className="inputbox1",
style={'margin-left':'35%','width':'450px','height':'45px','padding':'10px','margin-top':'60px',
'font-size':'16px','border-width':'3px','border-color':'#a0a3a2'
}),
),
html.Div(
dcc.Input(id="passw", type="text", placeholder="Enter Password",className="inputbox2",
style={'margin-left':'35%','width':'450px','height':'45px','padding':'10px','margin-top':'10px',
'font-size':'16px','border-width':'3px','border-color':'#a0a3a2',
}),
),
html.Div(
html.Button('Verify', id='verify', n_clicks=0, style={'border-width':'3px','font-size':'14px'}),
style={'margin-left':'45%','padding-top':'30px'}),
html.Div(id='output1')
])

@app.callback(
    dependencies.Output('output1', 'children'),
    dependencies.Input('verify', 'n_clicks'),
    dependencies.State("user", "value"),
    dependencies.State("passw", "value"),
        prevent_initial_call=True)
def update_output(n_clicks, uname, passw):
    file = open("userss.py","r")
    contents= file.read()
    oli = ast.literal_eval(contents)
    if uname =='' or uname == None or passw =='' or passw == None:
        return html.Div(children='',style={'padding-left':'550px','padding-top':'10px'})
    if uname not in oli:
        return html.Div(children='Incorrect Username',style={'padding-left':'550px','padding-top':'40px','font-size':'16px'})
    if oli[uname]==passw:
        return html.Div(dcc.Link('Access Granted!', href='/next_page',style={'color':'#183d22','font-family': 'serif', 'font-weight': 'bold', "text-decoration": "none",'font-size':'20px'}),style={'padding-left':'605px','padding-top':'40px'})
    else:
        return html.Div(children='Incorrect Password',style={'padding-left':'550px','padding-top':'40px','font-size':'16px'})



df = pd.read_csv("dataset.csv")

# Components
input_header = html.H2("Knowledge Graph Input")
upload_button = dcc.Upload(
        id="upload-data",
        children=html.Button(className="button", children="Upload CSV")
    )
upload_result = html.Div(id="upload-result")
output_header = html.H2("Knowledge Graph Output")
data_table = make_data_table(df)

#G = init_graph(df)
#elements = convert_nx_to_cyto(G)
#viz = visualize_graph(elements)


next_page = html.Div(children=[
html.Div(dcc.Link('Log out', href='/',style={'color':'#bed4c4','font-family': 'serif', 'font-weight': 'bold', "text-decoration": "none",'font-size':'20px'}),style={'padding-left':'80%','padding-top':'10px'}),
 html.Div(className="container", children=[
        input_header,
        html.P(children=[
            "You may upload your own input file to generate a knowledge graph. Make sure it is a csv file with the following columns: ",
            html.B("id, outcome, correlation, significance, number of samples, relative weight, rescaled weight")
        ]),
         upload_result,
        upload_button,
        html.Div(id="table-div", children=data_table)
        #html.Div(id="graph-div", children=viz)
         ])
])

@app.callback(
        dependencies.Output("upload-result", "children"),
        dependencies.Output("table-div", "children"),
        dependencies.Input("upload-data", "contents"),
        dependencies.State("upload-data", "filename"),
        prevent_initial_call=True
    )
def update_data(content, filename):
    if content is None:
        raise PreventUpdate
    content_type, content_string = content.split(",")
    decoded = base64.b64decode(content_string)

    error = html.P(className="red-text", children="Invalid input. Make sure you upload a CSV file with the necessary columns.")
    success = html.P("File uploaded: {}".format(filename))
    try:
        if "csv" in filename:
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
            # validate columns
            if not set([
                col.ID,
                col.CORRELATION,
                col.OUTCOME
                ]).issubset(df.columns):
                
                return error, no_update, no_update, no_update, no_update, no_update, no_update
        else:
            return error, no_update, no_update, no_update, no_update, no_update, no_update
    except Exception as e:
        return error, no_update, no_update, no_update, no_update, no_update, no_update
    
    #G = graph.init_graph(df)
    #elements = graph.convert_nx_to_cyto(G)
    #viz = graph.visualize_graph(elements)

    return success, df.to_dict("records"), elements, data_table




@app.callback(dependencies.Output('page-content', 'children'),
[dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/next_page':
        return next_page;
    if pathname == '/register_page':
        return register_page
    else:
       return index_page

if __name__ == '__main__':
    app.run_server(debug=True)