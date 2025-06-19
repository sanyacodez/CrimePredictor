from flask import Flask, request, render_template, redirect, url_for
from datetime import datetime
from pymongo import MongoClient
from utils.openrouteservice_safety import get_safest_route  # Keep if you use this function

app = Flask(__name__)

# MongoDB connection setup
try:
    client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
    # Trigger a server selection to verify connection
    client.server_info()
except Exception as e:
    print("❌ Could not connect to MongoDB:", e)
    raise e

db = client['crime_db']
incidents_collection = db['incidents']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        try:
            incident_type = request.form['type']
            date = request.form['date']
            time = request.form['time']
            lat = float(request.form['lat'])
            lng = float(request.form['lng'])

            incident = {
                'type': incident_type,
                'date': date,
                'time': time,
                'lat': lat,
                'lng': lng
            }

            incidents_collection.insert_one(incident)
            print(f"✅ Incident saved: {incident_type} at {lat}, {lng} on {date} {time}")

        except Exception as e:
            print("❌ Error saving incident to DB:", e)

        return redirect(url_for('home'))

    return render_template('report.html')

@app.route('/sos')
def sos():
    print("⚠️ SOS Triggered by User at", datetime.now())
    return render_template('sos.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/route', methods=['GET', 'POST'])
def route():
    if request.method == 'POST':
        try:
            start_lat = float(request.form['start_lat'])
            start_lng = float(request.form['start_lng'])
            end_lat = float(request.form['end_lat'])
            end_lng = float(request.form['end_lng'])

            result = get_safest_route((start_lng, start_lat), (end_lng, end_lat))
            return render_template('route.html', route=result["geojson"], risk=result["risk"])
        except Exception as e:
            print("❌ Error in route calculation:", e)
            return render_template('route.html', route=None, risk=None)

    return render_template('route.html', route=None, risk=None)

if __name__ == '__main__':
    app.run(port=5001, debug=True)
