import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from datetime import datetime
import pmdarima as pm



st.set_page_config(layout='wide', initial_sidebar_state='expanded')

@st.cache_data
def load_data(file_path):
    df = pd.read_excel(file_path)  # Assuming it's an Excel file
    return df

# Update the file path to the location on your computer
file_path = 'data/DF_dashboard2.xlsx'
data = load_data(file_path)

st.button("Rerun")

st.title('Dashboard actualizado al 17/12/2023')
st.markdown("## Información descriptiva de las ventas en monto y unidades", unsafe_allow_html=True)

st.sidebar.image('data/logo.png', caption='Consultora de innovación y transformación digital apalancada en diseño, tecnología y emprendimiento')
st.sidebar.header('Zona de filtrado')
canal = st.sidebar.multiselect('Selecciona el canal',
                               options=data['Canal'].unique(),
                               default=data['Canal'].unique())

plataforma = st.sidebar.multiselect('Selecciona la plataforma',
                               options=data['des_plataforma'].unique(),
                               default=data['des_plataforma'].unique())

subplataforma = st.sidebar.multiselect('Selecciona la subplataforma',
                               options=data['des_subplataforma'].unique(),
                               default=data['des_subplataforma'].unique())

medio1 = st.sidebar.multiselect('Selecciona el medio de CENCOSUD',
                                options=data[data['Canal']=='CENCOSUD']['Medio'].unique(),
                                default=data[data['Canal']=='CENCOSUD']['Medio'].unique())

medio2 = st.sidebar.multiselect('Selecciona el medio de SUPESA',
                                options=data[data['Canal']=='SUPESA']['Medio'].unique(),
                                default=data[data['Canal']=='SUPESA']['Medio'].unique())

medio3 = st.sidebar.multiselect('Selecciona el medio de TOTTUS',
                                options=data[data['Canal']=='TOTTUS']['Medio'].unique(),
                                default=data[data['Canal']=='TOTTUS']['Medio'].unique())

medio4 = st.sidebar.multiselect('Selecciona el medio de TOTTUS',
                                options=data[data['Canal']=='RAPPI']['Medio'].unique(),
                                default=data[data['Canal']=='RAPPI']['Medio'].unique())

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


nose = np.datetime64(date1)
nose2 =np.datetime64(date2)
#date1_1 = convert(date1)
#date2_1 = convert(date2)


#df_select = data.query('Canal == @canal & Medio == @medio & des_plataforma == @plataforma & des_subplataforma == @subplataforma & des_marca == @marca')
#df_select = data.query('Canal == @canal & Medio == @medio & des_plataforma == @plataforma & des_subplataforma == @subplataforma & des_marca == @marca & @date1 <= Fecha <= @date2')
df_select = data.query('Canal == @canal  & des_plataforma == @plataforma & des_subplataforma == @subplataforma & des_marca == @marca & (Medio == @medio1 | Medio == @medio2 | Medio == @medio3 | Medio == @medio4)')
df_select = df_select[(df_select['Fecha'] >= nose) & (df_select['Fecha'] <= nose2)]


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
dfig1 = df_select.groupby('Fecha')['MONTO'].sum().reset_index()
fig1 = px.line(dfig1, x=dfig1['Fecha'],y=dfig1['MONTO'],title='<b> Evolución del monto total en millones de soles </b>',
               template='plotly_dark')
#st.plotly_chart(fig1)

#Grafico dos
dfig2 = df_select.groupby('Fecha')['UND'].sum().reset_index()
fig2 = px.line(dfig2, x=dfig2['Fecha'],y=dfig2['UND'], title='<b> Evolución las unidades vendidas totales en millones </b>',
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


#SUPESA
#Categorias más importantes por canal
#c1_df = df_select[df_select['Canal']=='SUPESA'].groupby('des_categoria')['MONTO'].sum().reset_index()
#st.write(c1_df)
#Aceites, Detergentes, Salsas, Pastas y Conservas

st.header('Principales categorías - SUPESA')
listax = ['Aceites', 'Detergentes', 'Salsas', 'Pastas', 'Conservas']   
d1_df = df_select[(df_select['Canal'] == 'SUPESA') & (df_select['des_categoria'].isin(listax))].groupby(['des_categoria', 'Fecha'])['MONTO'].sum().reset_index()
d1_dfw = d1_df.pivot(index='Fecha', columns='des_categoria', values='MONTO')

figu = px.line(d1_dfw, x = d1_dfw.index, y=d1_dfw.columns, labels={'value':'Valor', 'variable':'Serie'}, line_shape='linear',
               title='Evolución en unidades monetarias')
st.plotly_chart(figu)

listax = ['Aceites', 'Detergentes', 'Salsas', 'Pastas', 'Conservas']   
d1_df = df_select[(df_select['Canal'] == 'SUPESA') & (df_select['des_categoria'].isin(listax))].groupby(['des_categoria', 'Fecha'])['UND'].sum().reset_index()
d1_dfw = d1_df.pivot(index='Fecha', columns='des_categoria', values='UND')

figu = px.line(d1_dfw, x = d1_dfw.index, y=d1_dfw.columns, labels={'value':'Valor', 'variable':'Serie'}, line_shape='linear',
               title='Evolución en unidades físicas vendidas')
st.plotly_chart(figu)

#TOTTUS
#Categorias más importantes por canal
#c1_df = df_select[df_select['Canal']=='TOTTUS'].groupby('des_categoria')['MONTO'].sum().reset_index()
#st.write(c1_df)
#Detergentes, Aceites, Salsas, Pastas, Galletas

st.header('Principales categorías - TOTTUS')
listax = ['Aceites', 'Detergentes', 'Salsas', 'Pastas', 'Galletas']   
d1_df = df_select[(df_select['Canal'] == 'TOTTUS') & (df_select['des_categoria'].isin(listax))].groupby(['des_categoria', 'Fecha'])['MONTO'].sum().reset_index()
d1_dfw = d1_df.pivot(index='Fecha', columns='des_categoria', values='MONTO')

figu = px.line(d1_dfw, x = d1_dfw.index, y=d1_dfw.columns, labels={'value':'Valor', 'variable':'Serie'}, line_shape='linear',
               title='Evolución en unidades monetarias')
st.plotly_chart(figu)
  
d1_df = df_select[(df_select['Canal'] == 'TOTTUS') & (df_select['des_categoria'].isin(listax))].groupby(['des_categoria', 'Fecha'])['UND'].sum().reset_index()
d1_dfw = d1_df.pivot(index='Fecha', columns='des_categoria', values='UND')

figu = px.line(d1_dfw, x = d1_dfw.index, y=d1_dfw.columns, labels={'value':'Valor', 'variable':'Serie'}, line_shape='linear',
               title='Evolución en unidades físicas vendidas')
st.plotly_chart(figu)

#CENCOSUD
#Categorias más importantes por canal
#c1_df = df_select[df_select['Canal']=='CENCOSUD'].groupby('des_categoria')['MONTO'].sum().reset_index()
#st.write(c1_df)
#Aceites, Detergentes, Salsas, Pastas, Conservas

st.header('Principales categorías - CENCOSUD')
listax = ['Aceites', 'Detergentes', 'Salsas', 'Pastas', 'Conservas']   
d1_df = df_select[(df_select['Canal'] == 'CENCOSUD') & (df_select['des_categoria'].isin(listax))].groupby(['des_categoria', 'Fecha'])['MONTO'].sum().reset_index()
d1_dfw = d1_df.pivot(index='Fecha', columns='des_categoria', values='MONTO')

figu = px.line(d1_dfw, x = d1_dfw.index, y=d1_dfw.columns, labels={'value':'Valor', 'variable':'Serie'}, line_shape='linear',
               title='Evolución en unidades monetarias')
st.plotly_chart(figu)
  
d1_df = df_select[(df_select['Canal'] == 'CENCOSUD') & (df_select['des_categoria'].isin(listax))].groupby(['des_categoria', 'Fecha'])['UND'].sum().reset_index()
d1_dfw = d1_df.pivot(index='Fecha', columns='des_categoria', values='UND')

figu = px.line(d1_dfw, x = d1_dfw.index, y=d1_dfw.columns, labels={'value':'Valor', 'variable':'Serie'}, line_shape='linear',
               title='Evolución en unidades físicas vendidas')
st.plotly_chart(figu)

#RAPPI
#Categorias más importantes por canal
#c1_df = df_select[df_select['Canal']=='RAPPI'].groupby('des_categoria')['MONTO'].sum().reset_index()
#st.write(c1_df)
#Salsas, Detergentes, Aceites, Galletas, Conservas

st.header('Principales categorías - RAPPI')
listax = ['Aceites', 'Detergentes', 'Salsas', 'Galletas', 'Conservas']   
d1_df = df_select[(df_select['Canal'] == 'RAPPI') & (df_select['des_categoria'].isin(listax))].groupby(['des_categoria', 'Fecha'])['MONTO'].sum().reset_index()
d1_dfw = d1_df.pivot(index='Fecha', columns='des_categoria', values='MONTO')

figu = px.line(d1_dfw, x = d1_dfw.index, y=d1_dfw.columns, labels={'value':'Valor', 'variable':'Serie'}, line_shape='linear',
               title='Evolución en unidades monetarias')
st.plotly_chart(figu)
  
d1_df = df_select[(df_select['Canal'] == 'RAPPI') & (df_select['des_categoria'].isin(listax))].groupby(['des_categoria', 'Fecha'])['UND'].sum().reset_index()
d1_dfw = d1_df.pivot(index='Fecha', columns='des_categoria', values='UND')

figu = px.line(d1_dfw, x = d1_dfw.index, y=d1_dfw.columns, labels={'value':'Valor', 'variable':'Serie'}, line_shape='linear',
               title='Evolución en unidades físicas vendidas')
st.plotly_chart(figu)






