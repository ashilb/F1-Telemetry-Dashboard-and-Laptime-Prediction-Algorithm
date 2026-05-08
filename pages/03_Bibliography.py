import streamlit as st

st.title("Bibiliography")

st.header("The following sources were used in the development of this program:")

st.write("Anthropic (2026) Claude (Claude Sonnet 4.6), available at: https://claude.ai - Claude (Anthropic, 2026) was used to provide guidance on project structure, explain programming concepts and suggest debugging strategies. All code was written and understood independently.")

st.write("Daniel Lewis (August 2023) Streamlit Cheat Sheet, available at https://cheat-sheet.streamlit.app/ - Used to understand all of the Streamlit commands used to code the GUI")

st.write(" Philipp Schäfer (2026) FastF1, available at https://docs.fastf1.dev/index.html# - The website is home to the FastF1 library. I used this website to research all commands, how they work and what they do.")

st.write("API design for machine learning software: experiences from the scikit-learn project, Buitinck et al., 2013 available at https://scikit-learn.org/stable/index.html# - This API was used to incorporate Random Forest Regression into the program")

st.write("Joblib Developers, Joblib: running Python functions as pipeline jobs available at https://joblib.readthedocs.io/en/latest/index.html - Used for saving and loading the trained random forest regressor model.")
 
st.write("Pandas Developers, pandas: Python Data Analysis Library available at https://pandas.pydata.org/docs/index.html - Used for manipulating and editing the dataframes in the program")
 
st.write("Plotly Developers, Plotly Open Source Graphing Library for Python (only used graph objects) available at https://plotly.com/python-api-reference/plotly.graph_objects.html - Used to display the tyre strat graph")

st.divider()

st.write("All API sources listed above have links directing to the documentation of the APIs which were used to develop this program. The documentation was used to understand how the APIs work, what commands they have and how to use those commands. The APIs were used to retrieve and manipulate data, train the machine learning model, save and load the model and create the GUI for the program.")