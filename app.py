from flask import Flask, request, render_template
import joblib
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import random

app = Flask(__name__)

# Custom class used for saving models (for backward compatibility)
class PredictionModel:
    def __init__(self, model, features, acc):
        self.model = model
        self.features = features
        self.acc = acc

    def predict(self, X):
        return self.model.predict(X)

# Load models
crime_model = joblib.load('model/suraksha_app_model_crime_pred_area.pkl')
safety_model = joblib.load('model/suraksha_app_model_safety.pkl')

# Load dataset
df = pd.read_excel("data/New_Delhi_crime.xlsx")

# Fit Nearest Neighbors model
coordinates = df[['Latitude', 'Longitude']]
area_codes = df['Delhi_Cluster_code_encode']
nn_model = NearestNeighbors(n_neighbors=1)
nn_model.fit(coordinates)

# Severity mapping
severity_map = {'low': 0, 'med': 1, 'medium': 1, 'high': 2}

# Suggestion map for top crimes
crime_suggestions = {
    'snatch': "Install more street CCTV cameras, improve street lighting, and increase police patrolling in the evening.",
    'stalk': "Establish safe zones, run community awareness campaigns, and deploy undercover patrol units.",
    'grop': "Increase presence of women officers, promote use of panic button apps, and ensure security at crowded transit spots.",
    'assault': "Set up emergency response booths, fast-track legal aid access, and conduct regular safety audits.",
    'catcall': "Launch public awareness drives, set up whistleblower helplines, and enforce strict anti-harassment laws.",
    'abuse': "Partner with NGOs, set up counseling and reporting centers, and enforce strict area-wise monitoring.",
    'touch': "Increase surveillance in crowded areas, install security alarms in buses/trains, and educate public on reporting abuse.",
    'comment': "Implement behavioral change campaigns in schools/colleges and increase community policing.",
    'whistle': "Introduce anti-harassment signage and train local shopkeepers to report incidents.",
    'lewd': "Encourage local residents to participate in safety watch groups and increase visibility of law enforcement."
}

def get_area_code(lat, lng, max_distance=0.05):
    distance, index = nn_model.kneighbors([[lat, lng]])
    if distance[0][0] > max_distance:
        return None
    return area_codes.iloc[index[0][0]]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        lat = float(request.form['lat'])
        lng = float(request.form['lng'])

        area_code = get_area_code(lat, lng)
        if area_code is None:
            return render_template('result.html',
                                   location=f"Lat: {lat:.4f}, Lng: {lng:.4f}",
                                   crime="N/A",
                                   safety="N/A",
                                   causes=["Location outside Delhi area. Please select a location within Delhi."],
                                   crime_percentages={},
                                   suggestions=[])

        area_df = df[df['Delhi_Cluster_code_encode'] == area_code]

        if area_df.empty:
            return render_template('result.html',
                                   location=f"Lat: {lat:.4f}, Lng: {lng:.4f}",
                                   crime="N/A",
                                   safety="N/A",
                                   causes=["No crime data available for this location."],
                                   crime_percentages={},
                                   suggestions=[])

        sample_row = area_df.sample(1).iloc[0]
        severity_raw = str(sample_row.get('Severity_index', 'low')).strip().lower()
        severity_value = severity_map.get(severity_raw, 0)

        input_features = {
            'Delhi_Cluster_code_encode': area_code,
            'year': int(sample_row.get('year', 2023)),
            'month': int(sample_row.get('month', 1)),
            'day': int(sample_row.get('day', 1)),
            'dayofweek': int(sample_row.get('dayofweek', 1)),
            'time_hour': int(sample_row.get('time_hour', 12)),
            'dayofyear': int(sample_row.get('dayofyear', 1)),
            'Severity_index': severity_value
        }

        if hasattr(crime_model, 'features') and 'Area' in crime_model.features:
            input_features['Area'] = str(sample_row.get('Area', 'Unknown'))

        input_df = pd.DataFrame([input_features])
        crime_prediction = crime_model.predict(input_df)[0]
        safety_prediction = safety_model.predict(input_df)[0]

        safety_result = "Unsafe" if safety_prediction else "Safe"
        crime_result = "High Risk" if (safety_result == "Unsafe" and crime_prediction) else "Low Risk"

        incident_col = 'Incident Category' if 'Incident Category' in area_df.columns else 'Category'

        # Top causes
        if safety_result == "Safe":
            keywords = ['comment', 'catcall', 'whistle', 'ogle', 'stare', 'lewd']
        else:
            keywords = ['touch', 'grop', 'stalk', 'assault', 'snatch', 'follow', 'abuse']

        top_causes = area_df[area_df[incident_col]
                             .str.lower()
                             .str.contains('|'.join(keywords))][incident_col] \
                             .value_counts().head(3).index.tolist()

        if not top_causes:
            top_causes = area_df[incident_col].value_counts().head(3).index.tolist()

        # Crime percentage
        total_crimes = area_df[incident_col].value_counts()
        crime_percentage = (total_crimes / total_crimes.sum() * 100).round(2).to_dict()

        # Suggestions based on top crimes
        suggestions = []
        for cause in top_causes:
            cause_lower = cause.lower()
            found = False
            for keyword in crime_suggestions:
                if keyword in cause_lower:
                    suggestions.append(crime_suggestions[keyword])
                    found = True
                    break
            if not found:
                suggestions.append("Promote community engagement and local safety campaigns.")

        return render_template('result.html',
                               location=f"Lat: {lat:.4f}, Lng: {lng:.4f}",
                               crime=crime_result,
                               safety=safety_result,
                               causes=top_causes,
                               crime_percentages=crime_percentage,
                               suggestions=suggestions)

    except Exception as e:
        print(f"Error: {e}")
        return render_template('result.html',
                               location="Error",
                               crime="Error",
                               safety="Error",
                               causes=[f"An error occurred: {str(e)}"],
                               crime_percentages={},
                               suggestions=[])

if __name__ == '__main__':
    app.run(debug=True, port=5001)

