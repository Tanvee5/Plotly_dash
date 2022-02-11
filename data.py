# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 22:04:46 2022

@author: DELL
"""

import pandas as pd
from dash import dash_table, dcc



def make_data_table(df):
    data_table = dash_table.DataTable(
        id="data-table",
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("records"),
        
    )

    return data_table
