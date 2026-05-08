import fastf1 as ff1
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib

ff1.Cache.enable_cache('f1_cache') 

#stores all the tracks in the 2024 F1 season in a list, this is used to retrieve the session data for each track
trackList = ["Sakhir", "Jeddah", "Melbourne", "Suzuka", "Shanghai", "Miami", "Imola", "Monaco", "Montréal", "Barcelona", "Spielberg", "Silverstone", "Budapest", "Spa-Francorchamps", "Zandvoort", "Monza", "Baku", "Marina Bay", "Austin", "Mexico City", "São Paulo", "Las Vegas", "Lusail", "Yas Island"]

#initialising an empty dataframe to store the session data for all tracks
sessiondf = None

#this loop retrieves the session data for each track in the trackList, extracts the relevant features and stores it in a sessiondf
for track in trackList:
    session = ff1.get_session(2024, track, 'Q')
    session.load()

    sessionLaps = session.laps[['Driver', 'Team', 'Compound', 'LapTime', 'TyreLife', 'IsAccurate']]

    lapsdf = pd.DataFrame(sessionLaps).insert(0, 'Circuit', track)
    sessionLaps['Circuit'] = track

    if sessiondf is None:
        sessiondf = sessionLaps
    else:
        sessiondf = pd.concat([sessiondf, sessionLaps], ignore_index=True)

#filters accurate laps only
sessiondf = sessiondf[sessiondf['IsAccurate'] == True]

#data is hot encoded to convert the categorical features into numerical features, so that the machine learning model can understand the data
sessiondf = pd.get_dummies(sessiondf, columns=['Circuit', 'Driver', 'Team', 'Compound'])

#y values
lapTimedf = sessiondf['LapTime'].dt.total_seconds()

#x values
featuresdf = sessiondf.drop(columns=['LapTime', 'IsAccurate'])

#data is slpit into a training set and a test set
X_train, X_test, y_train, y_test = train_test_split(featuresdf, lapTimedf, test_size=0.3, random_state=42)

#a random forest regression model is created and trained on the training data
model = RandomForestRegressor(n_estimators=200, random_state=42)

model.fit(X_train, y_train)


#trained model is used to predict time for test set
y_pred = model.predict(X_test)

# mean absolute error of model - calculates the efficiency of the model
mae = mean_absolute_error(y_test, y_pred) 

print("Evaluating Model...")

print(f'Mean Absolute Error: {mae:.2f} seconds')

#the trained model and the feature columns are saved using joblib
joblib.dump(model, 'data/model.pkl')

joblib.dump(featuresdf.columns.tolist(), 'data/feature_columns.pkl')


