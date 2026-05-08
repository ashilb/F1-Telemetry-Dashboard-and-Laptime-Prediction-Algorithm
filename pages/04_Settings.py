import streamlit as st

st.title("Settings")

st.divider()

#see toml file
st.write("To change between dark mode and light mode, see .toml file in the directory of this program")

st.divider()

driverList = ['ALB', 'ALO', 'BOT', 'GAS', 'HAM', 'HUL', 'LEC', 'MAG', 'NOR', 'OCO', 'PER', 'PIA', 'RIC', 'RUS', 'SAI', 'SAR', 'STR', 'TSU', 'VER', 'ZHO']

if 'favourite_driver' not in st.session_state:
    st.session_state['favourite_driver'] = driverList[0]

st.session_state['favourite_driver'] = st.selectbox("Select your Favourite Driver", driverList, index=driverList.index(st.session_state['favourite_driver']))

st.write("Your favourite driver is: " + st.session_state['favourite_driver'])


