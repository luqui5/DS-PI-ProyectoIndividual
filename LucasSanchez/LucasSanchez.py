import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib import rcParams
from PIL import Image
import datetime as dt
from dateutil.relativedelta import relativedelta 
import plotly.express as px
"# Lucas Nicolas Sanchez"

"Esta presentacion se basara sobre los datos del COVID-19 en EE.UU"



"## ¿Que es el COVID-19? "
st.write("COVID-19 es una enfermedad contagiosa causada por el virus SARS-CoV-2. Se cree que la transmision se produce por contacto directo o indirecto con 'gotitas' generadas de la via aerea de pacientes infectados (via 'gotitas' y via contacto directo) y las secreciones respiratorias. El periodo de incubacion promedio es de 6 dias (6.4 para ser exacto), variando entre 2-14 dias")
df_orig = pd.read_csv("COVID-19_Reported_Patient_Impact_and_Hospital_Capacity_by_State_Timeseries.csv")
df_orig['date'] = pd.to_datetime(df_orig['date'],format='%Y-%m-%d') 


"## ¿Cuáles fueron los 5 Estados con mayor ocupación hospitalaria por COVID? (en los primeros 6 meses del 2020)"

punto1= st.container()
with punto1:
    st.markdown("Nueva York con **687.963**")
    st.markdown("California con **441.543**")
    st.markdown("Florida con **329.651**")
    st.markdown("Texas con **253.496**")
    st.markdown("Illinois con **215.590**")

    #variable = df_orig[['state','date','inpatient_beds']]
    
    df_pto1 = df_orig[['state','date','inpatient_beds_used_covid']]
    df_pto1['date'] = pd.to_datetime(df_pto1['date']) 

    mask = (df_pto1['date'] >='2020-01-01') & (df_pto1['date'] <= '2020-07-01')
    filtro_df_pto1 = df_pto1.loc[mask]
    top5mayorocup = filtro_df_pto1
    top5mayorocup['Pacientes en cama con COVID'] = top5mayorocup['inpatient_beds_used_covid']
    top5mayorocup.drop(['inpatient_beds_used_covid'],axis=1,inplace=True)
    
    #variable = variable.groupby(by='state').sum().reset_index().sort_values('inpatient_beds',ascending=False)

    #variable #PARA RESPONDER EL DOC


    valormes = st.slider('Seleccione el mes (0 para mostrar top 5 en los 6 meses)',0, 6)
    
    
    if valormes==0:
        top5mayorocup = filtro_df_pto1.groupby(['state']).sum().sort_values(['Pacientes en cama con COVID'],ascending=False).reset_index().head(5)
        dashfig01=px.choropleth(top5mayorocup,locations=top5mayorocup['state'],locationmode='USA-states',scope='usa',color=top5mayorocup['Pacientes en cama con COVID'],color_continuous_scale=px.colors.sequential.matter,labels={'locations':'Estado','color':'Camas Ocupadas'})
        dashfig01.update_layout(title_text='Camas ocupadas por Estado',geo_scope='usa')
        st.write(dashfig01)
    else:
        for i in range(1,7):
                if i == valormes:
                    top5mayorocup['mes'] = top5mayorocup['date'].dt.month
                    top5mayorocup = top5mayorocup.groupby(['state','mes']).sum().reset_index()
                    top5mayorocup = top5mayorocup[top5mayorocup['mes'] == i]
                    
                    dashfig02=px.choropleth(top5mayorocup,locations=top5mayorocup['state'],locationmode='USA-states',scope='usa',color=top5mayorocup['Pacientes en cama con COVID'],color_continuous_scale=px.colors.sequential.matter,labels={'locations':'Estado','color':'Camas Ocupadas'})
                    dashfig02.update_layout(title_text='Camas ocupadas por Estado',geo_scope='usa')
                    st.write(dashfig02)



"## Puntos criticos (Maximos y minimos) en el estado de Nueva York"



'El dia donde mas hay pacientes en cama con COVID fue el dia: **2020-04-14** con un total de pacientes de: **14.126**'

'El dia donde menos pacientes en cama con COVID fue el dia:  **2020-03-14** con un total de pacientes de: **6**'

"## Intervalos de crecimiento y decrecimiento en el estado de Nueva York"

punto2 = st.container()
with punto2:
    cols1,_ = st.columns((1,1)) 
    cols2,_ = st.columns((1,1)) 

    format = 'MMM DD, YYYY' 
    start_date = dt.date(year=2020,month=1,day=1)
    end_date = dt.date(year=2022, month=8, day=4)
    end_date1= dt.date(year=2022, month=8, day=3)
    max_days = end_date-start_date

    slider = cols1.slider('Elige una Fecha inicial', min_value=start_date, value=end_date1 ,max_value=end_date1, format=format)

    fecha= str(slider)

    slider2 = cols2.slider('Elige una Fecha', min_value=slider, value=end_date ,max_value=end_date, format=format)

    fecha2 = str(slider2)

    df_orig = pd.read_csv("G:\Practica HENRY\Labs\PI2\DS-PI-ProyectoIndividual-main\COVID-19_Reported_Patient_Impact_and_Hospital_Capacity_by_State_Timeseries.csv")
    df_orig['date'] = pd.to_datetime(df_orig['date']) 
    df_pto2 = df_orig[df_orig['state'] == 'NY']

    df_pto2=df_pto2[(df_pto2['date'] >= fecha) & (df_pto2['date'] <= fecha2)]
    fig = plt.figure()  
    g = sns.lineplot(df_pto2['date'], df_pto2['inpatient_beds_used_covid'])
    g.set_xlabel("FECHA",fontsize=20,color='black')
    g.set_ylabel("Pacientes en cama con COVID",fontsize=20,color='black')
    rcParams['figure.figsize'] = 20,15
    st.pyplot(fig)



"## ¿Cuáles fueron los cinco Estados que más camas UCI -Unidades de Cuidados Intensivos- utilizaron durante el año 2020? (absoluto)"

st.markdown("Texas con **991.193** en el 2020")
st.markdown("California con **901.654** en el 2020")
st.markdown("Florida con **799.385.** en el 2020")
st.markdown("Nueva York con **495.350** en el 2020")
st.markdown("Pennsylvania con **465.537** en el 2020")




"## ¿Qué cantidad de camas se utilizaron, por Estado, para pacientes pediátricos con COVID durante el 2020?"
punto4= st.container()
with punto4:
    mask = (df_orig['date'] >='2020-01-01') & (df_orig['date'] <= '2020-12-31')
    filtro_df_pto4 = df_orig.loc[mask]
    filtro_df_pto4 = filtro_df_pto4[['state','date','all_pediatric_inpatient_bed_occupied']]
    var = filtro_df_pto4.groupby(['state']).sum()
    var['Pacientes pediatricos en cama'] = var['all_pediatric_inpatient_bed_occupied']
    var.drop(['all_pediatric_inpatient_bed_occupied'],axis=1,inplace=True)
    var = var.sort_values('Pacientes pediatricos en cama',ascending=False)
    listaestado = []
    for i in filtro_df_pto4['state']:
        if i not in listaestado:
            listaestado.append(i)
    opcion = st.selectbox('Selecciona un Estado',listaestado)

    for j in range(len(var)):
        if var.iloc[j].name == opcion:
            cant = var['Pacientes pediatricos en cama'][j]

    st.write('Pacientes pediatricos en cama:', int(cant))

    st.write('TOP 5 estados con mas pacientes pediatricos')
    st.write(var.head(5))

    prueba = st.checkbox('Tabla general pacientes pediatricos en cama')
    if prueba:
        st.write(var)

"## ¿Qué porcentaje de camas UCI corresponden a casos confirmados de COVID-19? Por Estado."
punto5 = st.container()
with punto5:
    filtro_df_pto5 = df_orig[['state','date','staffed_adult_icu_bed_occupancy','staffed_icu_adult_patients_confirmed_covid']]
    filtro_df_pto5['Totales camas UCI  ocupadas'] = filtro_df_pto5['staffed_adult_icu_bed_occupancy']
    filtro_df_pto5['Ocupadas camas UCI  por pacientes confirmados'] = filtro_df_pto5['staffed_icu_adult_patients_confirmed_covid']
    filtro_df_pto5.drop(['staffed_adult_icu_bed_occupancy'],axis=1,inplace=True)
    filtro_df_pto5.drop(['staffed_icu_adult_patients_confirmed_covid'],axis=1,inplace=True)
    filtro_df_pto5['porcentaje'] = filtro_df_pto5['Ocupadas camas UCI  por pacientes confirmados']/filtro_df_pto5['Totales camas UCI  ocupadas'] * 100
    filtro_df_pto5 = filtro_df_pto5.groupby(['state']).mean()
    filtro_df_pto5 = filtro_df_pto5.sort_values(['porcentaje'],ascending=False)
    filtro_df_pto5.dropna(inplace=True)

    st.write(filtro_df_pto5)

    "## ¿Cuántas muertes por covid hubo, por Estado, durante el año 2021?"
    
    punto6= st.container()
    
    with punto6:
        listaaño = ['Seleccione un Año',2020,2021,2022]
        opcion = st.selectbox('Selecciona un Año',listaaño)
        if opcion==2020:
            mask = (df_orig['date'] >='2020-01-01') & (df_orig['date'] <= '2020-12-31')
            filtro_df_pto6 = df_orig.loc[mask]
            filtro_df_pto6 = filtro_df_pto6[['state','date','deaths_covid']]
            filtro_df_pto6['Muertos por COVID'] = filtro_df_pto6['deaths_covid']
            filtro_df_pto6.drop(['deaths_covid'],axis=1,inplace=True)
            muertes_covid = filtro_df_pto6.groupby(['state']).sum()
            muertes_covid = muertes_covid.sort_values(['Muertos por COVID'],ascending=False)
            
            st.write(muertes_covid)
            
        if opcion == 2021:
            mask = (df_orig['date'] >='2021-01-01') & (df_orig['date'] <= '2021-12-31')
            filtro_df_pto6 = df_orig.loc[mask]
            filtro_df_pto6 = filtro_df_pto6[['state','date','deaths_covid']]
            filtro_df_pto6['Muertos por COVID'] = filtro_df_pto6['deaths_covid']
            filtro_df_pto6.drop(['deaths_covid'],axis=1,inplace=True)
            muertes_covid = filtro_df_pto6.groupby(['state']).sum()
            muertes_covid = muertes_covid.sort_values(['Muertos por COVID'],ascending=False)
            
            st.write(muertes_covid)
        
        if opcion == 2022:
            mask = (df_orig['date'] >='2022-01-01') & (df_orig['date'] <= '2022-12-31')
            filtro_df_pto6 = df_orig.loc[mask]
            filtro_df_pto6 = filtro_df_pto6[['state','date','deaths_covid']]
            filtro_df_pto6['Muertos por COVID'] = filtro_df_pto6['deaths_covid']
            filtro_df_pto6.drop(['deaths_covid'],axis=1,inplace=True)
            muertes_covid = filtro_df_pto6.groupby(['state']).sum()
            muertes_covid = muertes_covid.sort_values(['Muertos por COVID'],ascending=False)

            st.write(muertes_covid)
        else: pass
"## ¿Qué relación presenta la falta de personal médico, con la cantidad de muertes por covid durante el año 2021?"

punto7= st.container()
with punto7:
    from PIL import Image
    image = Image.open('imagen.png')

    st.image(image, caption='Maximo muertes en 1 dia por MES')


"## Siguiendo las respuestas anteriores, ¿cuál fue el peor mes de la pandemia para USA en su conjunto? Puede utilizar otras medidas que considere necesarias."
punto8= st.container()
with punto8:
    filtro_df_pto8 = df_orig[['state','date','deaths_covid']]
    filtro_dfmapa_pto8 = filtro_df_pto8
    filtro_df_pto8['mes'] = filtro_df_pto8['date'].dt.month
    filtro_df_pto8 = filtro_df_pto8.groupby(['mes']).sum().sort_values('deaths_covid',ascending=False)
    "Aca podemos ver que cantidad de muertes hubieron en total por mes en los EE.UU (sumando todos los eneros, todos los febreros, y asi)"
    "Y como podemos observar, el mes con un pico de muertes fue ENERO, sobrepasando por casi 19 Millones al mes que le sigue"

    filtro_df_pto8['Muertos por COVID'] = filtro_df_pto8['deaths_covid']
    filtro_df_pto8.drop(['deaths_covid'],axis=1,inplace=True)
    st.write(filtro_df_pto8)
    
    filtro_dfmapa_pto8 = filtro_dfmapa_pto8.groupby(['state']).sum().reset_index()
    filtro_dfmapa_pto8.drop(['mes'],axis=1,inplace=True)
    
    dashfig=px.choropleth(filtro_dfmapa_pto8,locations=filtro_dfmapa_pto8['state'],locationmode='USA-states',scope='usa',color=filtro_dfmapa_pto8['deaths_covid'],color_continuous_scale='Reds',labels={'locations':'Estado','color':'Fallecidos'})
    dashfig.update_layout(title_text='Fallecidos por estado en toda la pandemia',geo_scope='usa')
    st.write(dashfig)

    
punto9= st.container()
with punto9:
    st.write("## ¿Qué recomendaciones haría, ex post, con respecto a los recursos hospitalarios y su uso?")
    st.write("Yo recomendaria lo siguiente:")

    st.write("Sobre la infraestructura de los hospitales, evaluar bien el flujo de atencion que se les brinda a los pacientes sanos, adecuar las salas para evitar 'amontonamiento' de personas que concurran al hospital.")

    st.write("Con respecto a las salas, verificar que se tenga una buena ventilacion (ej: puerta cerrada pero con ventana abierta hacia el exterior)")
    st.write("Tener en cuenta los espacios/salas que se van a utilizar para el aislamiento.")

    st.write("Capacitar al equipo de salud (ya sea con medidas de prevencion, brindarle informacion sobre el VIRUS, ayuda psicologica hacia los pacientes)")

    st.write("Brindar informacion publica, medidas de prevencion, horarios de los medicos, lugares de vacunacion hacia la comunidad")

st.write('## Mapa de EE.UU // Camas ocupadas por estado')
df = df_orig[['state','inpatient_beds_used_covid']]
df['Pacientes con covid en cama'] = df['inpatient_beds_used_covid']
df['Estado'] = df['state']
df.drop(['state'],axis=1,inplace=True)
df.drop(['inpatient_beds_used_covid'],axis=1,inplace=True)

camasocupadas= st.container()

with camasocupadas:
    añosopcion = ['Seleccione un año',2020,2021,2022]
    opcion2 = st.selectbox('Selecciona un año', añosopcion)
    if opcion2==2020:
        mask = (df_orig['date'] >='2020-01-01') & (df_orig['date'] <= '2020-12-31')
        filtro_df_pto9 = df_orig.loc[mask]
        filtro_df_pto9 = filtro_df_pto9[['state','date','inpatient_beds_used']]
        filtro_df_pto9['Camas ocupadas'] = filtro_df_pto9['inpatient_beds_used']
        filtro_df_pto9.drop(['inpatient_beds_used'],axis=1,inplace=True)
        values = st.slider('Seleccione el mes (0 para mostrar todo el AÑO)',0, 12)
        
        if values==0:
            filtro_df_pto9 = filtro_df_pto9.groupby(['state']).sum().reset_index()
            
            dashfig2=px.choropleth(filtro_df_pto9,locations=filtro_df_pto9['state'],locationmode='USA-states',scope='usa',color=filtro_df_pto9['Camas ocupadas'],color_continuous_scale=px.colors.sequential.matter,labels={'locations':'Estado','color':'Camas Ocupadas'})
            dashfig2.update_layout(title_text='Camas ocupadas por Estado',geo_scope='usa')
            st.write(dashfig2)

        else:
            for i in range(1,13):
                if i == values:
                    filtro_df_pto9['mes'] = filtro_df_pto9['date'].dt.month
                    filtro_df_pto9 = filtro_df_pto9.groupby(['state','mes']).sum().reset_index()
                    filtro_df_pto9 = filtro_df_pto9[filtro_df_pto9['mes'] == i]
                    
                    dashfig2=px.choropleth(filtro_df_pto9,locations=filtro_df_pto9['state'],locationmode='USA-states',scope='usa',color=filtro_df_pto9['Camas ocupadas'],color_continuous_scale=px.colors.sequential.matter,labels={'locations':'Estado','color':'Camas Ocupadas'})
                    dashfig2.update_layout(title_text='Camas ocupadas por Estado',geo_scope='usa')
                    st.write(dashfig2)
        
    if opcion2 == 2021:
        mask = (df_orig['date'] >='2021-01-01') & (df_orig['date'] <= '2021-12-31')
        filtro_df_pto9 = df_orig.loc[mask]
        filtro_df_pto9 = filtro_df_pto9[['state','date','inpatient_beds_used']]
        filtro_df_pto9['Camas ocupadas'] = filtro_df_pto9['inpatient_beds_used']
        filtro_df_pto9.drop(['inpatient_beds_used'],axis=1,inplace=True)
        values = st.slider('Seleccione el mes (0 para mostrar todo el AÑO)',0, 12)
        
        if values==0:
            filtro_df_pto9 = filtro_df_pto9.groupby(['state']).sum().reset_index()
            
            dashfig2=px.choropleth(filtro_df_pto9,locations=filtro_df_pto9['state'],locationmode='USA-states',scope='usa',color=filtro_df_pto9['Camas ocupadas'],color_continuous_scale=px.colors.sequential.matter,labels={'locations':'Estado','color':'Camas Ocupadas'})
            dashfig2.update_layout(title_text='Camas ocupadas por Estado',geo_scope='usa')
            st.write(dashfig2)

        else:
            for i in range(1,13):
                if i == values:
                    filtro_df_pto9['mes'] = filtro_df_pto9['date'].dt.month
                    filtro_df_pto9 = filtro_df_pto9.groupby(['state','mes']).sum().reset_index()
                    filtro_df_pto9 = filtro_df_pto9[filtro_df_pto9['mes'] == i]
                    
                    dashfig3=px.choropleth(filtro_df_pto9,locations=filtro_df_pto9['state'],locationmode='USA-states',scope='usa',color=filtro_df_pto9['Camas ocupadas'],color_continuous_scale=px.colors.sequential.matter,labels={'locations':'Estado','color':'Camas Ocupadas'})
                    dashfig3.update_layout(title_text='Camas ocupadas por Estado',geo_scope='usa')
                    st.write(dashfig3)
        
    if opcion2 == 2022:
        mask = (df_orig['date'] >='2022-01-01') & (df_orig['date'] <= '2022-12-31')
        filtro_df_pto9 = df_orig.loc[mask]
        filtro_df_pto9 = filtro_df_pto9[['state','date','inpatient_beds_used']]
        filtro_df_pto9['Camas ocupadas'] = filtro_df_pto9['inpatient_beds_used']
        filtro_df_pto9.drop(['inpatient_beds_used'],axis=1,inplace=True)
        values = st.slider('Seleccione el mes (0 para mostrar todo el AÑO)',0, 12)
        
        if values==0:
            filtro_df_pto9 = filtro_df_pto9.groupby(['state']).sum().reset_index()
            
            dashfig2=px.choropleth(filtro_df_pto9,locations=filtro_df_pto9['state'],locationmode='USA-states',scope='usa',color=filtro_df_pto9['Camas ocupadas'],color_continuous_scale=px.colors.sequential.matter,labels={'locations':'Estado','color':'Camas Ocupadas'})
            dashfig2.update_layout(title_text='Camas ocupadas por Estado',geo_scope='usa')
            st.write(dashfig2)

        else:
            for i in range(1,13):
                if i == values:
                    filtro_df_pto9['mes'] = filtro_df_pto9['date'].dt.month
                    filtro_df_pto9 = filtro_df_pto9.groupby(['state','mes']).sum().reset_index()
                    filtro_df_pto9 = filtro_df_pto9[filtro_df_pto9['mes'] == i]
                    
                    dashfig4=px.choropleth(filtro_df_pto9,locations=filtro_df_pto9['state'],locationmode='USA-states',scope='usa',color=filtro_df_pto9['Camas ocupadas'],color_continuous_scale=px.colors.sequential.matter,labels={'locations':'Estado','color':'Camas Ocupadas'})
                    dashfig4.update_layout(title_text='Camas ocupadas por Estado',geo_scope='usa')
                    st.write(dashfig4)
    else: pass


     





