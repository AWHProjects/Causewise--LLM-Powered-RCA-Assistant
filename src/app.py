from flask import Flask, render_template, request
from parser import parse_log
from llm import analyze_incident
from utils import save_uploaded_file
import os

# Configure Flask to find templates and static files in parent directory
app = Flask(__name__,
            template_folder='../templates',
            static_folder='../static')

@app.route('/', methods=['GET', 'POST'])
def home():
    analysis = None
    raw_log_data = None
    demo_type = None
    
    if request.method == 'POST':
        if 'demo_basic' in request.form:
            # Use basic incident log for demo
            sample_log_path = '../data/sample_incident.log'
            raw_log_data = parse_log(sample_log_path)
            analysis = analyze_incident(raw_log_data)
            demo_type = "Basic Log Format"
        elif 'demo_splunk' in request.form:
            # Use Splunk JSON format for demo
            sample_log_path = '../data/sample_splunk.json'
            raw_log_data = parse_log(sample_log_path)
            analysis = analyze_incident(raw_log_data)
            demo_type = "Splunk JSON Format"
        elif 'demo_complex' in request.form:
            # Use complex system log for demo
            sample_log_path = '../data/sample_complex.txt'
            raw_log_data = parse_log(sample_log_path)
            analysis = analyze_incident(raw_log_data)
            demo_type = "Complex System Log"
        elif 'incident_file' in request.files:
            uploaded_file = request.files['incident_file']
            if uploaded_file.filename:
                filepath = save_uploaded_file(uploaded_file)
                raw_log_data = parse_log(filepath)
                analysis = analyze_incident(raw_log_data)
                demo_type = f"Uploaded File: {uploaded_file.filename}"
    
    return render_template('index.html', analysis=analysis, raw_log_data=raw_log_data, demo_type=demo_type)

if __name__ == '__main__':
    app.run(debug=True)