# Crime Predictor App

## Overview
The Crime Predictor App is a web-based platform designed to predict crime risk, suggest safety measures, and assist users in reporting incidents or finding safer routes within New Delhi. It leverages machine learning models, real crime data, and geospatial analysis to provide actionable safety insights for both users and administrators.

## Features
- **Crime Risk Prediction:** Predicts the risk level (High/Low) and safety status (Safe/Unsafe) for a selected location and time in Delhi.
- **Incident Reporting:** Allows users to report crime incidents with type, date, time, and location.
- **SOS Alert:** Users can trigger an SOS alert for emergencies.
- **Safe Route Finder:** Computes and displays the safest walking route between two points, considering crime data along the path.
- **Admin Reports:** Admins can view submitted reports and prediction analytics.
- **AI Chat Assistant:** Users can interact with an AI assistant for safety-related queries.

## Directory Structure
```
crime_predictor_app/
│   app.py                  # Main Flask app for crime prediction and admin
│   requirements.txt        # Python dependencies
│
├── data/
│   └── New_Delhi_crime.xlsx         # Crime dataset for Delhi
│
├── model/
│   ├── suraksha_app_model_crime_pred_area.pkl   # Crime prediction model
│   └── suraksha_app_model_safety.pkl           # Safety prediction model
│
├── templates/              # Admin/main app HTML templates
│   ├── admin_reports.html
│   ├── heatmap.html
│   ├── heatmap_content.html
│   ├── index.html
│   └── result.html
│
├── user_app/
│   ├── __init__.py
│   ├── incident_log.csv
│   ├── New_Delhi_crime.xlsx
│   ├── user_server.py      # User-facing Flask app
│   ├── static/
│   │   ├── images/
│   │   │   └── IMG_7940.PNG
│   │   └── style.css
│   ├── templates/          # User-facing HTML templates
│   │   ├── chat.html
│   │   ├── index.html
│   │   ├── report.html
│   │   ├── route.html
│   │   └── sos.html
│   └── utils/
│       └── openrouteservice_safety.py
│
└── venv/                   # Python virtual environment (not included)
```

## Setup Instructions
### Prerequisites
- Python 3.8+
- pip (Python package manager)
- MongoDB (for incident logging)
- [OpenRouteService API key](https://openrouteservice.org/sign-up/) (for safe route feature)

### Installation
1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd crime_predictor_app
   ```
2. **Create and activate a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install geopandas openrouteservice pymongo shapely
   ```
4. **Set up MongoDB:**
   - Ensure MongoDB is running locally on the default port (27017).
   - No extra setup is needed for development.
5. **Download/Place Models and Data:**
   - Ensure the `model/` and `data/` folders contain the required `.pkl` and `.xlsx` files.
   - If using the safe route feature, update your OpenRouteService API key in `user_app/utils/openrouteservice_safety.py`.

## Usage
### 1. Main Crime Prediction App (Admin/Analytics)
Run the main Flask app:
```bash
python app.py
```
- Access at: [http://localhost:5001](http://localhost:5001)
- Features: Crime prediction, analytics, admin reports.

### 2. User App (Reporting, SOS, Safe Route, Chat)
Run the user-facing Flask app:
```bash
cd user_app
python user_server.py
```
- Access at: [http://localhost:5001](http://localhost:5001)
- Features: Incident reporting, SOS, safe route, AI chat.

## Dependencies
- Flask
- scikit-learn
- pandas
- numpy
- joblib
- geopandas
- openrouteservice
- pymongo
- shapely
- Jinja2
- (See `requirements.txt` for full list)

## Notes
- The app is designed for New Delhi and uses a real crime dataset for predictions.
- The safe route feature requires a valid OpenRouteService API key.
- MongoDB is required for logging user-reported incidents.
- For production, security and deployment settings should be reviewed.

## Credits
- Crime data: [Source as per your dataset]
- Route safety: [OpenRouteService](https://openrouteservice.org/)
- Developed by: [Sanya Vashsith] 