#!/usr/bin/env python
# coding: utf-8

# ### Packages importeren

# In[24]:


import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from streamlit_folium import folium_static
import folium
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score


# ### Data inladen

# In[36]:


income = pd.read_csv("income.csv", encoding='latin-1')
unemployment = pd.read_csv("unemployment.csv")
poverty = pd.read_csv("poverty_level_wages.csv")
cost = pd.read_csv("cost_of_living_us.csv")
df_staat = pd.read_csv('us_state_cost.csv')
population = pd.read_csv('acs2015_census_tract_data.csv')
zorg = pd.read_csv('ZorgAPI.csv')
df_totaal = pd.read_csv('df_totaal.csv')
df_filter = pd.read_csv('filtered_df.csv')


# In[26]:


tab1, tab2, tab3 = st.tabs(['intro', 'overzicht', 'vergelijking'])


# ### Introductie

# #### Kolommen vertalen

# In[27]:


with tab1:
    # Dictionary voor Nederlandse vertalingen van kolomnamen
    kolom_vertalingen = {
        'housing_cost': 'Huisvestingskosten',
        'food_cost': 'Voedingskosten',
        'transportation_cost': 'Vervoerskosten',
        'healthcare_cost': 'Zorgkosten',
        'other_necessities_cost': 'Overige noodzakelijke kosten',
        'childcare_cost': 'Kinderopvangkosten',
        'taxes': 'Belastingen',
        'total_cost': 'Totale kosten',
        'median_family_income': 'Mediaan gezinsinkomen'
    }
    cost = cost.rename(columns=kolom_vertalingen)
    df_staat = df_staat.rename(columns=kolom_vertalingen)


# In[28]:


with tab1:
    st.title("Verenigde Staten")

    selected_variable = st.selectbox("Selecteer een variabele", list(kolom_vertalingen.values()))

    # Definieer een kleurenpalet voor elke variabele
    color_palette = {
        'Huisvestingskosten': 'steelblue',
        'Voedingskosten': 'forestgreen',
        'Vervoerskosten': 'peachpuff',
        'Zorgkosten': 'orange',
        'Overige noodzakelijke kosten': 'purple',
        'Kinderopvangkosten': 'yellowgreen',
        'Belastingen': 'pink',
        'Totale kosten': 'gray',
        'Mediaan gezinsinkomen': 'greenyellow'
    }


# #### Kaart Verenigde Staten

# In[29]:


with tab1:
    # Coördinaten van het midden van de VS
    us_coordinates = [37.0902, -95.7129]

    # Voeg de Choropleth-laag toe aan de kaart
    st.header(f"Kaart van de Verenigde Staten met {selected_variable}")
    if selected_variable== 'Huisvestingskosten':
        st.write('Op de kaart hieronder worden de huisvestingskosten weergegeven aan de hand van een schaal. De kaart laat zien dat de kosten in het noorden, midden en zuiden van Amerika lager zijn dan in het westen en oosten.')
    elif selected_variable== 'Voedingskosten':
        st.write('Op de kaart hieronder worden de voedingskosten weergegeven aan de hand van een schaal. De kaart toont aan dat in het midden van Amerika de kosten lager zijn dan in de rest van Amerika.')
    elif selected_variable== 'Vervoerskosten':
        st.write('Op de kaart hieronder worden de vervoerskosten weergegeven aan de hand van een schaal. Duidelijk is het verschil te zien tussen het noorden/westen en het zuiden/oosten van Amerika.')
    elif selected_variable== 'Zorgkosten':
        st.write('Op de kaart hieronder worden de zorgkosten weergegeven aan de hand van een schaal. Op deze kaart is te zien dat de kosten in het midden van Amerika hoger zijn dan in de rest van Amerika.')
    elif selected_variable== 'Overige noodzakelijke kosten':
        st.write('Op de kaart hieronder worden de overige noodzakelijke kosten weergegeven aan de hand van een schaal. De kaart toont aan dat in het midden van Amerika de kosten lager zijn dan in de rest van Amerika.')
    elif selected_variable== 'Kinderopvangkosten':
        st.write('Op de kaart hieronder worden de kinderopvangkosten weergegeven aan de hand van een schaal. De kaart toont aan dat in het zuidwesten van Amerika de kosten hoger zijn dan in de rest van Amerika.')
    elif selected_variable== 'Belastingen':
        st.write('Op de kaart hieronder worden de belastingen weergegeven aan de hand van een schaal. De kaart laat zien dat in het midden van Amerika de belastingen lager zijn in vergelijking met de rest van Amerika.')
    elif selected_variable == 'Totale kosten':
        st.write('Op de kaart hieronder worden de totale kosten weergeven aan de hand van een schaal. De kaart laat zien dat de totale kosten in het zuiden/oosten/midden de kosten lager zijn in vergelijk tot met de rest van Amerika.')
    elif selected_variable == 'Mediaan gezinsinkomen':
        st.write('Op de kaart hieronder wordt het mediaan gezinsinkomen weergeven aan de hand van een schaal. De kaart laat zien dat in het zuidoosten het mediaan gezinsinkomen lager is in vergelijk tot met de rest van Amerika.')

    folium_static_map = folium.Map(location=us_coordinates, zoom_start=4)

    folium.Choropleth(
        geo_data='https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/us-states.json',
        name='choropleth',
        data=df_staat,  # Je moet df_staat definiëren met de juiste gegevens
        columns=['name', selected_variable],
        key_on='feature.properties.name',
        fill_color='YlGn',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=selected_variable
    ).add_to(folium_static_map)

    # Toon de interactieve kaart met Streamlit
    folium_static(folium_static_map)


# #### Histogram, boxplot en scatterplot

# In[30]:


with tab1:
    # Geef zowel min_value als max_value als float door
    min_value = float(cost[selected_variable].min())
    max_value = float(cost[selected_variable].max())

    # Pas de min_value en max_value aan in st.slider
    range_variable = st.slider(f"Bereik van {selected_variable}", min_value=min_value, max_value=max_value, 
                               value=(min_value, max_value), format="%d", key='worst')

    # Filter de gegevens op basis van het geselecteerde bereik en variabele
    filtered_df = cost[(cost[selected_variable] >= range_variable[0]) & (cost[selected_variable] <= range_variable[1])]

    gemiddelde = filtered_df[selected_variable].mean()
    mediaan = filtered_df[selected_variable].median()


    # Maak een histogram-plot voor de gefilterde gegevens met Plotly Express
    fig = px.histogram(filtered_df, x=selected_variable, nbins=20, color_discrete_sequence=[color_palette[selected_variable]])

    fig.update_xaxes(title=selected_variable)
    fig.update_yaxes(title='Frequentie')
    fig.update_layout(bargap=0.05)

    #  Voeg lijnen toe voor het gemiddelde en de mediaan aan subplot 1
    fig.add_shape(
        type='line',
        x0=gemiddelde,
        x1=gemiddelde,
        y0=0,
        y1=1,
        xref='x',
        yref='paper',
        line=dict(color='red', dash='dash')
    )

    fig.add_shape(
        type='line',
        x0=mediaan,
        x1=mediaan,
        y0=0,
        y1=1,
        xref='x',
        yref='paper',
        line=dict(color='black', dash='solid')
    )

    fig.add_trace(go.Scatter(x=[None], y=[None], mode='lines', line=dict(color='red', dash='dash'), name=f'Gemiddelde: {gemiddelde:.2f}'))
    fig.add_trace(go.Scatter(x=[None], y=[None], mode='lines', line=dict(color='black', dash='solid'), name=f'Mediaan: {mediaan:.2f}'))

    # Maak een boxplot voor dezelfde gegevens met Plotly Express
    boxplot = px.box(filtered_df, y=selected_variable, color_discrete_sequence=[color_palette[selected_variable]])

    boxplot.update_yaxes(title=selected_variable)

    # Maak een eenvoudige scatter plot met "taxes" op de x-as en "total_cost" op de y-as
    scatter = px.scatter(cost, x=selected_variable, y="Totale kosten", color_discrete_sequence=[color_palette[selected_variable]])

    # Toon de scatter plot


    # Toon de plot
    st.header(f"Histogram van {selected_variable}")
    if selected_variable== 'Huisvestingskosten':
        st.write('Met behulp van de slider kun je uitschieters verwijderen, en de boxplot toont waar deze afwijkende waarden zich bevinden. Het verwijderen van uitschieters kan de verdeling van de data veranderen, maar soms blijft de basisvorm van de verdeling onveranderd.')
        st.write('In de histogram hieronder kun je zien hoe de data van de huisvestingskosten is verdeeld. De data vertoont een recht scheve verdeling, wat betekent dat de meeste waarden aan de rechterkant van de grafiek liggen.')
    elif selected_variable== 'Voedingskosten':
        st.write('Met behulp van de slider kun je uitschieters verwijderen, en de boxplot toont waar deze afwijkende waarden zich bevinden. Het verwijderen van uitschieters kan de verdeling van de data veranderen, maar soms blijft de basisvorm van de verdeling onveranderd.')
        st.write('In de histogram hieronder lijkt de data van de voedingskosten normaal verdeeld te zijn, maar na het verwijderen van de uitschieters lijkt het meer op een uniforme verdeling.')
    elif selected_variable== 'Vervoerskosten':
        st.write('Met behulp van de slider kun je uitschieters verwijderen, en de boxplot toont waar deze afwijkende waarden zich bevinden. Het verwijderen van uitschieters kan de verdeling van de data veranderen, maar soms blijft de basisvorm van de verdeling onveranderd.')
        st.write('In de histogram hieronder kun je zien dat de data met de uitschieters lijkt op een normale verdeling. Na het verwijderen van de uitschieters wordt dit bevestigd doordat de mediaan en het gemiddelde dichter bij elkaar komen.')
    elif selected_variable== 'Zorgkosten':
        st.write('Met behulp van de slider kun je uitschieters verwijderen, en de boxplot toont waar deze afwijkende waarden zich bevinden. Het verwijderen van uitschieters kan de verdeling van de data veranderen, maar soms blijft de basisvorm van de verdeling onveranderd.')
        st.write('In de histogram hieronder kun je zien dat de data met de uitschieters lijkt op een normale verdeling. Na het verwijderen van de uitschieters wordt dit bevestigd doordat de mediaan en het gemiddelde dichter bij elkaar komen.')
    elif selected_variable== 'Overige noodzakelijke kosten':
        st.write('Met behulp van de slider kun je uitschieters verwijderen, en de boxplot toont waar deze afwijkende waarden zich bevinden. Het verwijderen van uitschieters kan de verdeling van de data veranderen, maar soms blijft de basisvorm van de verdeling onveranderd.')
        st.write('In het histogram hieronder kun je zien dat de data met de uitschieters niet lijkt op een normale verdeling. Na het verwijderen van de uitschieters blijven de mediaan en het gemiddelde nog steeds ver uit elkaar staan.')
    elif selected_variable== 'Kinderopvangkosten':
        st.write('Met behulp van de slider kun je uitschieters verwijderen, en de boxplot toont waar deze afwijkende waarden zich bevinden. Het verwijderen van uitschieters kan de verdeling van de data veranderen, maar soms blijft de basisvorm van de verdeling onveranderd.')
        st.write('In de histogram hieronder kun je zien dat de data met de uitschieters niet lijkt op een normale verdeling. Na het verwijderen van de uitschieters blijven de mediaan en het gemiddelde nog steeds ver uit elkaar staan.')

    elif selected_variable== 'Belastingen':
        st.write('Met behulp van de slider kun je uitschieters verwijderen, en de boxplot toont waar deze afwijkende waarden zich bevinden. Het verwijderen van uitschieters kan de verdeling van de data veranderen, maar soms blijft de basisvorm van de verdeling onveranderd.')
        st.write('In de histogram hieronder kun je zien dat de data met de uitschieters lijkt op een normale verdeling. Na het verwijderen van de uitschieters wordt dit bevestigd doordat de mediaan en het gemiddelde dichter bij elkaar komen')
    elif selected_variable == 'Totale kosten':
        st.write('Met behulp van de slider kun je uitschieters verwijderen, en de boxplot toont waar deze afwijkende waarden zich bevinden. Het verwijderen van uitschieters kan de verdeling van de data veranderen, maar soms blijft de basisvorm van de verdeling onveranderd.')
        st.write('In de histogram hieronder kun je zien dat de data met de uitschieters niet lijkt op een normale verdeling. Na het verwijderen van de uitschieters blijven de mediaan en het gemiddelde nog steeds ver uit elkaar staan.')
    elif selected_variable == 'Mediaan gezinsinkomen':
        st.write('Met behulp van de slider kun je uitschieters verwijderen, en de boxplot toont waar deze afwijkende waarden zich bevinden. Het verwijderen van uitschieters kan de verdeling van de data veranderen, maar soms blijft de basisvorm van de verdeling onveranderd.')
        st.write('In het histogram hieronder kun je zien dat de data met de uitschieters lijkt op een normale verdeling. Na het verwijderen van de uitschieters wordt dit bevestigd doordat de mediaan en het gemiddelde dichter bij elkaar komen.')

    st.plotly_chart(fig)

    st.header(f"Boxplot van {selected_variable}")
    st.plotly_chart(boxplot)

    if selected_variable == 'Totale kosten':
        pass
    else:
        st.header(f"Spreidingsdiagram van {selected_variable}")
        if selected_variable== 'Huisvestingskosten':
            st.write('In de onderstaande spreidingsdiagram wordt de relatie tussen huisvestingskosten en totale kosten weergegeven. De grafiek laat duidelijk zien dat hogere huisvestingskosten correleren met hogere totale kosten.')
        elif selected_variable== 'Voedingskosten':
            st.write('In de onderstaande spreidingsdiagram wordt de relatie tussen voedingskosten en totale kosten weergegeven. De grafiek laat duidelijk zien dat hogere voedingskosten correleren met hogere totale kosten.')
        elif selected_variable== 'Vervoerskosten':
            st.write('Uit de onderstaande spreidingsdiagram is niet direct een concrete conclusie te trekken over de relatie tussen vervoerskosten en totale kosten, omdat veel datapunten zich in hetzelfde gebied bevinden.')
        elif selected_variable== 'Zorgkosten':
            st.write('In de onderstaande spreidingsdiagram wordt de relatie tussen zorgkosten en totale kosten weergegeven. De grafiek laat duidelijk zien dat hogere zorgkosten correleren met hogere totale kosten.')
        elif selected_variable== 'Overige noodzakelijke kosten':
            st.write('In de onderstaande spreidingsdiagram wordt de relatie tussen overige noodzakelijke kosten en totale kosten weergegeven. De grafiek laat duidelijk zien dat hogere overige noodzakelijke kosten correleren met hogere totale kosten.')
        elif selected_variable== 'Kinderopvangkosten':
            st.write('In de onderstaande spreidingsdiagram wordt de relatie tussen kinderopvangkosten en totale kosten weergegeven. De grafiek laat duidelijk zien dat hogere kinderopvangkosten correleren met hogere totale kosten.')
        elif selected_variable== 'Belastingen':
            st.write('In de onderstaande spreidingsdiagram wordt de relatie tussen belastingen en totale kosten weergegeven. De grafiek laat duidelijk zien dat hogere belastingen correleren met hogere totale kosten.')
        elif selected_variable == 'Mediaan gezinsinkomen':
            st.write('Uit de onderstaande spreidingsdiagram is niet direct een concrete conclusie te trekken over de relatie tussen het mediaan gezinsinkomen en totale kosten, omdat veel datapunten zich in hetzelfde gebied bevinden.')
        st.plotly_chart(scatter)


# ### Overzicht staten

# #### Data aanpassingen

# In[ ]:


with tab2:
    groen1 = px.colors.sequential.Greens[2]
    groen2 = px.colors.sequential.Greens[4]
    groen3 = px.colors.sequential.Greens[6]
    groen4 = px.colors.sequential.Greens[8]
    
    blauw1 = px.colors.sequential.Blues[1]
    blauw2 = px.colors.sequential.Blues[2]
    blauw3 = px.colors.sequential.Blues[3]
    blauw4 = px.colors.sequential.Blues[4]
    blauw5 = px.colors.sequential.Blues[5]
    blauw6 = px.colors.sequential.Blues[6]
    blauw7 = px.colors.sequential.Blues[7]
    blauw8 = px.colors.sequential.Blues[8]

    rood = px.colors.sequential.Reds[4]


# In[ ]:


with tab2:
    kolom_vertalingen = {
            'PrivateWork': 'Particuliere sector',
            'PublicWork': 'Publieke sector',
            'SelfEmployed': 'Zelfstandige',
            'FamilyWork': 'Onbetaald familiewerk'
        }
    population = population.rename(columns=kolom_vertalingen)


# In[ ]:


with tab2:
    #inkomen categoriseren
    def categorize_income(x, low_threshold, high_threshold):
        if x < low_threshold:
            return 'Laag inkomen'
        elif low_threshold <= x < high_threshold:
            return 'Gemiddeld inkomen'
        else:
            return 'Hoog inkomen'

    income_threshold_low = 40000# jouw lage drempel voor inkomen
    income_threshold_high = 100000# jouw hoge drempel voor inkomen

    income['inkomensgroep'] = income['Mean'].apply(lambda x: categorize_income(x, income_threshold_low, income_threshold_high))


# In[ ]:


with tab2:
    # Create a Streamlit app
    st.title('Informatie per staat')
    st.write("Hieronder zijn verschillende gegevens van een staat gevisualiseerd. "
    "Er is gebruikgemaakt van de gegevens van 2011 tot en met 2015. Met behulp van de drop-downbox kan er een staat worden gekozen. " 
    "De visualisaties zullen zich daar op aanpassen.")

    selected_state = st.selectbox('Kies een staat', income['State_Name'].unique(), key = '1')

    state = income[income['State_Name'] == selected_state]
    state = state.reset_index(drop=True)
    afkorting = state['State_ab'].loc[0]


# #### Cijfers over de staat

# In[ ]:


with tab2:
    st.header("Huishoudinkomen")
    st.write("Hieronder is de verdeling van het huishoudinkomen opgedeeld in inkomensgroepen over de staat te zien. "
             "Een laag inkomen is een inkomen onder 40.000, een gemiddeld inkomen is een inkomen tussen de 40.000 en 100.000 en een hoog inkomen is een inkomen boven de 100.000. "
             "De inkomensgroepen zijn gebasseerd op de verdeling van het inkomen in de periode 2011 tm 2015. "
             "In de kaart is te zien waar de verschillende inkomensgroepen zich bevinden. "
             "Daarnaast is er in de tekst boven de kaart weergegeven wat het percentage inwoners zijn onder die inkomensgroep.") 
    
    col1, col2, col3 = st.columns(3)

    filterdf = income[income['State_Name'] == selected_state]

    groep = pd.DataFrame(filterdf.groupby('inkomensgroep')['inkomensgroep'].count().reset_index(name='count')) 
    laag = groep[groep['inkomensgroep'] == 'Laag inkomen']
    mid = groep[groep['inkomensgroep'] == 'Gemiddeld inkomen']
    hoog = groep[groep['inkomensgroep'] == 'Hoog inkomen']
    totaal = laag['count'].values[0] + mid['count'].values[0] + hoog['count'].values[0]

    laag_percentage = f"{(laag['count'].values[0] / totaal * 100):.2f}%"
    mid_percentage = f"{(mid['count'].values[0] / totaal * 100):.2f}%"
    hoog_percentage = f"{(hoog['count'].values[0] / totaal * 100):.2f}%"

    col1.metric("Laag inkomen", laag_percentage)
    col2.metric("Gemiddeld inkomen", mid_percentage)
    col3.metric("Hoog inkomen", hoog_percentage)


# #### Kaart over inkomensgroepen

# In[ ]:


with tab2:
    colors = {'Laag inkomen': groen2, 'Gemiddeld inkomen': blauw4, 'Hoog inkomen' : rood}


# In[ ]:


with tab2:
    filterdf = income[income['State_Name'] == selected_state]

    fig = px.scatter_mapbox(filterdf, lat="Lat", lon="Lon", color = 'inkomensgroep', 
                            color_discrete_map=colors, zoom=5,
                            mapbox_style="carto-positron", title = 'Kaart met inkomensgroepen')

    fig.update_layout(  
        autosize=True)

    center = dict(lon=filterdf['Lon'].iloc[0], lat=filterdf['Lat'].iloc[0])  # Coordinates for Alabama
    fig.update_geos(center=center, scope="usa")

    st.plotly_chart(fig, use_container_width=True)


# #### Pie chart geslacht

# In[ ]:


with tab2:
    st.header("Verdelingen")
    st.write("In de linker cirkeldiagram is de verdeling van de werksectoren in de desbetreffende staat te zien. "
    "Hierin is er een verdeling gemaakt tussen de particuliere sector, publieke sector, zelfstandige en onbetaald familiewerk. "
    "In de interactieve plot kunnen de verschillende delen gemakkelijk geselecteerd worden zodat de informatie duidelijk te zien is. ")
    
    st.write("In de rechter cirkeldiagram is de verdeling van de verschillende kosten in de desbetreffende staat te zien. "
             "Er is hierbij gebruik gemaakt van de vervoerskosten, zorgkosten, kinderopvangkosten, huisvestigingskosten, voedingskosten, belastingen en overige noodzakelijke kosten. ")

    col4, col5 = st.columns(2)


# #### Pie chart over employment

# In[31]:


with tab2:
    employment = population[['State', 'County', 'TotalPop', 'Employed', 'Particuliere sector', 'Publieke sector', 'Zelfstandige', 'Onbetaald familiewerk', 'Unemployment']]
    employment = employment.dropna()
    employment['Particuliere sector'] = (employment['Employed'] * employment['Particuliere sector'] / 100).round().astype(int)
    employment['Publieke sector'] = (employment['Employed'] * employment['Publieke sector'] / 100).round().astype(int)
    employment['Zelfstandige'] = (employment['Employed'] * employment['Zelfstandige'] / 100).round().astype(int)
    employment['Onbetaald familiewerk'] = (employment['Employed'] * employment['Onbetaald familiewerk'] / 100).round().astype(int)
    employment['Unemployment'] = (employment['TotalPop'] * employment['Unemployment'] / 100).round().astype(int)
    employment = employment.groupby(['State']).agg({'TotalPop': 'sum', 'Employed': 'sum', 'Particuliere sector': 'sum', 'Publieke sector': 'sum', 'Zelfstandige': 'sum', 'Onbetaald familiewerk': 'sum', 'Unemployment': 'sum'}).reset_index()


# In[32]:


with tab2:
    employment['Anders'] = employment['TotalPop'] - employment['Employed'] - employment['Unemployment']
    employment1 = employment[['State', 'Employed', 'Unemployment', 'Anders']] 
    employment1 = employment1.melt(id_vars=['State'], var_name='Category', value_name='Value')
    employment1 = employment1.sort_values(by = 'State').reset_index(drop = True)


# In[33]:


with tab2:
    employment2 = employment[['State', 'Particuliere sector', 'Publieke sector', 'Zelfstandige', 'Onbetaald familiewerk']]
    employment2 = employment2.melt(id_vars=['State'], var_name='Type', value_name='aantal')
    employment2 = employment2.sort_values(by = 'State').reset_index(drop = True)
    employment2['Category'] = 'Employed'


# In[34]:


with tab2:
    employers = pd.merge(employment1, employment2, on=['State', 'Category'] , how='outer')
    def replace_na_with_value(row):
        if pd.isna(row['aantal']):
            return row['Value']
        return row['aantal']

    # Pas de functie toe op de kolom "Aantal"
    employers['aantal'] = employers.apply(replace_na_with_value, axis=1)


# In[ ]:


with tab2:
    colors1 = {'Particuliere sector':groen1, 'Publieke sector':groen2, 'Zelfstandige' : groen3, 'Onbetaald familiewerk' : groen4}
    colors_list1 = [colors1[key] for key in colors1]

    colors2 = {'Huisvestingskosten': blauw1, 'Voedingskosten': blauw2, 'Vervoerskosten': blauw3, 'Zorgkosten': blauw4, 'Overige noodzakelijke kosten': blauw5, 'Kinderopvangkosten': blauw6, 'Belastingen': blauw7}
    colors_list2 = [colors2[key] for key in colors2]


# In[ ]:


with tab2:
    with col4:
        data = employment2[employment2['State'] == selected_state]
        pie3 = px.pie(data, names='Type', values='aantal', color_discrete_sequence=colors_list1, title = "Werksector")
        pie3.update_traces(textposition='inside', textinfo='percent+label', showlegend = False)
        # pie3.update_layout(legend=dict(orientation="h", y=-0.2, font=dict(size=9)))

        # Streamlit app
        st.plotly_chart(pie3, use_container_width=True)


# #### Pie chart kosten

# In[ ]:


with tab2:
    with col5:
        filtered_df = df_staat[df_staat['name'] == selected_state]

        # Selecteer de waarden en namen voor de pie chart
        values = filtered_df.iloc[0, 1:9].tolist()  # Hier nemen we aan dat de waarden beginnen vanaf de derde kolom (index 2)
        names = filtered_df.columns[1:9].tolist()

        # Maak een pie chart met de geselecteerde waarden en namen
        pie4 = px.pie(values=values, names=names, color_discrete_sequence=colors_list2, title = 'Verdeling kosten')
        pie4.update_traces(textposition='inside', textinfo='percent+label', showlegend = False)
        # pie4.update_layout(legend=dict(orientation="h", font=dict(size=9)))


        # Toon het pie chart
        st.plotly_chart(pie4,  use_container_width=True)


# #### Lijn diagram zorg

# In[ ]:

# In[ ]:
# In[ ]:

df_zorg1 = zorg[zorg['YEAR'] < 2016]
with tab2:
    st.header('Zorgverzekering over de jaren')
    st.write("In de onderstaande grafiek is het aantal mensen met een zorgverzekering per jaar te zien. "
             "Elke kleur staat voor een andere groep mensen in de samenleving op basis van leeftijd of geslacht. ")
    df_zorg1 = df_zorg1[df_zorg1['NAME'] == selected_state]

    # Selecteer jaren om weer te geven
    jaren = ['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']

    # Maak een Streamlit-figure
    lijn = go.Figure()

    for age in df_zorg1.AGECAT.unique():
        for sex in range(3):
            lijst = []
            for index, row in df_zorg1.iterrows():
                year = row['YEAR']
                row_age = row['AGECAT']
                row_sex = row['SEXCAT']
                pt = row['NIC_PT']
                if str(row_age) == str(age) and row_sex == sex:
                    lijst.append(pt)
            trace_name = f'Age {age}, Sex {sex}'
            lijn.add_trace(go.Scatter(x=jaren, y=lijst, mode='lines+markers', name=trace_name))

    # Vervang 0 door "totaal", 1 door "man" en 2 door "vrouw" in de legenda
    lijn.update_traces(name="totaal", selector=dict(name="Age 0, Sex 0"))
    lijn.update_traces(name="man", selector=dict(name="Age 0, Sex 1"))
    lijn.update_traces(name="vrouw", selector=dict(name="Age 0, Sex 2"))
    lijn.update_traces(name="totaal van 18 t/m 65", selector=dict(name="Age 1, Sex 0"))
    lijn.update_traces(name="man van 18 t/m 65", selector=dict(name="Age 1, Sex 1"))
    lijn.update_traces(name="vrouw van 18 t/m 65", selector=dict(name="Age 1, Sex 2"))
    lijn.update_traces(name="totaal onder 19", selector=dict(name="Age 4, Sex 0"))

    # Toon de grafiek in Streamlit
    st.plotly_chart(lijn, use_container_width=True)


# In[ ]:


with tab2:
    df_zorg = zorg[zorg['YEAR'] < 2016]
    df_zorg = df_zorg[df_zorg['AGECAT'] == 0]
    df_zorg = df_zorg[df_zorg['SEXCAT'] == 0]
    df_zorg = df_zorg[['NIC_PT', 'NAME', 'NUI_PT', 'YEAR', 'AGECAT', 'SEXCAT']]
    
with tab2:
    staat = df_filter[df_filter['Area_name'] == selected_state]

with tab2:
    # Lijst van de prefixen die we willen verwerken
    prefixes = ['Unemployed', 'Employed', 'Civilian_labor_force']

    # De uiteindelijke DataFrame waarin we de resultaten zullen opslaan
    jaar_employed = pd.DataFrame()

    # Loop over de prefixen
    for prefix in prefixes:
        # Selecteer de kolommen die met het huidige prefix beginnen en behoud de waarden
        staat = staat.drop_duplicates(subset=['Area_name'])

        ake = staat.filter(like=prefix)

        # Voeg de 'State'-kolom toe aan de gefilterde DataFrame
        ake['Area_name'] = staat['Area_name']

        # Gebruik melt om de kolommen om te zetten naar rijen
        jaar_column = pd.melt(ake, id_vars=['Area_name'], var_name='Year', value_name=prefix)

        # Sorteer de DataFrame op 'State' en 'Year' voor een overzichtelijke weergave
        jaar_column = jaar_column.sort_values(by=['Area_name', 'Year']).reset_index(drop=True)

        # Haal alleen het jaar uit de 'Year' kolom
        jaar_column['Year'] = jaar_column['Year'].str.extract('(\d{4})')

        # Verwijder eventuele komma's in de kolom en converteer naar integer
        jaar_column[prefix] = jaar_column[prefix].str.replace(',', '', regex=True).astype(int)

        # Voeg de huidige DataFrame samen met de uiteindelijke DataFrame
        if jaar_employed.empty:
            jaar_employed = jaar_column
        else:
            jaar_employed = jaar_employed.merge(jaar_column, on=['Area_name', 'Year'])

    # Toon het resultaat
    jaar_employed['Year'] = jaar_employed['Year'].astype(int)
    # jaar_employed
    
with tab2:
    jaar_zorg = df_zorg[df_zorg['NAME'] == selected_state]
# jaar_zorg

with tab2:
    # Drop de oorspronkelijke kolom Year_Age_Sex
    jaar_zorg.drop(columns=['AGECAT', 'SEXCAT', 'NUI_PT'], inplace=True)
    # jaar_zorg
    
with tab2:
    samen = jaar_zorg.merge(jaar_employed, left_on='YEAR', right_on='Year').sort_values(by='YEAR', ascending=True)
    # samen
    
with tab2:
    # Filter de gegevens voor trainingsgegevens
    train_data = samen[samen['Year'] < 2016]

    # Bouw een lineair regressiemodel
    model = LinearRegression()
    model.fit(train_data[['Year']], train_data['NIC_PT'])

    # Voorspellingen voor de jaren 2016 tot en met 2021
    years_to_predict = [2016, 2017, 2018, 2019, 2020, 2021]
    predictions = model.predict(pd.DataFrame({'Year': years_to_predict}))

    # Voeg de voorspellingen toe aan een DataFrame
    predictions_df = pd.DataFrame({
        'Year': years_to_predict,
        'NIC_PT': predictions
    })

    train_predictions = model.predict(train_data[['Year']])
    r2 = r2_score(train_data['NIC_PT'], train_predictions)

    # Toon de R-squared score
    # print("R-squared score for the model: {:.2f}".format(r2))

    # Toon het resultaat
    cumulative = pd.concat([samen, predictions_df], ignore_index=True)
    # cumulative['NIC_PT'] = cumulative['NIC_PT'].astype(int)
    # cumulative
    
with tab2:
    st.header("Voorspelling zorgverzekeringen")
    st.write("Hieronder is een diagram te zien waarbij het aantal mensen met een zorgverzekering te zien is. "
             "De periode 2011 tm 2015 is werkelijke data. De jaren na 2015 zijn een voorspelling op basis van de eerdere gegevens. "
             "Ook is er gekeken naar hoeveel mensen een baan hadden en hoeveel mensen werkloos zijn. "
             "Met de verticale lijn is te zien vanaf wanneer er voorspelt wordt. ")
    drempelwaarde_x = 2015  # Pas deze waarde aan
    jaren = cumulative['Year']

    # Cumulatieve dieselwaarden tot en met 2016 (voorbeeldgegevens, pas aan zoals nodig)
    diesel = cumulative['NIC_PT']

    # Maak een Plotly figuur
    fig = go.Figure()

    # Voeg een lijn toe voor de cumulatieve dieselwaarden tot de drempelwaarde
    fig.add_trace(go.Scatter(x=jaren[jaren <= drempelwaarde_x], y=diesel[jaren <= drempelwaarde_x], mode='lines+markers', name='Aantal Zorgverzekeringen'))

    # Voeg een lijn toe voor de cumulatieve dieselwaarden na de drempelwaarde en geef deze een andere kleur
    fig.add_trace(go.Scatter(x=jaren[jaren >= drempelwaarde_x], y=diesel[jaren >= drempelwaarde_x], mode='lines+markers', name='Voorspelde aantal Zorgverzekeringen', line=dict(color='red')))

    fig.update_layout(
        title='Zorgverzekeringen',
        xaxis=dict(title='Jaar'),
        yaxis=dict(title='Zorgverzekeringen')
    )

    st.plotly_chart(fig)




# ### Vergelijking

# In[ ]:


with tab3:
    cost['family_member_count'] = cost['family_member_count'].replace('1p0c', '1 volwassene en geen kinderen')
    cost['family_member_count'] = cost['family_member_count'].replace('2p0c', '2 volwassenen en geen kinderen')
    cost['family_member_count'] = cost['family_member_count'].replace('1p1c', '1 ouder en 1 kind')
    cost['family_member_count'] = cost['family_member_count'].replace('1p2c', '1 ouder en 2 kinderen')
    cost['family_member_count'] = cost['family_member_count'].replace('1p3c', '1 ouder en 3 kinderen')
    cost['family_member_count'] = cost['family_member_count'].replace('1p4c', '1 ouder en 4 kinderen')
    cost['family_member_count'] = cost['family_member_count'].replace('2p1c', '2 ouders en 1 kind')
    cost['family_member_count'] = cost['family_member_count'].replace('2p2c', '2 ouders en 2 kinderen')
    cost['family_member_count'] = cost['family_member_count'].replace('2p3c', '2 ouders en 3 kinderen')
    cost['family_member_count'] = cost['family_member_count'].replace('2p4c', '2 ouders en 4 kinderen')


# #### Selectie vergelijkingen

# In[212]:


with tab3:
    st.title("Vergelijkingen")
    st.write("Om wat diepere informatie te krijgen te kunnen maken van de verschillende counties in een staat kan er hieronder een vergelijking gemaakt worden. "
             "Hierbij moet er een staat gekozen worden en de grootte van het huishouden. "
             "Daarna kunnen er 2 counties in die staat gekozen worden om te vergelijken. ")

    selected_state = st.selectbox('Kies een staat', income['State_Name'].unique(), key = '2')
    huishouden = st.selectbox('Kies de samenstelling van het huishouden', ['1 volwassene en geen kinderen', '2 volwassenen en geen kinderen', '1 ouder en 1 kind', '1 ouder en 2 kinderen', '1 ouder en 3 kinderen', '1 ouder en 4 kinderen', '2 ouders en 1 kind', '2 ouders en 2 kinderen', '2 ouders en 3 kinderen', '2 ouders en 4 kinderen'], key = '342')  # Parameters: label, minimum, maximum, standaardwaarde
    
    col8, col9 = st.columns(2)
    with col8:
        state = income[income['State_Name'] == selected_state]
        state = state.reset_index(drop=True)
        afkorting = state['State_ab'].loc[0]
        
        cost1 = cost[cost['state'] == afkorting]
        selected_county1 = st.selectbox('Kies een county', cost1['county'].unique(), key = '4')
        
    with col9:
        state = income[income['State_Name'] == selected_state]
        state = state.reset_index(drop=True)
        afkorting = state['State_ab'].loc[0]
        
        cost2 = cost[cost['state'] == afkorting]
        selected_county2 = st.selectbox('Kies een county', cost2['county'].unique(), key = '5')

# #### Barplot

# In[ ]:


with tab3:
    if selected_county1 and selected_county2 and huishouden:
        st.write(f"In onderstaande grafiek is het verschil tussen de verschillende kosten te zien tussen de counties {selected_county1} en {selected_county1}. "
                 f"Deze counties zijn gevestigd in {selected_state}. "
                 f"De vergelijking is gemaakt op een huishouden van {huishouden}. ")
        # Verzamel gegevens voor beide geselecteerde county en huishouden
        data1 = cost1[(cost1['county'] == selected_county1) & (cost1['family_member_count'] == huishouden)]
        data2 = cost2[(cost2['county'] == selected_county2) & (cost2['family_member_count'] == huishouden)]

        data1 = data1[['county', 'Huisvestingskosten', 'Voedingskosten', 'Vervoerskosten', 'Zorgkosten', 'Overige noodzakelijke kosten', 'Kinderopvangkosten', 'Belastingen']]
        melted_df1 = pd.melt(data1, id_vars=['county'], var_name='kostentype', value_name='Kosten')
        
        data2 = data2[['county', 'Huisvestingskosten', 'Voedingskosten', 'Vervoerskosten', 'Zorgkosten', 'Overige noodzakelijke kosten', 'Kinderopvangkosten', 'Belastingen']]
        melted_df2 = pd.melt(data2, id_vars=['county'], var_name='kostentype', value_name='Kosten')

        fig = go.Figure()

        # Voeg de eerste trace toe aan de figuur met de gewenste naam
        fig.add_trace(go.Bar(x=melted_df1['kostentype'], y=melted_df1['Kosten'], name=selected_county1))

        # Voeg de tweede trace toe aan de figuur met de gewenste naam
        fig.add_trace(go.Bar(x=melted_df2['kostentype'], y=melted_df2['Kosten'], name=selected_county2))

        # Update de layout van de figuur voor een legenda
        fig.update_layout(barmode='group', legend=dict(title=dict(text='Counties')), title = 'Verdeling kosten')

        # Toon de plot
        st.plotly_chart(fig)


        # verg = income.groupby('County')[['Mean', 'Median', 'Stdev']].mean().reset_index()
        # verg_county1 = verg[verg['County'] == selected_county1]
        # gemiddelde_inkomen1 = verg_county1.iloc[0, 1]
        # standaarddeviatie_inkomen1 = verg_county1.iloc[0, 3]
        # mediaan_inkomen1 = verg_county1.iloc[0, 2]

        # bar45 = px.bar(
        #     x=['Gemiddelde huishoudinkomen', 'Mediaan huishoudinkomen'],
        #     y=[gemiddelde_inkomen1, mediaan_inkomen1],
        #     error_y=dict(type='constant', value=standaarddeviatie_inkomen1), barmode = 'group',
        #     title='Gemiddelde, Mediaan en Standaarddeviatie van Inkomen')
        
        # verg_county2 = verg[verg['County'] == selected_county2]
        # gemiddelde_inkomen2 = verg_county2.iloc[0, 1]
        # standaarddeviatie_inkomen2 = verg_county2.iloc[0, 3]
        # mediaan_inkomen2 = verg_county2.iloc[0, 2]
        
        # bar45.add_bar(
        #     x=['Gemiddelde huishoudinkomen', 'Mediaan huishoudinkomen'],
        #     y=[gemiddelde_inkomen2, mediaan_inkomen2],
        #     error_y=dict(type='constant', value=standaarddeviatie_inkomen2),
        #     name=selected_county2
        # )
        # st.plotly_chart(bar45)

# In[ ]:





# In[ ]:




