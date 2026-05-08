import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import fastf1 as ff1
#importing all the necessary libraries

session = None
#initalising session variable to None, this will be used to store the session data once it is loaded


#defining a dictionary to save tyre compounds to their respective colors for the tyre strategy chart
tyreColours = {
"SOFT": "red",
"MEDIUM": "yellow",
"HARD": "white",
"INTERMEDIATE": "green",
"WET": "blue"
}

ff1.Cache.enable_cache('f1_cache')  #enabling cache for the fastf1 library to speed up data retrieval

st.title("Telemetry Dashboard")
st.header("2024 F1 Season Telemetry Data")

try:
    schedule = ff1.get_event_schedule(2024, include_testing=False)  #retrieving the schedule for the 2024 F1 season
except Exception as e:
    st.error(f"Failed to load session data: {e}")
    st.stop()

#this function allows the user to select which race they want to view telemetry for, and also shows the schedule for the season 
def selectRace():

    if st.button("Show Schedule"):
        st.write(schedule[["Location", "Country", "OfficialEventName"]])

    st.button("Hide Schedule", type="primary")

    events = schedule["Location"]

    global selectedRace
    selectedRace = st.selectbox('Select which round you would like to view telemetry for:', events)

    st.write("You have selected the " + selectedRace + " round.")

selectRace()

#this function allows the user to select which session they want to view telemetry for
def selectSession():

    selectedEventFormat = schedule["EventFormat"][schedule["Location"] == selectedRace].values[0]
    
    global eventFormatUsed
    eventFormatUsed = " "

    if selectedEventFormat == "sprint_qualifying":
        eventFormatUsed = "Sprint Race Weekend"
    else:
        eventFormatUsed = "Regular Race Weekend"

    st.write("The format for the " + selectedRace + " round is " + eventFormatUsed)

    
    regWeek = ["FP1", "FP2", "FP3", "Qualifying", "Race"]
    sprintWeek = ["FP1", "Sprint Qualifying", "Sprint Race", "Qualifying", "Race"]

    global selectedSession
    selectedSession = st.selectbox("Select which session you would like to view telemetry for:", regWeek if eventFormatUsed == "Regular Race Weekend" else sprintWeek)

selectSession()

#this function retrieves the session data for the selected race and session
@st.cache_data(show_spinner=False)
def get_session_data(race, session_name):
    session = ff1.get_session(2024, race, session_name)
    with st.spinner("Loading..."):
        session.load(laps=True, telemetry=True, weather=True)
    return session

#this function formats the timedelta values in the session data to a more readable format
def format_timedelta(td):
    if pd.isnull(td):
        return ""
    total_seconds = td.total_seconds()
    hours = int(total_seconds // 3600) 
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    milliseconds = int((total_seconds - int(total_seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}:{milliseconds:03d}"

#this function highlights the user's favourite driver in the session data tables
def highlight_favourite(row, column):
    favourite = st.session_state.get('favourite_driver', None)
    if favourite and row[column] == favourite:
        return ['background-color: #C8FFAC; color: black'] * len(row)
    return [''] * len(row)


#this function loads the session data and displays it in a table, with the user's favourite driver highlighted
def loadSession():

    global session

    if st.button("Load Session Data"):
        with st.spinner("Loading the data..."):
            try:
                #loads the dataframe to the GUI
                session = get_session_data(selectedRace, selectedSession)
                laps_df = session.laps[["Driver", "DriverNumber", "Team", "Position", "LapTime", "LapNumber", "Compound", "Stint", "TyreLife", "Deleted", "DeletedReason", "IsAccurate"]].copy()
                laps_df = laps_df[laps_df["IsAccurate"] == True]
                laps_df["LapTime"] = laps_df["LapTime"].apply(format_timedelta)
                for col in ["Position", "LapNumber", "Stint", "TyreLife"]:
                    laps_df[col] = laps_df[col].fillna(0).astype(int)
            except Exception as e:
                st.error("Failed to load session data. Please check your internet connection.")
                return
        
        #highlights the user's favourite driver in the laps dataframe
        favourite = st.session_state.get('favourite_driver', None)
        if favourite:
            st.write(f"* Favourite driver **{favourite}** rows are highlighted in green.")
        st.dataframe(laps_df.style.apply(highlight_favourite, column='Driver', axis=1))

loadSession()


#this function creates a tyre strat graph where it displays the tyre compound every driver used in every single lap of the selected session
def tyreStrat():
    if session != None:
        st.divider()
        st.header("Tyre Strategy Chart")
        try:
            tyre_df = session.laps[['Driver', 'LapNumber', 'Compound', 'Stint']]
            fig = go.Figure()
            results_sorted = session.results.sort_values('Position')
            drivers_by_position = results_sorted['Abbreviation'].tolist()


            for driver in drivers_by_position:
                driver_data = tyre_df[tyre_df['Driver'] == driver]
                fig.add_trace(go.Scatter(
                    x=driver_data['LapNumber'],
                    y=driver_data['Driver'],
                    mode='lines+markers',
                    marker=dict(color=driver_data['Compound'].map(tyreColours)),
                    name=driver
                ))
           
            fig.update_layout(
                        height=800,
                        title='Tyre Strategy Chart',
                        xaxis_title='Lap Number',
                        yaxis_title='Driver',
                        yaxis=dict(categoryorder='array', categoryarray=list(reversed(drivers_by_position)))
            )
            st.plotly_chart(fig)
            st.write("SOFT : red , MEDIUM: yellow , HARD: white , INTERMEDIATE: green , WET: blue")
        except Exception as e:
            st.error("Failed to load tyre strategy data. Please check your internet connection.")


tyreStrat()

#this function displays the finishing order of the selected session, with the user's favourite driver highlighted
def finishingOrder():
    if session != None:
        st.divider()
        st.header("Session Results")
        try:
            finishingOrder = session.results[['Position', 'Abbreviation', 'DriverNumber', 'Points']]
            favourite = st.session_state.get('favourite_driver', None)
            finishingOrder['Position'] = finishingOrder['Position'].fillna(0).astype(int)
            finishingOrder['Points'] = finishingOrder['Points'].fillna(0).astype(int)
            if favourite:
                st.write(f"* Favourite driver **{favourite}** row is highlighted in green.")
            st.dataframe(finishingOrder.style.apply(highlight_favourite, column='Abbreviation', axis=1), hide_index=True)
        except Exception as e:
            st.error("Failed to load session results. Please check your internet connection.")

finishingOrder()
