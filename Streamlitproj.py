import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from datetime import datetime
import pmdarima as pm



st.set_page_config(layout='wide', initial_sidebar_state='expanded')


#Data
#data = pd.read_excel('data/DF_dashboard2.xlsx')

@st.cache_data
def load_data(file_path):
    df = pd.read_excel(file_path)  # Assuming it's an Excel file
    return df

# Update the file path to the location on your computer
file_path = 'data/DF_dashboard2.xlsx'
data = load_data(file_path)

st.button("Rerun")


st.title('Dashboard actualizado al 17/11/2023')
st.markdown("## Información descriptiva de las ventas en monto y unidades", unsafe_allow_html=True)

st.sidebar.image('data/logo.png', caption='Consultora de innovación y transformación digital apalancada en diseño, tecnología y emprendimiento')
st.sidebar.header('Zona de filtrado')
canal = st.sidebar.multiselect('Selecciona el canal',
                               options=data['Canal'].unique(),
                               default=data['Canal'].unique())

medio = st.sidebar.multiselect('Selecciona el medio',
                               options=data['Medio'].unique(),
                               default=data['Medio'].unique())


plataforma = st.sidebar.multiselect('Selecciona la plataforma',
                               options=data['des_plataforma'].unique(),
                               default=data['des_plataforma'].unique())

subplataforma = st.sidebar.multiselect('Selecciona la subplataforma',
                               options=data['des_subplataforma'].unique(),
                               default=data['des_subplataforma'].unique())

marca = st.sidebar.multiselect('Selecciona la marca',
                               options=data['des_marca'].unique(),
                               default=data['des_marca'].unique())
#Obteniendo los valores mínimos y máximos de la DATA
startDate = data['Fecha'].min()
endDate = data['Fecha'].max()

col1, col2 = st.columns(2)
with col1:
    date1 = st.date_input('Fecha inicial', startDate)

with col2:
    date2 = st.date_input('Fecha final', endDate)


#Funcion para utilizar la variable tiempo
def convert(fecha_str):
    f_obj = fecha_str 
    f_fil = f_obj.strftime('%Y-%m')

    return f_fil


date1_1 = convert(date1)
date2_1 = convert(date2)


#df_select = data.query('Canal == @canal & Medio == @medio & des_plataforma == @plataforma & des_subplataforma == @subplataforma & des_marca == @marca')
#df_select = data.query('Canal == @canal & Medio == @medio & des_plataforma == @plataforma & des_subplataforma == @subplataforma & des_marca == @marca & @date1 <= Fecha <= @date2')
df_select = data.query('Canal == @canal & Medio == @medio & des_plataforma == @plataforma & des_subplataforma == @subplataforma & des_marca == @marca')
df_select = df_select[(df_select['Tiempo'] >= date1_1) & (df_select['Tiempo'] <= date2_1)]


#KPIs importantes
monto_total = int(df_select['MONTO'].sum())
und_total = int(df_select['UND'].sum())

left_column, right_column = st.columns(2)
with left_column:
    st.info('Monto total', icon='💰')
    st.metric(label='Suma total',value=f'S/. {monto_total:,.2f}')

with right_column:
    st.info('Unidades totales', icon='📦')
    st.metric(label='Suma total',value=f'{und_total:,.0f}')


#Grafico uno
dfig1 = df_select.groupby('Tiempo')['MONTO'].sum().reset_index()
fig1 = px.line(dfig1, x=dfig1['Tiempo'],y=dfig1['MONTO'],title='<b> Evolución del monto total en millones de soles </b>',
               template='plotly_dark')
#st.plotly_chart(fig1)

#Grafico dos
dfig2 = df_select.groupby('Tiempo')['UND'].sum().reset_index()
fig2 = px.line(dfig2, x=dfig2['Tiempo'],y=dfig2['UND'], title='<b> Evolución las unidades vendidas totales en millones </b>',
               template='plotly_dark')
#st.plotly_chart(fig2)

left, right = st.columns(2)
left.plotly_chart(fig1, use_container_width=True)
right.plotly_chart(fig2, use_container_width=True)


#Grafico 3
dfig3 = df_select.groupby(['Tiempo', 'Canal'])['MONTO'].sum().reset_index()
fig3 = px.bar(dfig3, x=dfig3['Tiempo'], y=dfig3['MONTO'], color='Canal', title='<b> Evolución del monto vendido por canales en millones de soles </b>')
#st.plotly_chart(fig3)

#Grafico 4
dfig4 = df_select.groupby(['Tiempo', 'Medio'])['MONTO'].sum().reset_index()
fig4 = px.bar(dfig4, x=dfig4['Tiempo'], y=dfig4['MONTO'], color=dfig4['Medio'], title='<b> Evolución del monto vendido por medios en millones de soles </b>')
#st.plotly_chart(fig4)

left2, right2 = st.columns(2)
left2.plotly_chart(fig3, use_container_width=True)
right2.plotly_chart(fig4, use_container_width=True)

#Grafico 5 marcas seleccionadas
#PRIMOR, BOLIVAR, SAPOLIO, ALACENA, DON VITTORIO, OPAL, NICOLINI, MARSELLA, SAO, BLANCA FLOR
marcas = ['Primor', 'Bolivar', 'Sapolio', 'Alacena', 'Don Vittorio', 'Opal',
          'Nicolini', 'Marsella', 'Sao', 'Blanca Flor']
dfig5 = df_select[df_select['des_marca'].isin(marcas)]
dfig5 = dfig5.groupby(['Tiempo', 'des_marca'])['MONTO'].sum().reset_index()
fig5 = px.bar(dfig5, x=dfig5['Tiempo'], y=dfig5['MONTO'], color=dfig5['des_marca'], title='<b> Evolución del monto vendido por marcas seleccionadas </b>')
#st.plotly_chart(fig5)


#Figura 5.1
figx = go.Figure()
dfigx= df_select.groupby('Canal')[['MONTO', 'UND']].sum().reset_index()
figx.add_trace(go.Bar(x=dfigx['Canal'],y=dfigx['MONTO'],name='Monto'))
figx.add_trace(go.Bar(x=dfigx['Canal'],y=dfigx['UND'],name='Unidades'))
figx.update_layout(title='Monto y unidades vendidas por los cuatro canales acumulados hasta 2023-10')
#st.plotly_chart(figx, use_container_width =True)

left3, right3 = st.columns(2)
left3.plotly_chart(fig5, use_container_width=True)
right3.plotly_chart(figx, use_container_width=True)


#Grafico 7 

fig7 = px.treemap(df_select, path=['Canal', 'Medio','des_categoria'],values= 'MONTO', hover_data=['MONTO'], color='des_categoria',
                  title='Participación de las categorias por medio, dentro de cada canal')
fig7.update_layout(width=800,height=650)
st.plotly_chart(fig7)

#
det_produc, top_monto, top_und = st.tabs(['Detalle de Productos','Top Monto', 'Top Unidades'])
with det_produc:
    st.header('Detalle de productos')
    datcua3 = df_select[['Canal','Medio','des_categoria','Material',
                         'UND','MONTO','Tiempo']]
    st.write(datcua3)

with top_monto:
    st.header('Top en monto por categoría')
    datcua1 = df_select.groupby('des_categoria')['MONTO'].sum().reset_index()
    st.write(datcua1)

with top_und:
    st.header('Top en unidades por categoría')
    datcua2 = df_select.groupby('des_categoria')['UND'].sum().reset_index()
    st.write(datcua2)


st.markdown("## Proyecciones del top 4 de categorías por monto", unsafe_allow_html=True)

top5monto = ['Aceites', 'Detergentes', 'Salsas', 'Pastas', 'Conservas']
pro1 = df_select[df_select['des_categoria'].isin(top5monto)]
pro1 = pro1.groupby(['Canal','des_categoria', 'Tiempo'])[['MONTO','UND']].sum().reset_index()

st.markdown("### CENCOSUD", unsafe_allow_html=True)

# PROYECCION
## figp_1
df_figp1 = pro1[(pro1['Canal'] == 'CENCOSUD') & (pro1['des_categoria'] == 'Aceites')]

mod1 = pm.auto_arima(df_figp1['MONTO'], start_p=1, start_q=1, max_p=3, max_q=3, m=12,
                       start_P=0, seasonal=True, d=1, D=1, trace=True,
                       n_jobs=-1,  # We can run this in parallel by controlling this option
                       error_action='ignore',  # don't want to know if an order does not work
                       suppress_warnings=True,  # don't want convergence warnings
                       stepwise=False, random=True, random_state=42,  # we can fit a random search (not exhaustive)
                       n_fits=25)

pre1 = mod1.predict(n_periods = 5)

pre11 = pd.DataFrame(pre1, columns=['MONTO'])
pre11['Tiempo'] = ['2023-11', '2023-12', '2024-01', '2024-02', '2024-03']

df_figpp1 = df_figp1[['Tiempo', 'MONTO']]
df_figpp1 = pd.DataFrame(df_figpp1)

df_final_pro1 = pd.concat([df_figpp1, pre11])
#st.write(df_final_pro1)

fig_forecast_1 = px.line(df_final_pro1, x=df_final_pro1['Tiempo'],y=df_final_pro1['MONTO'],title='<b> Evolución del monto total en miles de soles de la categoria Aceites </b>',
              template='plotly_dark', markers=True)
fig_forecast_1.update_traces(line_color="firebrick")


## figp_2
df_figp2 = pro1[(pro1['Canal'] == 'CENCOSUD') & (pro1['des_categoria'] == 'Detergentes')]

mod2 = pm.auto_arima(df_figp2['MONTO'], start_p=1, start_q=1, max_p=3, max_q=3, m=12,
                       start_P=0, seasonal=True, d=1, D=1, trace=True,
                       n_jobs=-1,  # We can run this in parallel by controlling this option
                       error_action='ignore',  # don't want to know if an order does not work
                       suppress_warnings=True,  # don't want convergence warnings
                       stepwise=False, random=True, random_state=42,  # we can fit a random search (not exhaustive)
                       n_fits=25)

pre2 = mod2.predict(n_periods = 5)

pre22 = pd.DataFrame(pre2, columns=['MONTO'])
pre22['Tiempo'] = ['2023-11', '2023-12', '2024-01', '2024-02', '2024-03']

df_figpp2 = df_figp2[['Tiempo', 'MONTO']]
df_figpp2 = pd.DataFrame(df_figpp2)

df_final_pro2 = pd.concat([df_figpp2, pre22])
#st.write(df_final_pro1)

fig_forecast_2 = px.line(df_final_pro2, x=df_final_pro2['Tiempo'],y=df_final_pro2['MONTO'],title='<b> Evolución del monto total en miles de soles de la categoria Detergentes </b>',
              template='plotly_dark', markers=True)
fig_forecast_2.update_traces(line_color="firebrick")


left, right = st.columns(2)
left.plotly_chart(fig_forecast_1, use_container_width=True)
right.plotly_chart(fig_forecast_2, use_container_width=True)


########################################################################################

## figp_3
df_figp3 = pro1[(pro1['Canal'] == 'CENCOSUD') & (pro1['des_categoria'] == 'Salsas')]

mod3 = pm.auto_arima(df_figp3['MONTO'], start_p=1, start_q=1, max_p=3, max_q=3, m=12,
                       start_P=0, seasonal=True, d=1, D=1, trace=True,
                       n_jobs=-1,  # We can run this in parallel by controlling this option
                       error_action='ignore',  # don't want to know if an order does not work
                       suppress_warnings=True,  # don't want convergence warnings
                       stepwise=False, random=True, random_state=42,  # we can fit a random search (not exhaustive)
                       n_fits=25)

pre3 = mod3.predict(n_periods = 5)

pre33 = pd.DataFrame(pre3, columns=['MONTO'])
pre33['Tiempo'] = ['2023-11', '2023-12', '2024-01', '2024-02', '2024-03']

df_figpp3 = df_figp3[['Tiempo', 'MONTO']]
df_figpp3 = pd.DataFrame(df_figpp3)

df_final_pro3 = pd.concat([df_figpp3, pre33])
#st.write(df_final_pro1)

fig_forecast_3 = px.line(df_final_pro3, x=df_final_pro3['Tiempo'],y=df_final_pro3['MONTO'],title='<b> Evolución del monto total en miles de soles de la categoria Salsas </b>',
              template='plotly_dark', markers=True)
fig_forecast_3.update_traces(line_color="firebrick")

## figp_4
df_figp4 = pro1[(pro1['Canal'] == 'CENCOSUD') & (pro1['des_categoria'] == 'Pastas')]

mod4 = pm.auto_arima(df_figp4['MONTO'], start_p=1, start_q=1, max_p=3, max_q=3, m=12,
                       start_P=0, seasonal=True, d=1, D=1, trace=True,
                       n_jobs=-1,  # We can run this in parallel by controlling this option
                       error_action='ignore',  # don't want to know if an order does not work
                       suppress_warnings=True,  # don't want convergence warnings
                       stepwise=False, random=True, random_state=42,  # we can fit a random search (not exhaustive)
                       n_fits=25)

pre4 = mod4.predict(n_periods = 5)

pre44 = pd.DataFrame(pre4, columns=['MONTO'])
pre44['Tiempo'] = ['2023-11', '2023-12', '2024-01', '2024-02', '2024-03']

df_figpp4 = df_figp4[['Tiempo', 'MONTO']]
df_figpp4 = pd.DataFrame(df_figpp4)

df_final_pro4 = pd.concat([df_figpp4, pre44])
#st.write(df_final_pro1)

fig_forecast_4 = px.line(df_final_pro4, x=df_final_pro4['Tiempo'],y=df_final_pro4['MONTO'],title='<b> Evolución del monto total en miles de soles de la categoria Pastas </b>',
              template='plotly_dark', markers=True)
fig_forecast_4.update_traces(line_color="firebrick")


left, right = st.columns(2)
left.plotly_chart(fig_forecast_3, use_container_width=True)
right.plotly_chart(fig_forecast_4, use_container_width=True)



#################################################################################################################################
#################################################################################################################################

st.markdown("### SUPESA", unsafe_allow_html=True)

## figp_1
df_figp1 = pro1[(pro1['Canal'] == 'SUPESA') & (pro1['des_categoria'] == 'Aceites')]

mod1 = pm.auto_arima(df_figp1['MONTO'], start_p=1, start_q=1, max_p=3, max_q=3, m=12,
                       start_P=0, seasonal=True, d=1, D=1, trace=True,
                       n_jobs=-1,  # We can run this in parallel by controlling this option
                       error_action='ignore',  # don't want to know if an order does not work
                       suppress_warnings=True,  # don't want convergence warnings
                       stepwise=False, random=True, random_state=42,  # we can fit a random search (not exhaustive)
                       n_fits=25)

pre1 = mod1.predict(n_periods = 5)

pre11 = pd.DataFrame(pre1, columns=['MONTO'])
pre11['Tiempo'] = ['2023-11', '2023-12', '2024-01', '2024-02', '2024-03']

df_figpp1 = df_figp1[['Tiempo', 'MONTO']]
df_figpp1 = pd.DataFrame(df_figpp1)

df_final_pro1 = pd.concat([df_figpp1, pre11])
#st.write(df_final_pro1)

fig_forecast_1 = px.line(df_final_pro1, x=df_final_pro1['Tiempo'],y=df_final_pro1['MONTO'],title='<b> Evolución del monto total en miles de soles de la categoria Aceites </b>',
              template='plotly_dark', markers=True)
fig_forecast_1.update_traces(line_color="#32CD32")


## figp_2
df_figp2 = pro1[(pro1['Canal'] == 'SUPESA') & (pro1['des_categoria'] == 'Detergentes')]

mod2 = pm.auto_arima(df_figp2['MONTO'], start_p=1, start_q=1, max_p=3, max_q=3, m=12,
                       start_P=0, seasonal=True, d=1, D=1, trace=True,
                       n_jobs=-1,  # We can run this in parallel by controlling this option
                       error_action='ignore',  # don't want to know if an order does not work
                       suppress_warnings=True,  # don't want convergence warnings
                       stepwise=False, random=True, random_state=42,  # we can fit a random search (not exhaustive)
                       n_fits=25)

pre2 = mod2.predict(n_periods = 5)

pre22 = pd.DataFrame(pre2, columns=['MONTO'])
pre22['Tiempo'] = ['2023-11', '2023-12', '2024-01', '2024-02', '2024-03']

df_figpp2 = df_figp2[['Tiempo', 'MONTO']]
df_figpp2 = pd.DataFrame(df_figpp2)

df_final_pro2 = pd.concat([df_figpp2, pre22])
#st.write(df_final_pro1)

fig_forecast_2 = px.line(df_final_pro2, x=df_final_pro2['Tiempo'],y=df_final_pro2['MONTO'],title='<b> Evolución del monto total en miles de soles de la categoria Detergentes </b>',
              template='plotly_dark', markers=True)
fig_forecast_2.update_traces(line_color="#32CD32")


left, right = st.columns(2)
left.plotly_chart(fig_forecast_1, use_container_width=True)
right.plotly_chart(fig_forecast_2, use_container_width=True)


########################################################################################

## figp_3
df_figp3 = pro1[(pro1['Canal'] == 'SUPESA') & (pro1['des_categoria'] == 'Salsas')]

mod3 = pm.auto_arima(df_figp3['MONTO'], start_p=1, start_q=1, max_p=3, max_q=3, m=12,
                       start_P=0, seasonal=True, d=1, D=1, trace=True,
                       n_jobs=-1,  # We can run this in parallel by controlling this option
                       error_action='ignore',  # don't want to know if an order does not work
                       suppress_warnings=True,  # don't want convergence warnings
                       stepwise=False, random=True, random_state=42,  # we can fit a random search (not exhaustive)
                       n_fits=25)

pre3 = mod3.predict(n_periods = 5)

pre33 = pd.DataFrame(pre3, columns=['MONTO'])
pre33['Tiempo'] = ['2023-11', '2023-12', '2024-01', '2024-02', '2024-03']

df_figpp3 = df_figp3[['Tiempo', 'MONTO']]
df_figpp3 = pd.DataFrame(df_figpp3)

df_final_pro3 = pd.concat([df_figpp3, pre33])
#st.write(df_final_pro1)

fig_forecast_3 = px.line(df_final_pro3, x=df_final_pro3['Tiempo'],y=df_final_pro3['MONTO'],title='<b> Evolución del monto total en miles de soles de la categoria Salsas </b>',
              template='plotly_dark', markers=True)
fig_forecast_3.update_traces(line_color="#32CD32")

## figp_4
df_figp4 = pro1[(pro1['Canal'] == 'SUPESA') & (pro1['des_categoria'] == 'Pastas')]

mod4 = pm.auto_arima(df_figp4['MONTO'], start_p=1, start_q=1, max_p=3, max_q=3, m=12,
                       start_P=0, seasonal=True, d=1, D=1, trace=True,
                       n_jobs=-1,  # We can run this in parallel by controlling this option
                       error_action='ignore',  # don't want to know if an order does not work
                       suppress_warnings=True,  # don't want convergence warnings
                       stepwise=False, random=True, random_state=42,  # we can fit a random search (not exhaustive)
                       n_fits=25)

pre4 = mod4.predict(n_periods = 5)

pre44 = pd.DataFrame(pre4, columns=['MONTO'])
pre44['Tiempo'] = ['2023-11', '2023-12', '2024-01', '2024-02', '2024-03']

df_figpp4 = df_figp4[['Tiempo', 'MONTO']]
df_figpp4 = pd.DataFrame(df_figpp4)

df_final_pro4 = pd.concat([df_figpp4, pre44])
#st.write(df_final_pro1)

fig_forecast_4 = px.line(df_final_pro4, x=df_final_pro4['Tiempo'],y=df_final_pro4['MONTO'],title='<b> Evolución del monto total en miles de soles de la categoria Pastas </b>',
              template='plotly_dark', markers=True)
fig_forecast_4.update_traces(line_color="#32CD32")


left, right = st.columns(2)
left.plotly_chart(fig_forecast_3, use_container_width=True)
right.plotly_chart(fig_forecast_4, use_container_width=True)


#################################################################################################################################
#################################################################################################################################

st.markdown("### TOTTUS", unsafe_allow_html=True)

## figp_1
df_figp1 = pro1[(pro1['Canal'] == 'TOTTUS') & (pro1['des_categoria'] == 'Aceites')]

mod1 = pm.auto_arima(df_figp1['MONTO'], start_p=1, start_q=1, max_p=3, max_q=3, m=12,
                       start_P=0, seasonal=True, d=1, D=1, trace=True,
                       n_jobs=-1,  # We can run this in parallel by controlling this option
                       error_action='ignore',  # don't want to know if an order does not work
                       suppress_warnings=True,  # don't want convergence warnings
                       stepwise=False, random=True, random_state=42,  # we can fit a random search (not exhaustive)
                       n_fits=25)

pre1 = mod1.predict(n_periods = 5)

pre11 = pd.DataFrame(pre1, columns=['MONTO'])
pre11['Tiempo'] = ['2023-11', '2023-12', '2024-01', '2024-02', '2024-03']

df_figpp1 = df_figp1[['Tiempo', 'MONTO']]
df_figpp1 = pd.DataFrame(df_figpp1)

df_final_pro1 = pd.concat([df_figpp1, pre11])
#st.write(df_final_pro1)

fig_forecast_1 = px.line(df_final_pro1, x=df_final_pro1['Tiempo'],y=df_final_pro1['MONTO'],title='<b> Evolución del monto total en miles de soles de la categoria Aceites </b>',
              template='plotly_dark', markers=True)
fig_forecast_1.update_traces(line_color="#8532cd")


## figp_2
df_figp2 = pro1[(pro1['Canal'] == 'TOTTUS') & (pro1['des_categoria'] == 'Detergentes')]

mod2 = pm.auto_arima(df_figp2['MONTO'], start_p=1, start_q=1, max_p=3, max_q=3, m=12,
                       start_P=0, seasonal=True, d=1, D=1, trace=True,
                       n_jobs=-1,  # We can run this in parallel by controlling this option
                       error_action='ignore',  # don't want to know if an order does not work
                       suppress_warnings=True,  # don't want convergence warnings
                       stepwise=False, random=True, random_state=42,  # we can fit a random search (not exhaustive)
                       n_fits=25)

pre2 = mod2.predict(n_periods = 5)

pre22 = pd.DataFrame(pre2, columns=['MONTO'])
pre22['Tiempo'] = ['2023-11', '2023-12', '2024-01', '2024-02', '2024-03']

df_figpp2 = df_figp2[['Tiempo', 'MONTO']]
df_figpp2 = pd.DataFrame(df_figpp2)

df_final_pro2 = pd.concat([df_figpp2, pre22])
#st.write(df_final_pro1)

fig_forecast_2 = px.line(df_final_pro2, x=df_final_pro2['Tiempo'],y=df_final_pro2['MONTO'],title='<b> Evolución del monto total en miles de soles de la categoria Detergentes </b>',
              template='plotly_dark', markers=True)
fig_forecast_2.update_traces(line_color="#8532cd")


left, right = st.columns(2)
left.plotly_chart(fig_forecast_1, use_container_width=True)
right.plotly_chart(fig_forecast_2, use_container_width=True)


########################################################################################

## figp_3
df_figp3 = pro1[(pro1['Canal'] == 'TOTTUS') & (pro1['des_categoria'] == 'Salsas')]

mod3 = pm.auto_arima(df_figp3['MONTO'], start_p=1, start_q=1, max_p=3, max_q=3, m=12,
                       start_P=0, seasonal=True, d=1, D=1, trace=True,
                       n_jobs=-1,  # We can run this in parallel by controlling this option
                       error_action='ignore',  # don't want to know if an order does not work
                       suppress_warnings=True,  # don't want convergence warnings
                       stepwise=False, random=True, random_state=42,  # we can fit a random search (not exhaustive)
                       n_fits=25)

pre3 = mod3.predict(n_periods = 5)

pre33 = pd.DataFrame(pre3, columns=['MONTO'])
pre33['Tiempo'] = ['2023-11', '2023-12', '2024-01', '2024-02', '2024-03']

df_figpp3 = df_figp3[['Tiempo', 'MONTO']]
df_figpp3 = pd.DataFrame(df_figpp3)

df_final_pro3 = pd.concat([df_figpp3, pre33])
#st.write(df_final_pro1)

fig_forecast_3 = px.line(df_final_pro3, x=df_final_pro3['Tiempo'],y=df_final_pro3['MONTO'],title='<b> Evolución del monto total en miles de soles de la categoria Salsas </b>',
              template='plotly_dark', markers=True)
fig_forecast_3.update_traces(line_color="#8532cd")

## figp_4
df_figp4 = pro1[(pro1['Canal'] == 'TOTTUS') & (pro1['des_categoria'] == 'Pastas')]

mod4 = pm.auto_arima(df_figp4['MONTO'], start_p=1, start_q=1, max_p=3, max_q=3, m=12,
                       start_P=0, seasonal=True, d=1, D=1, trace=True,
                       n_jobs=-1,  # We can run this in parallel by controlling this option
                       error_action='ignore',  # don't want to know if an order does not work
                       suppress_warnings=True,  # don't want convergence warnings
                       stepwise=False, random=True, random_state=42,  # we can fit a random search (not exhaustive)
                       n_fits=25)

pre4 = mod4.predict(n_periods = 5)

pre44 = pd.DataFrame(pre4, columns=['MONTO'])
pre44['Tiempo'] = ['2023-11', '2023-12', '2024-01', '2024-02', '2024-03']

df_figpp4 = df_figp4[['Tiempo', 'MONTO']]
df_figpp4 = pd.DataFrame(df_figpp4)

df_final_pro4 = pd.concat([df_figpp4, pre44])
#st.write(df_final_pro1)

fig_forecast_4 = px.line(df_final_pro4, x=df_final_pro4['Tiempo'],y=df_final_pro4['MONTO'],title='<b> Evolución del monto total en miles de soles de la categoria Pastas </b>',
              template='plotly_dark', markers=True)
fig_forecast_4.update_traces(line_color="#8532cd")


left, right = st.columns(2)
left.plotly_chart(fig_forecast_3, use_container_width=True)
right.plotly_chart(fig_forecast_4, use_container_width=True)



#################################################################################################################################
#################################################################################################################################

st.markdown("### RAPPI", unsafe_allow_html=True)

## figp_1
df_figp1 = pro1[(pro1['Canal'] == 'RAPPI') & (pro1['des_categoria'] == 'Aceites')]

mod1 = pm.auto_arima(df_figp1['MONTO'], start_p=1, start_q=1, max_p=3, max_q=3, m=12,
                       start_P=0, seasonal=True, d=1, D=1, trace=True,
                       n_jobs=-1,  # We can run this in parallel by controlling this option
                       error_action='ignore',  # don't want to know if an order does not work
                       suppress_warnings=True,  # don't want convergence warnings
                       stepwise=False, random=True, random_state=42,  # we can fit a random search (not exhaustive)
                       n_fits=25)

pre1 = mod1.predict(n_periods = 5)

pre11 = pd.DataFrame(pre1, columns=['MONTO'])
pre11['Tiempo'] = ['2023-11', '2023-12', '2024-01', '2024-02', '2024-03']

df_figpp1 = df_figp1[['Tiempo', 'MONTO']]
df_figpp1 = pd.DataFrame(df_figpp1)

df_final_pro1 = pd.concat([df_figpp1, pre11])
#st.write(df_final_pro1)

fig_forecast_1 = px.line(df_final_pro1, x=df_final_pro1['Tiempo'],y=df_final_pro1['MONTO'],title='<b> Evolución del monto total en miles de soles de la categoria Aceites </b>',
              template='plotly_dark', markers=True)
fig_forecast_1.update_traces(line_color="#cd8a32")


## figp_2
df_figp2 = pro1[(pro1['Canal'] == 'RAPPI') & (pro1['des_categoria'] == 'Detergentes')]

mod2 = pm.auto_arima(df_figp2['MONTO'], start_p=1, start_q=1, max_p=3, max_q=3, m=12,
                       start_P=0, seasonal=True, d=1, D=1, trace=True,
                       n_jobs=-1,  # We can run this in parallel by controlling this option
                       error_action='ignore',  # don't want to know if an order does not work
                       suppress_warnings=True,  # don't want convergence warnings
                       stepwise=False, random=True, random_state=42,  # we can fit a random search (not exhaustive)
                       n_fits=25)

pre2 = mod2.predict(n_periods = 5)

pre22 = pd.DataFrame(pre2, columns=['MONTO'])
pre22['Tiempo'] = ['2023-11', '2023-12', '2024-01', '2024-02', '2024-03']

df_figpp2 = df_figp2[['Tiempo', 'MONTO']]
df_figpp2 = pd.DataFrame(df_figpp2)

df_final_pro2 = pd.concat([df_figpp2, pre22])
#st.write(df_final_pro1)

fig_forecast_2 = px.line(df_final_pro2, x=df_final_pro2['Tiempo'],y=df_final_pro2['MONTO'],title='<b> Evolución del monto total en miles de soles de la categoria Detergentes </b>',
              template='plotly_dark', markers=True)
fig_forecast_2.update_traces(line_color="#cd8a32")


left, right = st.columns(2)
left.plotly_chart(fig_forecast_1, use_container_width=True)
right.plotly_chart(fig_forecast_2, use_container_width=True)


########################################################################################

## figp_3
df_figp3 = pro1[(pro1['Canal'] == 'RAPPI') & (pro1['des_categoria'] == 'Salsas')]

mod3 = pm.auto_arima(df_figp3['MONTO'], start_p=1, start_q=1, max_p=3, max_q=3, m=12,
                       start_P=0, seasonal=True, d=1, D=1, trace=True,
                       n_jobs=-1,  # We can run this in parallel by controlling this option
                       error_action='ignore',  # don't want to know if an order does not work
                       suppress_warnings=True,  # don't want convergence warnings
                       stepwise=False, random=True, random_state=42,  # we can fit a random search (not exhaustive)
                       n_fits=25)

pre3 = mod3.predict(n_periods = 5)

pre33 = pd.DataFrame(pre3, columns=['MONTO'])
pre33['Tiempo'] = ['2023-11', '2023-12', '2024-01', '2024-02', '2024-03']

df_figpp3 = df_figp3[['Tiempo', 'MONTO']]
df_figpp3 = pd.DataFrame(df_figpp3)

df_final_pro3 = pd.concat([df_figpp3, pre33])
#st.write(df_final_pro1)

fig_forecast_3 = px.line(df_final_pro3, x=df_final_pro3['Tiempo'],y=df_final_pro3['MONTO'],title='<b> Evolución del monto total en miles de soles de la categoria Salsas </b>',
              template='plotly_dark', markers=True)
fig_forecast_3.update_traces(line_color="#cd8a32")

## figp_4
df_figp4 = pro1[(pro1['Canal'] == 'RAPPI') & (pro1['des_categoria'] == 'Pastas')]

mod4 = pm.auto_arima(df_figp4['MONTO'], start_p=1, start_q=1, max_p=3, max_q=3, m=12,
                       start_P=0, seasonal=True, d=1, D=1, trace=True,
                       n_jobs=-1,  # We can run this in parallel by controlling this option
                       error_action='ignore',  # don't want to know if an order does not work
                       suppress_warnings=True,  # don't want convergence warnings
                       stepwise=False, random=True, random_state=42,  # we can fit a random search (not exhaustive)
                       n_fits=25)

pre4 = mod4.predict(n_periods = 5)

pre44 = pd.DataFrame(pre4, columns=['MONTO'])
pre44['Tiempo'] = ['2023-11', '2023-12', '2024-01', '2024-02', '2024-03']

df_figpp4 = df_figp4[['Tiempo', 'MONTO']]
df_figpp4 = pd.DataFrame(df_figpp4)

df_final_pro4 = pd.concat([df_figpp4, pre44])
#st.write(df_final_pro1)

fig_forecast_4 = px.line(df_final_pro4, x=df_final_pro4['Tiempo'],y=df_final_pro4['MONTO'],title='<b> Evolución del monto total en miles de soles de la categoria Pastas </b>',
              template='plotly_dark', markers=True)
fig_forecast_4.update_traces(line_color="#cd8a32")


left, right = st.columns(2)
left.plotly_chart(fig_forecast_3, use_container_width=True)
right.plotly_chart(fig_forecast_4, use_container_width=True)

















