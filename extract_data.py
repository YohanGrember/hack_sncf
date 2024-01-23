import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import datetime

from typing import Optional
import streamlit as st



def read_dataset(dirname:str):
    df = pd.read_csv(dirname, delimiter = ';')
    
    df.rename({'depart': 'inbound', 'arrivee': 'outbound',
              'nombre_de_trains_programmes': 'planned_trains',
               'nombre_de_trains_ayant_circule': 'moving_trains',
               'nombre_de_trains_annules': 'canceled_trains',
               'nombre_de_trains_en_retard_a_l_arrivee': 'delayed_trains',
               'taux_de_regularite': 'regularity_percentage',
               'nombre_de_trains_a_l_heure_pour_un_train_en_retard_a_l_arrivee': 'ratio_on_time_vs_late',
              }, axis = 1, 
              inplace = True)
    
    df['date'] = pd.to_datetime(df['date'] + '-01')
    
    return(df)



def filter_dataset(data:pd.DataFrame, inbound:Optional[str], outbound:Optional[str]):
    df = data.copy()
    if inbound:
        df = df.loc[df.inbound == inbound]
        if outbound:
            df = df.loc[df.outbound == outbound]
    
    return(df)



def aggregate_dataset_ts(data:pd.DataFrame, y: str):
    data_agg = data.groupby(by = 'date', as_index=False)[y].sum()
    
    return(data_agg)



def plot_ts(data_agg:pd.DataFrame, y:str):
    st.line_chart(data_agg, x = 'date', y=y)

def get_outbounds(df):
    return df.outbound.unique()



