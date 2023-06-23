import streamlit as st
import streamlit_survey as ss
import pandas as pd
import numpy as np
import plotly.express as px
from Utility_methods import PEMethod
import pycid
import requests
import country_converter as coco
from geopy.geocoders import Nominatim

# internal imports
from SCS_constants import DF_US, DF_EU, EU_objectives, DF_CN, draw_macid

  # Create a sidebar with US preferences
st.sidebar.markdown('**US preferences**\n\n'
                     '- Increase legitimacy of US actions through larger coalition\n'
                     '- Reduce burden on US in EA and IO\n'
                     '- Deter CN from aggression against TW (or other)\n'
                     '- Maintain relations with CN: Avoid military confrontation with CN\n'
                     '- Maintain relations with CN: Avoid economic confrontation with CN\n'
                     '- Maintain freedom of seas\n'
                     '- Deter Russia from aggression against NATO\n'
                     '- Defeat Russia if war in EA')
    
    
# Create a sidebar with CN preferences
st.sidebar.markdown('**CN preferences**\n\n'
                     '- Maintain relations with US: Avoid military confrontation with US\n'
                     '- Maintain relations with US: Avoid economic confrontation with US\n'
                     '- Avoid US aid to TW\n'
                     '- Limit US freedom of maneuver in WP\n'
                     '- Consolidate CN power in WP\n'
                     '- Maintain relations with ASEAN\n'
                     '- Maintain relations with EUR')

# rank hoe je denkt dat China deze dingen rankt.

# rank hoe belangrijk de VS vindt dat wij hier zijn

# hoe denkt de participant over China

# rank basic preferences

cc = coco.CountryConverter()
def convert_to_iso3(location):
    return cc.convert(names=str(location), to='ISO3')

def chloropleth_weapon_locations(df):
        
        df['ISO_A3'] = None
        df['Country_Location'] = None
        
        geolocator = Nominatim(user_agent="weapon_locations")
        # initialize country converter
        
        # Get countries from URL
        worldmap = requests.get("https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_admin_0_countries.geojson").json()

        df['ISO_A3'] = df['locations'].apply(lambda x: convert_to_iso3(x))
        figmap = px.choropleth_mapbox(
                    df,
                    locations="ISO_A3", # Based on this ID!
                    geojson=worldmap,
                    featureidkey="properties.ADM0_A3",
                    color='utility', # This is coloured!
                    color_continuous_scale='Blues',
                    hover_data=['utility'],
                    #animation_frame="date",
                    range_color=[20, 10],
                    title="Demo plotting utility on map",
                    mapbox_style="carto-positron",
                    center={"lat": 44.5260, "lon": 30.2551},
                    zoom=1
                )
        return figmap

def color_negative_red(value):
                if value < 0:
                    return 'background-color: red'
                elif value > 0:
                    return 'background-color: green'
                return ''

def get_column_with_positive_value(index, df):
    val = []
    for column in df.columns:
        if df.loc[index, column] > 0:
            val.append(column)
    return val

def get_column_with_negative_value(index, df):
    "Retreiveing the column names that store negative values"
    val = []
    for column in df.columns:
        
        if df.loc[index, column] < 0:
            val.append(column)
    return val
  
def get_column_with_neutral_value(index, df):
    val = []
    for column in df.columns:
        
        if df.loc[index, column] == 0:
            val.append(column)
    return val

# ----------------------------------------------------------------------------------------
def eliciting_belief(elements, page_nr, dx_dict, frame, start):
    new_frame = frame.copy()
    """
    For each action we need to rank the objectives in terms of effectiveness
    """
    domain_index = page_nr - start
    element = list(elements.values())
    
    title = element[domain_index] #table data -> options
    element = list(elements.keys())
    
    element = element[domain_index]

    options_positive = get_column_with_positive_value(element, frame)
    options_negative = get_column_with_negative_value(element, frame)

    survey = ss.StreamlitSurvey(f"Belief survey {element}")

    st.subheader(f"Given we choose action {title}, what is the likelihood of war?")
    survey.slider(f"Probability of war following {title}(%)", min_value=0, max_value=100, value=50)
    st.error("Here we need a type separating question to separate domain experts? I propose that this type separation question is the TYPE of China player.")

    survey.slider("Percentage of domain experts (%):", min_value=0, max_value=100, value=50, key = 'domain_exp1')
    
    if len(options_positive) > 1 or len(options_negative) > 1:
        st.subheader(f"The action: {title} may have positive or negative effects on the objectives. Please rank these objectives in order of strength of the relation.")
    
    save_col_pos = []
    # ranking the positive outcomes
    if len(list(options_positive)) > 1:
        st.subheader("Please rank the positive effects in terms of effectiveness:")
        options=[option for option in options_positive]
        if options:
            answer_1 = survey.radio(f"1st most strongly affected objective:", options=options, key=f"answer_1_{page_nr}")
            save_col_pos.append(answer_1)

        options=[option for option in options_positive if option != answer_1]

        if options: 
            answer_2 = survey.radio(f"2nd most strongly affected objective:", options=[option for option in options_positive if option != answer_1], key=f"answer_2_{page_nr}")
            save_col_pos.append(answer_2)

        options=[option for option in options_positive if option != answer_1 and option != answer_2]
        if options:
            answer_3 = survey.radio(f"3rd most strongly affected objective:", options=[option for option in options_positive if option != answer_1 and option != answer_2], key=f"answer_3_{page_nr}")
            save_col_pos.append(answer_3)

        options=[option for option in options_positive if option != answer_1 and option != answer_2 and option != answer_3]
        if options:
            answer_4 = survey.radio(f"4th most strongly affected objective:", options=[option for option in options_positive if option != answer_1 and option != answer_2 and option != answer_3], key=f"answer_4_{page_nr}")
            save_col_pos.append(answer_4)

    

    # ranking the negative objectives
    save_col_neg = []
    if len(list(options_negative)) > 1:
        st.subheader("Please rank the negative effects in terms of effectiveness:")
        answer_11 = survey.radio(f"1st most negatively affected objective:", options=list(options_negative), key=f"answer_11_{page_nr}")
        save_col_neg.append(answer_11)

        options = [option for option in options_negative if option != answer_11]
        if len(options) > 0:
            answer_22 = survey.radio(f"2nd most negatively affected objective:", options=options, key=f"answer_22_{page_nr}")
            save_col_neg.append(answer_22)

        options = [option for option in options_negative if option != answer_11 and option != answer_22]
        if len(options) > 0:
            answer_33 = survey.radio(f"3rd most negatively affected objective:", options=options, key=f"answer_33_{page_nr}")
            save_col_neg.append(answer_33)

        options = [option for option in options_negative if option != answer_11 and option != answer_22 and option != answer_33]
        if len(options) > 0:
            answer_44 = survey.radio(f"4th most negatively affected objective:", options=options, key=f"answer_44_{page_nr}")
            save_col_neg.append(answer_44)

    row = new_frame.loc[element]

    # Set the corresponding column values for positive values
    if save_col_pos:
        for i, column in enumerate(save_col_pos):
            row[save_col_pos[i]] =  len(save_col_pos) - i

    # Set the corresponding column values for negative values
    if save_col_neg:
        for i, column in enumerate(save_col_neg):
            row[save_col_neg[i]] = - len(save_col_neg) + i - 1

    
    return survey.to_json(), element, new_frame




# ------------------ The survey ---------------------------------------
def main():
    NEW_DF_US = DF_US
    NEW_DF_EU = DF_EU

    elements = ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9']
    json_beliefs = []
    #random.shuffle(elements)
    # Define the best and worst tuples
    best_tuple = ("(No ship)", "No war")
    worst_tuple = ("Blue vessel IO (most risky?)", "War")  
    # Replace "Scenario X" and "DY" with the actual worst outcome pair

    table_data = {
    "Options": ["Blue, IO, US(D1)", "Blue, IO, EU(D2)", 
                "Blue, WP, US(D3)", "Blue, WP, EU(D4)", 
                "Brown, IO, US (D5)", "Brown, IO, EU (D6)", 
                "Brown, WP, US (D7)", "Brown, WP, EU (D8)",
                "No ship (D9)"],
    "Titles": [
        "Blue vessel to Indian Ocean under US coalition",
        "Blue vessel to Indian Ocean under EU coalition",
        "Blue vessel to West Pacific under US coalition",
        "Blue vessel to West Pacific under EU coalition",
        "Brown vessel to Indian Ocean under US coalition",
        "Brown vessel to Indian Ocean under EU coalition",
        "Brown vessel to West Pacific under US coalition",
        "Brown vessel to West Pacific under EU coalition",
        "No ship"]
        }
    dictionary_data = {option: title for option, title in zip(table_data['Options'], table_data['Titles'])}

    # Define the list of options
    options = ["War", "No war"]
    
    # Create an empty list to store the randomized outcomes
    random_outcomes = []

    # Iterate over each domain (D) and each option (T)
    for D in table_data['Titles']:
        for T in options:
            # Check if the current outcome is the best or worst tuple
            if (T, D) != best_tuple and (T, D) != worst_tuple:
                random_outcomes.append((T, D))  # Add the outcome to the randomized list

    threat_level = None
    survey = ss.StreamlitSurvey("Survey Example")
    pages = survey.pages(35, on_submit=lambda: st.success("Your responses have been recorded. Thank you!"))
    with pages:
        if pages.current == 0:
            # Request personal information
            st.write("Welcome to the survey!")
            name = survey.text_input("What is your name?")
            age = survey.number_input("What is your age?", min_value=0, max_value=100)
            profile = survey.radio(
                    f"Profile",
                    options=["Domain expert", "Policy maker"]
                )
        elif pages.current == 1:
            st.header("Profile")
            st.write("""We need a description of the situation at hand""")
            st.write("long story short: The EU may take one out of 9 actions (decision node D2) after which China may respond with War/No war (decision node D1). Both players, the EU and China have a utility function that that assigns a utility to the actions taken by both players. The utility is measured by the objectives of the respective player.")
            st.image("maid_scs.png")

            st.header('Objectives')
            st.info("Please note that the color red indicates a negative effect, while green represents a positive effect on the objective. Later we assign a number (positive or negative) in order to indicate the strength of this effect.")
            st.subheader("US objectives")
            
            # Apply the formatting to the DataFrame using the Styler class
            styled_df = DF_US.style.applymap(color_negative_red)
            st.write(styled_df)

            st.subheader("EU objectives")
            styled_df = DF_EU.style.applymap(color_negative_red)
            st.write(styled_df)
            
            st.subheader("China objectives")
            st.error("This is a random table, this should be filled by a domain expert")
            styled_df = DF_CN.style.applymap(color_negative_red)
            st.write(styled_df)
            
        elif pages.current == 2:
            st.header("We need some question about the nature of the threat/tension level at the moment")
          
            
        elif pages.current == 3:

            st.header("Please read about the possible actions to take by the EU")
            st.table(table_data)
          
                        
        elif pages.current == 4:
            st.header("Measuring the risk profile")
            subtitle = """For each scenario decide whether you prefer the certainty of receiving 50 dollars, or to take a gamble with two possible outcomes. These two possible outcomes are either receiving 100 dollars or receiving nothing. The chance of ending up with either one of those options depends on a probability p, that lies between the scale of 0 and 100. Closer to 0 lowers the chance of ending up with that option, while moving towards 100 increases that chance.""" 
            st.write(subtitle)
            PE_Method = PEMethod(random_outcome="50 dollars", best_outcome="100 dollars", worst_outcome="0 dollars")
            pe_method = PE_Method.eliciting_utility(element = "pilot")
            survey.data["risk_profile"] = pe_method

            # initialize frame
            survey.data['new_DF_EU'] = DF_EU
            survey.data['new_DF_US'] = DF_US
            survey.data['new_DF_CN'] = DF_CN

        elif pages.current in range(5, 5+len(EU_objectives)):
            st.header("Ranking the EU objectives")
            frame = survey.data['new_DF_EU']
            json_belief, element, new_DF_EU = eliciting_belief(dictionary_data,pages.current, dictionary_data, frame, 5)
            survey.data['new_DF_EU'] = new_DF_EU
            survey.data[f"{element}_EU"] = json_belief
            

        elif pages.current in range(11 + 6): 
             st.header("Ranking the US objectives")
             frame = survey.data['new_DF_US']
             json_belief, element, new_DF_US = eliciting_belief(dictionary_data,pages.current, dictionary_data, frame, 11)
             survey.data[f"{element}_US"] = json_belief
             survey.data['new_DF_US'] = new_DF_US

        elif pages.current in range(18 + 7): 
             st.header("Ranking the CN objectives")
             frame = survey.data['new_DF_CN']
             json_belief, element, new_DF_CN = eliciting_belief(dictionary_data,pages.current, dictionary_data, frame, 18)
             survey.data[f"{element}_CN"] = json_belief
             survey.data['new_DF_CN'] = new_DF_CN


        elif pages.current == 26:
            st.subheader("Scaled US objectives for the policy maker")
            frame = survey.data['new_DF_US']
            styled_df = frame.style.applymap(color_negative_red)
            st.write(styled_df)

            st.subheader("Scaled EU objectives for the policy maker")
            frame = survey.data['new_DF_EU']
            styled_df = frame.style.applymap(color_negative_red)
            st.write(styled_df)

            st.subheader("Scaled CN objectives for the policy maker")
            frame = survey.data['new_DF_CN']
            styled_df = frame.style.applymap(color_negative_red)
            st.write(styled_df)

        elif pages.current == 27:
            st.subheader("Very simple demo game where the ship sending action leads to several utilities")
            
            macid = pycid.MACID(
                [("D2", "U1"), ("D", "D2"), ("D", "U2"), ("D", "U1"), ("D2", "U2")], 
                agent_decisions={1: ["D"], 2: ["D2"]},
                agent_utilities={1: ["U1"], 2: ["U2"]},
            )

            # specifying the domain of each decision variable
            d2_domain = [0, 1, 2, 3, 4, 5, 6, 7, 8] # each of the ship sending variations
            d3_domain = [0, 1] # war , no war

            agent1_payoff = survey.data['new_DF_EU'].values 
            agent2_payoff= survey.data['new_DF_CN'].values
            agent3_payoff= survey.data['new_DF_US'].values
            a1p = {d: np.sum(agent1_payoff[d]) for d in d2_domain}
            a2p = {d: np.sum(agent2_payoff[d]) for d in d2_domain}
            a3p = {d: np.sum(agent3_payoff[d]) for d in d2_domain}
            
            macid.add_cpds(
                D=d2_domain,
                D2 = d3_domain,
                U1= lambda D, D2: a1p[D]*D2,
                U2= lambda D, D2: a2p[D]*D2, 
                ) #U3 = lambda D: a3p[D]
            
            draw_macid(macid)
            macid.impute_fully_mixed_policy_profile() # we first must assign arbirtrary (but fully mixed) decision rules to all decision nodes
            #macid.expected_utility(context={"D": 3, "D2": 0}, agent=1)
            
            ship_action = survey.radio(f"Choose an action:", options=list(table_data['Titles']), key=f"ship action")
            index = list(table_data['Titles']).index(ship_action)
            index = int(index)

            st.write("expected utility for EU:")
            utilityEU = macid.expected_utility(context={"D": index, "D2": 1}, agent=1)
            st.write(utilityEU)

            st.write("expected utility for CN:")
            utilityCN = macid.expected_utility(context={"D": index, "D2": 1}, agent=2)
            st.write(utilityCN)


            eu_countries = [
            'Austria',
            'Belgium',
            'Bulgaria',
            'Croatia',
            'Cyprus',
            'Czech Republic',
            'Denmark',
            'Estonia',
            'Finland',
            'France',
            'Germany',
            'Greece',
            'Hungary',
            'Ireland',
            'Italy',
            'Latvia',
            'Lithuania',
            'Luxembourg',
            'Malta',
            'Netherlands',
            'Poland',
            'Portugal',
            'Romania',
            'Slovakia',
            'Slovenia',
            'Spain',
            'Sweden'
            ]

            df = pd.DataFrame({'locations': eu_countries})
            df['utility'] = utilityEU
            df.loc[len(df)] = ['China', utilityCN]
            figmap = chloropleth_weapon_locations(df)
            st.plotly_chart(figmap, width=6000)

            #st.write("expected utility agent 3:")
            #st.write(macid.expected_utility(context={"D": index, "D2": 0}, agent=3))

           


      
               
if __name__ == '__main__':
    main()


# st.header("Now we take a gamble between the worst case scenario and the best case scenario")
#             # -----------------------------------
#             # Get the domain (D) index from the page number
#             domain_index = pages.current - 5 
            
#             # ------------------------------------
#             random_outcome_index = (pages.current - 5) % len(EU_objectives)

#             # Force them to rank the outcomes - PE function assigns a utility of each outcome
#             # pick a best outcome
#             best_outcome = st.selectbox('Most important outcome to be fulfilled:', EU_objectives)
#             worst_outcome = st.selectbox('Least important outcome to be fulfilled:', [option for option in EU_objectives if option != best_outcome])


#             # Apply a standardized PE Method for the given strategy 
#             PE_Method = PEMethod(random_outcome=f"{EU_objectives[domain_index]}", best_outcome= best_outcome, worst_outcome= worst_outcome)
#             pe_method = PE_Method.eliciting_utility(element = EU_objectives[random_outcome_index], switching_only= True)

#             survey.data[str(EU_objectives[random_outcome_index])]  = pe_method

#             json = survey.to_json()