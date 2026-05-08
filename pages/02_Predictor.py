import streamlit as st
import fastf1 as ff1
import pandas as pd
import joblib


ff1.Cache.enable_cache('f1_cache')

st.title("Lap Time Predictor")

def load_model():
    model = joblib.load('data/model.pkl')
    feature_columns = joblib.load('data/feature_columns.pkl')
    return model, feature_columns

model, feature_columns = load_model()

trackList = ["Sakhir", "Jeddah", "Melbourne", "Suzuka", "Shanghai", "Miami", "Imola", "Monaco", "Montréal", "Barcelona", "Spielberg", "Silverstone", "Budapest", "Spa-Francorchamps", "Zandvoort", "Monza", "Baku", "Marina Bay", "Austin", "Mexico City", "São Paulo", "Las Vegas", "Lusail", "Yas Island"]


st.selectbox("Select Circuit", trackList, key='circuit')

st.selectbox("Select Driver", ['VER', 'PER', 'LEC', 'SAI', 'NOR', 'PIA', 'HAM', 'RUS', 'ALO', 'STR', 'GAS', 'OCO', 'HUL', 'MAG', 'TSU', 'RIC', 'ALB', 'SAR', 'ZHO', 'BOT'], key='driver')

driverTeams = {
    'VER': 'Red Bull Racing',
    'PER': 'Red Bull Racing',
    'LEC': 'Ferrari',
    'SAI': 'Ferrari',
    'NOR': 'McLaren',
    'PIA': 'McLaren',
    'HAM': 'Mercedes',
    'RUS': 'Mercedes',
    'ALO': 'Aston Martin',
    'STR': 'Aston Martin',
    'GAS': 'Alpine',
    'OCO': 'Alpine',
    'HUL': 'Haas',
    'MAG': 'Haas',
    'TSU': 'RB',
    'RIC': 'RB',
    'ALB': 'Williams',
    'SAR': 'Williams',
    'ZHO': 'Kick Sauber',
    'BOT': 'Kick Sauber'
}

team = driverTeams[st.session_state.driver]

st.write("Team auto-detected: " + team)

st.selectbox("Select Tyre Compound", ['SOFT', 'MEDIUM', 'HARD', 'INTERMEDIATE', 'WET'], key='compound')

st.number_input("Tyre Life", min_value=1, max_value=70, key='tyre_life') 

if st.button("Predict Lap Time"):
    input_data = {
        'Circuit': st.session_state.circuit,
        'Driver': st.session_state.driver,
        'Team': team,
        'Compound': st.session_state.compound,
        'TyreLife': st.session_state.tyre_life,
    }

    input_df = pd.DataFrame.from_dict([input_data])

    input_df = pd.get_dummies(input_df, columns=['Circuit', 'Driver', 'Team', 'Compound']) 

    input_df = input_df.reindex(columns=feature_columns, fill_value=0)
    predicted_time = model.predict(input_df)[0]
    minutes = int(predicted_time // 60)
    seconds = int(predicted_time % 60)
    milliseconds = int((predicted_time - int(predicted_time)) * 1000)

    st.markdown(f"<span style='color:green; font-weight:bold'>Predicted Lap Time: {minutes:02d}:{seconds:02d}:{milliseconds:03d}</span>", unsafe_allow_html=True)
    st.write(f"Note: Prediction accuracy may vary by ±1.5 seconds.")
