from flask import Flask, render_template, request, jsonify
from parser import parse_log
from llm import analyze_incident, validate_llm_connection
from utils import save_uploaded_file
from system_monitor import monitor
import os
import threading
import time

# Configure Flask to find templates and static files in parent directory
app = Flask(__name__,
            template_folder='../templates',
            static_folder='../static')

# Global variables for progress tracking
progress_data = {'percent': 0, 'message': 'Ready', 'processing': False}

def progress_callback(percent, message):
    """Callback function for progress updates"""
    global progress_data
    progress_data = {'percent': percent, 'message': message, 'processing': percent < 100}

@app.route('/')
def home():
    # Get system stats for display
    system_stats = monitor.get_current_stats()
    process_info = monitor.get_process_info()
    
    return render_template('index.html',
                         system_stats=system_stats,
                         process_info=process_info)

@app.route('/analyze', methods=['POST'])
def analyze():
    global progress_data
    analysis = None
    raw_log_data = None
    demo_type = None
    
    # Reset progress
    progress_data = {'percent': 0, 'message': 'Starting analysis...', 'processing': True}
    
    try:
        if 'demo_basic' in request.form:
            # Use basic incident log for demo
            sample_log_path = '../data/sample_incident.log'
            raw_log_data = parse_log(sample_log_path)
            analysis = analyze_incident(raw_log_data, progress_callback)
            demo_type = "Basic Log Format"
        elif 'demo_splunk' in request.form:
            # Use Splunk JSON format for demo
            sample_log_path = '../data/sample_splunk.json'
            raw_log_data = parse_log(sample_log_path)
            analysis = analyze_incident(raw_log_data, progress_callback)
            demo_type = "Splunk JSON Format"
        elif 'demo_complex' in request.form:
            # Use complex system log for demo
            sample_log_path = '../data/sample_complex.txt'
            raw_log_data = parse_log(sample_log_path)
            analysis = analyze_incident(raw_log_data, progress_callback)
            demo_type = "Complex System Log"
        elif 'demo_cisco' in request.form:
            # Use Cisco log format for demo
            sample_log_path = '../data/sample_cisco.log'
            raw_log_data = parse_log(sample_log_path)
            analysis = analyze_incident(raw_log_data, progress_callback)
            demo_type = "Cisco Network Log"
        elif 'demo_polycom' in request.form:
            # Use Polycom log format for demo
            sample_log_path = '../data/sample_polycom.log'
            raw_log_data = parse_log(sample_log_path)
            analysis = analyze_incident(raw_log_data, progress_callback)
            demo_type = "Polycom VoIP Log"
        elif 'incident_file' in request.files:
            uploaded_file = request.files['incident_file']
            if uploaded_file.filename:
                filepath = save_uploaded_file(uploaded_file)
                raw_log_data = parse_log(filepath)
                analysis = analyze_incident(raw_log_data, progress_callback)
                demo_type = f"Uploaded File: {uploaded_file.filename}"
    
        # Get updated system stats after processing
        system_stats = monitor.get_current_stats()
        process_info = monitor.get_process_info()
        
        return render_template('index.html',
                             analysis=analysis,
                             raw_log_data=raw_log_data,
                             demo_type=demo_type,
                             system_stats=system_stats,
                             process_info=process_info)
    
    except Exception as e:
        progress_data = {'percent': 100, 'message': f'Error: {str(e)}', 'processing': False}
        return render_template('index.html',
                             error=str(e),
                             system_stats=monitor.get_current_stats(),
                             process_info=monitor.get_process_info())

@app.route('/progress')
def get_progress():
    """API endpoint for progress updates"""
    return jsonify(progress_data)

@app.route('/system_stats')
def get_system_stats():
    """API endpoint for real-time system statistics"""
    return jsonify({
        'system': monitor.get_current_stats(),
        'process': monitor.get_process_info()
    })

@app.route('/validate_llm')
def validate_llm():
    """API endpoint for LLM validation testing"""
    validation_result = validate_llm_connection()
    return jsonify(validation_result)

if __name__ == '__main__':
    app.run(debug=True)