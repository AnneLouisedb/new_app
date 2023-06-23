import streamlit as st
st.set_page_config(layout="wide", page_title="SCS")
#import libraries
import plotly.express as px
import pandas as pd
import requests


IP = ['AUS', 'BRN', 'KHM', 'FJI', 'IDN', 'JPN', 'KIR', 'MYS', 'MHL', 'FSM', 'NRU', 'NZL', 'NIU', 'PRK', 'PLW', 'PNG', 'PHL', 'WSM', 'SGP', 'SLB', 'KOR', 'TZA', 'THA', 'TLS', 'TON', 'TUV', 'VUT', 'VNM']

vessels_dict = {"Blue water vessel": "serious warfighting capability [simplified]", "Brown water vessel": "law enforcement capability [simplified]"}

flags_dict = {"NAT": "national", "EU": "European Union", "US": "US"}

#------------------------------------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------------------------------------------------------
def app():

    # get countries from url
    worldmap = requests.get(
            "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_admin_0_countries.geojson"
            ).json()


     # simulate dataframe,  don't to local file
    Final = pd.DataFrame(
            {
                "ISO_A3": [f["properties"]["ADM0_A3"] for f in worldmap["features"]],
                "Risk" : [10 for f in worldmap["features"]]
            }
        )
    
    
    # Create a sidebar with US preferences
    st.sidebar.markdown('**US preferences**\n\n'
                     '- Increase legitimacy of US actions through larger coalition\n'
                     '- Reduce burden on US in EA and IO\n'
                     '- Deter CN from aggression against TW (or other)\n'
                     '- Maintain relations with CN: Avoid military confrontation with CN\n'
                     '- Maintain relations with CN: Avoid economic confrontation with CN\n'
                     '- Maintain freedom of seas\n'
                     '- Deter RUS from aggression against NATO\n'
                     '- Defeat RUS if war in EA')
    
    
    # Create a sidebar with CN preferences
    st.sidebar.markdown('**CN preferences**\n\n'
                     '- Maintain relations with US: Avoid military confrontation with US\n'
                     '- Maintain relations with US: Avoid economic confrontation with US\n'
                     '- Avoid US aid to TW\n'
                     '- Limit US freedom of maneuver in WP\n'
                     '- Consolidate CN power in WP\n'
                     '- Maintain relations with ASEAN\n'
                     '- Maintain relations with EUR')
   
    st.title('Demo')
    st.write('''  
            Which ships should EUR send alongside whom to accomplish what at which cost? Both which other EUR, US, and which ASIAN states?    
            ''')
    # clarify policy trade-offs
  
    # Define the list of agents and their preferences
    agents = {
        "EUR": ["Deter CN from aggression against TW", "Strengthen relations with US", "Maintain relations with ASEAN", "more"],
        "ASIAN": ["EUR BLUE presence", "EUR Brown presence", "Deter CN from agression against TW", 'more']
    }
    # ---------------------
    capabilities = [
    "Send BLUE ship to WP",
    "Send BROWN ship to WP",
    "Send BLUE ship to IO",
    "Send BROWN ship to IO",
    "Keep ALL BLUE ships in EA, send NO BLUE ships to IP"
    ]

    
    
    # -------------------

    # Display a dropdown menu for the user to select an agent
    selected_agent = st.selectbox("Select an agent:", list(agents.keys()))

    # Display the selected agent's preferences
    selected_preferences = agents[selected_agent]

    st.write("Agent preferences:", selected_preferences)
    if selected_agent == "EUR":
        st.write("""Outcomes:\n
            Deter CN from aggression against TW (or other) \n
            Strengthen relations with US \n
            Reassure regional states \n
            Maintain freedom of seas """)
        selected_ship= st.selectbox("Vessel:", vessels_dict.keys())
        st.write(vessels_dict[selected_ship])
        selected_region = st.selectbox("Send to",["IO", "WP"])
        if selected_region ==  "WP":
            WP = ['AUS', 'CHN', 'JPN', 'PHL', 'KOR', 'TWN', 'VNM', 'PNG', 'IDN', 'MYS']
            # Filter the dataframe based on the selected region
            Final = Final[Final["ISO_A3"].isin(WP)]
            # filter dataframe on these countries
            # Add a circle shape around the Indian Ocean region
            figmap = px.choropleth(
            Final,
            locations="ISO_A3",
            color="Risk",
            color_continuous_scale="Blues",
            #animation_frame="Date",
            range_color=[20, 10],
            title="Risk score",
            )
            
     
        else:
            figmap = px.choropleth(
            Final,
            locations="ISO_A3",
            color="Risk",
            color_continuous_scale="Blues",
            #animation_frame="Date",
            range_color=[20, 10],
            title="Risk score",
            ) 
            figmap.add_shape(type='circle',
                        xref='paper', yref='paper',
                        x0=0.5, y0=0.2, x1=0.9, y1=0.5,
                        line=dict(color='red', width=3),
                        opacity=0.3)
            
        selected_flag = st.selectbox("Under flag:", flags_dict.keys())
        st.write("Implications of this coalition are .... bla bla bla")

            # now colour countries in WP
            # now colour countries in the IO
    else:
        pass
    
    # -------------------------------------------------------------------------------------------------------------------------------
      
   
    #'Value of goods in USD'
    # plot the weapons instead of the co2 emissions using this geojson
    
        
  
    # figmap = px.choropleth_mapbox(
    #     Final,
    #     locations="ISO_A3",
    #     geojson=worldmap,
    #     featureidkey="properties.ADM0_A3",
    #     color="Risk",
    #     color_continuous_scale='Blues',
    #     hover_data=["ISO_A3"],
    #     #animation_frame="Date",
    #     range_color=[20, 10],
    #     title="Risk score",
    #     mapbox_style="carto-positron",
    #     )

   
    st.plotly_chart(figmap, width=1000000)


# ------------------------------------------------------Horizontal box 1---------------------------------------------------------------------------------------------------
   
    
# ------------------------------------------------------Horizontal box 1---------------------------------------------------------------------------------------------------
   
#Run app
app()