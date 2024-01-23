import streamlit as st
from extract_data import read_dataset, filter_dataset, aggregate_dataset_ts, plot_ts

df = read_dataset('dataset/regularite-mensuelle-intercites.csv')

inbound = st.selectbox("Départ", options = [''] + sorted(df.inbound.unique()), placeholder="Choisissez une gare de départ", label_visibility="visible")
outbound = st.selectbox("Arrivée", options = [''] + sorted(df.outbound.unique()), placeholder="Choisissez une gare d'arrivée", label_visibility="visible")


filtered_dataset = filter_dataset(data=df, inbound=inbound, outbound=outbound)

planned_trains_df = aggregate_dataset_ts(filtered_dataset, y = 'planned_trains')


canceled_trains_df  = aggregate_dataset_ts(filtered_dataset, y = 'canceled_trains') 
delayed_trains_df  = aggregate_dataset_ts(filtered_dataset, y = 'delayed_trains') 

COLS_TO_AGGREGATE = ['planned_trains', 'canceled_trains', 'delayed_trains']
ts_df = filtered_dataset.groupby(by = 'date', as_index=False)[COLS_TO_AGGREGATE].sum()
all_periods_df = filtered_dataset[COLS_TO_AGGREGATE].sum()

ts_df['delayed_percentage'] = ts_df['delayed_trains'] / ts_df['planned_trains']
all_periods_df['delayed_percentage'] = all_periods_df['delayed_trains'] / all_periods_df['planned_trains']


st.metric('Taux de retard', "{:.1%}".format(all_periods_df.delayed_percentage) , label_visibility="visible")

plot_ts(planned_trains_df, y='planned_trains')

st.line_chart(ts_df, x="date", y=COLS_TO_AGGREGATE)
