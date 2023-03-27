import numpy as np #Linear Algebra
import pandas as pd #To Wrok WIth Data
import streamlit as st
from streamlit_option_menu import option_menu
## I am going to use plotly for visualizations. It creates really cool and interective plots.
import matplotlib.pyplot as plt # Just in case.
import plotly.express as px #Easy way to plot charts
import plotly.graph_objects as go #Does the same thing. Gives more options.
import plotly as ply # The whole package
from plotly.subplots import make_subplots #As the name suggests, for subplots.
import seaborn as sns #Just in case. It can be useful sometimes.

st.set_page_config(page_title="Literacy Rate DAshboard", page_icon="chart_with_upwards_trend:", layout="wide")
st.title(":chart_with_upwards_trend: Literacy Rate of India")   # Used to set the title 

#Hide Streamlit Style
hide_st_style = """
                 <style>
                 #MainMenu {visibility:hidden;}
                 footer {visibility:hidden;}
                 header{visibility:hidden;}
                 </style>
                """
st.markdown(hide_st_style, unsafe_allow_html = True)

#df = pd.read_csv("../input/govt-of-india-literacy-rate/GOI.csv") #Loading the dataset.
df1=pd.read_csv("C:/Users/shawr/Downloads/Devika Python Project/GOI.csv")
#df1
#df1.columns

#New Column
df1['Total - Per. Change'] = (df1.loc[:,'Literacy Rate (Persons) - Total - 2011'] - 
                df1.loc[:,'Literacy Rate (Persons) - Total - 2001'])/df1.loc[:,'Literacy Rate (Persons) - Total - 2001']
df1['Rural - Per. Change'] = (df1.loc[:,'Literacy Rate (Persons) - Rural - 2011'] - 
                df1.loc[:,'Literacy Rate (Persons) - Rural - 2001'])/df1.loc[:,'Literacy Rate (Persons) - Total - 2001']
df1['Urban - Per. Change'] = (df1.loc[:,'Literacy Rate (Persons) - Urban - 2011'] - 
                df1.loc[:,'Literacy Rate (Persons) - Urban - 2001'])/df1.loc[:,'Literacy Rate (Persons) - Total - 2001']

#Filter of Category
st.sidebar.header("Please Filter Here:")
Category= st.sidebar.multiselect(
    "Select the Category",
    options=df1["Category"].unique(),
    default=df1["Category"].unique()
)    

df1= df1.query( 
    "Category==@Category"
)

## Column names are too long, I don't need that much info in a column name. So, i am altering the names.
new_col=[]
for i in df1.columns:
    new_col.append(i.split('(Persons) - ')[-1])
df1.columns=new_col


# Overall Literacy Rates in India
India = df1[df1['Category'] == 'Country'].T
India = India.iloc[2:8,:]
India.reset_index(inplace=True)
India.columns = ['Measure', 'Value']
India.loc[:,'Measure'] = India['Measure'].apply(lambda x : str(x).split(' -')[0])
India_2001 = India.iloc[[0,2,4],:]
India_2011 = India.iloc[[1,3,5],:]
fig = go.Figure(data=[
    go.Bar(name='2001', x=India_2001['Measure'], y=India_2001['Value'], marker_color='rgb(55, 83, 109)'),
    go.Bar(name='2011', x=India_2011['Measure'], y=India_2011['Value'], marker_color='rgb(26, 118, 255)')
])
fig.update_layout(barmode='group', title='Overall Literacy Rate in India :')
#st.plotly_chart(fig)


df = df1.iloc[1:,:] #Removing data for India as a whole country.
df.rename(columns={'Country/ States/ Union Territories Name' :'States/ Union Territories'}, inplace = True) 


# BoxPlot
fig1 = go.Figure()
fig1.add_trace(go.Box(y=df['Total - 2001'], name='Total-2001', boxpoints='suspectedoutliers'))
fig1.add_trace(go.Box(y=df['Total - 2011'], name='Total-2011',boxpoints='suspectedoutliers'))
fig1.add_trace(go.Box(y=df['Rural - 2001'], name='Rural-2001', boxpoints='suspectedoutliers'))
fig1.add_trace(go.Box(y=df['Rural - 2011'], name='Rural-2011', boxpoints='suspectedoutliers'))
fig1.add_trace(go.Box(y=df['Urban - 2001'], name='Urban-2001', boxpoints='suspectedoutliers'))
fig1.add_trace(go.Box(y=df['Urban - 2011'], name='Urban-2011', boxpoints='suspectedoutliers'))
#st.plotly_chart(fig1)



# Total Literacy Rate Across Nation:
df.sort_values(by='Total - 2001', inplace=True)

fig2 = go.Figure(data = [
    go.Scatter(name='2001', x=df['States/ Union Territories'], y=df['Total - 2001'], mode='markers',marker=dict(
            color='red',
            colorscale='Viridis')),
    go.Scatter(name='2011', x=df['States/ Union Territories'], y=df['Total - 2011'], mode='markers',marker=dict(
            color='green',
            colorscale='Viridis'))
])

fig2.update_layout(barmode='group', title = 'Total Literacy Rate Across Nation :')
#st.plotly_chart(fig2)

# Rural Literacy Rate Across Nation:
df.sort_values(by='Rural - 2001', inplace=True)

fig3 = go.Figure(data = [
    go.Line(name='2001', x=df['States/ Union Territories'], y=df['Rural - 2001'], mode='markers',marker=dict(
            color='red',
            colorscale='Viridis')),
    go.Line(name='2011', x=df['States/ Union Territories'], y=df['Rural - 2011'], mode='markers',marker=dict(
            color='green',
            colorscale='Viridis'))
])

fig3.update_layout(barmode='group', title = 'Literacy rate in rural areas acorss the country :')
#st.plotly_chart(fig3)

# Urban Literacy Rate Across Nation:
df.sort_values(by='Urban - 2001', inplace=True)

fig4 = go.Figure(data = [
    go.Line(name='2001', x=df['States/ Union Territories'], y=df['Urban - 2001'], mode='markers',marker=dict(
            color='red',
            colorscale='Viridis')),
    go.Line(name='2011', x=df['States/ Union Territories'], y=df['Urban - 2011'], mode='markers',marker=dict(
            color='green',
            colorscale='Viridis'))
])

fig4.update_layout(barmode='group')
#st.plotly_chart(fig4)



#Lowest and Highest Total in 2001
lowest_2001 = df.sort_values(by=['Total - 2001']).head()
highest_2001 = df.sort_values(by=['Total - 2001']).tail()

fig5 = go.Figure(data = [
    go.Line(name = 'Lowest_2001', x=lowest_2001['States/ Union Territories'], y=lowest_2001['Total - 2001'], mode='markers'),
    go.Line(name = 'Highest_2001', x=highest_2001['States/ Union Territories'], y=highest_2001['Total - 2001'], mode='markers')
])

fig5.update_layout(barmode='group', title = 'Lowest and highest "Total literacy" rate in 2001 :')
#st.plotly_chart(fig5)

#Lowest and Highest Total in 2011 
lowest_2011 = df.sort_values(by=['Total - 2011']).head()
highest_2011 = df.sort_values(by=['Total - 2011']).tail()

fig6 = go.Figure(data = [
    go.Line(name = 'Lowest_2011', x=lowest_2011['States/ Union Territories'], y=lowest_2011['Total - 2011'], mode='markers'),
    go.Line(name = 'Highest_2011', x=highest_2011['States/ Union Territories'], y=highest_2011['Total - 2011'], mode='markers')
])

fig6.update_layout(barmode='group', title = 'Lowest and highest "Total Literacy" literacy rate in 2011 :')
#st.plotly_chart(fig6)


#Lowest and Highest of Rural in 2001
lowest_2001 = df.sort_values(by=['Rural - 2001']).head()
highest_2001 = df.sort_values(by=['Rural - 2001']).tail()

fig7 = go.Figure(data = [
    go.Line(name = 'Lowest_2001', x=lowest_2001['States/ Union Territories'], y=lowest_2001['Rural - 2001'], mode='markers'),
    go.Line(name = 'Highest_2001', x=highest_2001['States/ Union Territories'], y=highest_2001['Rural - 2001'], mode='markers')
])

fig7.update_layout(barmode='group', title = 'Lowest and highest "Rural literacy" rate in 2001 :')
#st.plotly_chart(fig7)

#Lowest and Highest of Rural in 2011
lowest_2011 = df.sort_values(by=['Rural - 2011']).head()
highest_2011 = df.sort_values(by=['Rural - 2011']).tail()

fig8 = go.Figure(data = [
    go.Line(name = 'Lowest_2011', x=lowest_2011['States/ Union Territories'], y=lowest_2011['Rural - 2011'], mode='markers'),
    go.Line(name = 'Highest_2011', x=highest_2011['States/ Union Territories'], y=highest_2011['Rural - 2011'], mode='markers')
])

fig8.update_layout(barmode='group', title = 'Lowest and highest "Rural literacy" rate in 2011 :')
#st.plotly_chart(fig8)


#Loest and Highest of Urban in 2001
lowest_2001 = df.sort_values(by=['Urban - 2001']).head()
highest_2001 = df.sort_values(by=['Urban - 2001']).tail()

fig9 = go.Figure(data = [
    go.Line(name = 'Lowest_2001', x=lowest_2011['States/ Union Territories'], y=lowest_2001['Urban - 2001'], mode='markers'),
    go.Line(name = 'Highest_2001', x=highest_2011['States/ Union Territories'], y=highest_2001['Urban - 2001'], mode='markers')
])

fig9.update_layout(barmode='group', title = 'Lowest and highest "Urban literacy" rate in 2001 :')
#st.plotly_chart(fig9)

#Lowest and Highest of Urban in 2011
lowest_2011 = df.sort_values(by=['Urban - 2011']).head()
highest_2011 = df.sort_values(by=['Urban - 2011']).tail()

fig10 = go.Figure(data = [
    go.Line(name = 'Lowest_2011', x=lowest_2011['States/ Union Territories'], y=lowest_2011['Urban - 2011'], mode='markers'),
    go.Line(name = 'Highest_2011', x=highest_2011['States/ Union Territories'], y=highest_2011['Urban - 2011'], mode='markers')
])

fig10.update_layout(barmode='group', title = 'Lowest and highest "Urban literacy" rate in 2011 :')
#st.plotly_chart(fig10)



#Per Change

#Per Change Total
fig11=px.bar(df.sort_values(by='Total - Per. Change'),
       x='States/ Union Territories', y='Total - Per. Change',
       color='Total - Per. Change', title='Totel Per. Change')
#st.plotly_chart(fig11)

#Per Change Rural
fig12=px.bar(df.sort_values(by='Rural - Per. Change'),
       x='States/ Union Territories', y='Rural - Per. Change',
       color='Rural - Per. Change', title='Rural Per. Change')
#st.plotly_chart(fig12)

#Per Change Urban
fig13=px.bar(df.sort_values(by='Urban - Per. Change'),
       x='States/ Union Territories', y='Urban - Per. Change',
       color='Urban - Per. Change', title='Urban Per. Change')
#st.plotly_chart(fig13)



#st.plotly_chart(fig14)

# Literacy Rate in each State/ Union Territory
df2 = pd.melt(df, id_vars='States/ Union Territories', value_vars=['Total - 2001', 'Total - 2011',
       'Rural - 2001', 'Rural - 2011', 'Urban - 2001', 'Urban - 2011',
       'Total - Per. Change', 'Rural - Per. Change', 'Urban - Per. Change'])
fig15 = px.bar(df2, 'variable', 'value', animation_frame='States/ Union Territories',
             color_discrete_sequence=['brown'])
fig15.update_layout(title='Literacy Rate of each State/ Union Territory.')
#st.plotly_chart(fig15)



# Region: East,West,North,South
East = ['Arunachal Pradesh','Assam','Jharkhand','West Bengal','Odisha',
        'Mizoram','Meghalaya','Manipur','Sikkim','Tripura','Nagaland']
West = ['Maharashtra','Gujarat','Goa']    
North = ['Uttar Pradesh','Bihar','Jammu & Kashmir','Rajasthan', 'Punjab','Haryana','Madhya Pradesh',
        'Chhattisgarh','Uttarakhand','NCT of Delhi','Tamil Nadu','Chandigarh','Himachal Pradesh',]
South = ['Andhra Pradesh','Karnataka','Kerala']

def zone_applier(x):
    if x in East :
        return 'East'
    elif x in West :
        return 'West'
    elif x in North :
        return 'North'
    else :
        return 'South'
    
State = df[df['Category']=='State']
State['Zone'] =State['States/ Union Territories'].apply(zone_applier)
State = State.groupby(by='Zone').agg('median')
State = State.iloc[:,:6]
State.reset_index(inplace=True)

State = State.T.reset_index()
State.columns = State.iloc[0,:]
State = State.iloc[1:,:]    

fig16 = go.Figure(data=[
    go.Bar(name='East', x=State['Zone'], y=State['East']),
    go.Bar(name='West', x=State['Zone'], y=State['West']),
    go.Bar(name='North', x=State['Zone'], y=State['North']),
    go.Bar(name='South', x=State['Zone'], y=State['South'])
])
fig16.update_layout(barmode='group', title='Avg. Literacy Rate by Zone:')
#st.plotly_chart(fig16)

fig17 = make_subplots(rows=2,cols=2)
fig17.add_trace(go.Bar(name='East', x=State['Zone'], y=State['East']), row=1,col=1)
fig17.add_trace(go.Bar(name='West', x=State['Zone'], y=State['West']), row=1, col=2)
fig17.add_trace(go.Bar(name='North', x=State['Zone'], y=State['North']), row=2, col=1)
fig17.add_trace(go.Bar(name='South', x=State['Zone'], y=State['South']), row=2, col=2)
#st.plotly_chart(fig17)

# st.tabs() - used to create tabs just like web browsers
select_options = option_menu(
        menu_title=None,
        options = ["Data", "Literacy Rate","Comparison","Region"],
        orientation="horizontal")

if select_options == "Data":
    
    #Checkbox of show data
    if st.checkbox('Show data'):
        st.write(df1) 

    # Overall Literacy Rates in India
    st.plotly_chart(fig)

    # BoxPlot
    st.plotly_chart(fig1)


if select_options == "Literacy Rate":

    #SElect Box of Literacy rate
    Select_group= st.selectbox('Literacy Rate of',
                            options=['Total','Rural' ,
                                        'Urban']
                            )
    if Select_group=='Total':
        # Total Literacy Rate Across Nation:
        st.plotly_chart(fig2)

    if Select_group=='Rural':
        #Rural Literacy Rate Across Nation:
        st.plotly_chart(fig3)

    if Select_group=='Urban':
        #Urban Literacy Rate Across Nation:
        st.plotly_chart(fig4)



    ##Select Box of Highest and Lowest literacy Rate
    Select_group= st.selectbox('Highest and Lowest Rate of',
                            options=['Total','Rural',
                                        'Urban']
                            )

    if Select_group=='Total' :
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
            #Lowest and Highest Total in 2001
                st.header("column 1")
                st.plotly_chart(fig5, use_container_width=True)

            with col2:
            #Lowest and Highest Total in 2011 
                st.header("column 2")
                st.plotly_chart(fig6, use_container_width=True)

    if Select_group=='Rural':
        with st.container():
            # create differet columns using columns() 
            col1, col2 = st.columns(2)
            with col1:
            #Lowest and Highest of Rural in 2001
                st.header("column 1")
                st.plotly_chart(fig7,use_container_width=True)

            with col2:
            #Lowest and Highest of Rural in 2011
                st.header("column 2")
                st.plotly_chart(fig8,use_container_width=True)
 
    if Select_group=='Urban':
        with st.container():
            # create differet columns using columns() 
            col1, col2 = st.columns(2)
            with col1:
            #Lowest and Highest of Urban in 2001
                st.header("column 1")
                st.plotly_chart(fig9,use_container_width=True)

            with col2:
            #Lowest and Highest of Urban in 2011
                st.header("column 2")
                st.plotly_chart(fig10,use_container_width=True)



    ##Select Box of per change in Literacy Rate
    Select_group= st.selectbox('Per.Change',
                            options=['Total','Rural' ,
                                        'Urban'])

    if Select_group=='Total':
        #Total Per Change
        st.plotly_chart(fig11)

    if Select_group=='Rural':
        #Rural Per Change
        st.plotly_chart(fig12)

    if Select_group=='Urban':
        #Urban Per change
        st.plotly_chart(fig13)

if select_options == "Comparison":
    # States vs Union Territories
    # States vs Union Territories
    temp_1 = df.groupby(by=['Category'])['Total - 2001'].mean().reset_index().T
    temp_2 = df.groupby(by=['Category'])['Total - 2011'].mean().reset_index().T

    temp_3 = df.groupby(by=['Category'])['Rural - 2001'].mean().reset_index().T
    temp_4 = df.groupby(by=['Category'])['Rural - 2011'].mean().reset_index().T

    temp_5 = df.groupby(by=['Category'])['Urban - 2001'].mean().reset_index().T
    temp_6 = df.groupby(by=['Category'])['Urban - 2011'].mean().reset_index().T

    frames = [temp_1, temp_2, temp_3, temp_4, temp_5, temp_6]
    temp = pd.concat(frames)
    loc = [0,1,3,5,7,9,11]
    temp = temp.iloc[loc,:]
    temp = temp.iloc[1:,:]
    temp.reset_index(inplace=True)
    temp.columns=['Category','State','Union Territory']

    fig14 = go.Figure(data = [
        go.Bar(name='States', y=temp['Category'], x=temp['State'], orientation='h', marker_color='rgb(26, 118, 255)'),
        go.Bar(name='Union Territories', y=temp['Category'], x=temp['Union Territory'], orientation='h', marker_color='rgb(55, 83, 109)')
    ])
    fig14.update_layout(barmode='group')

    st.plotly_chart(fig14)

    # Literacy Rate in each State/ Union Territory
    st.plotly_chart(fig15)

if select_options == "Region":
    # Region: East,West,North,South
    st.plotly_chart(fig16)

    st.plotly_chart(fig17)



