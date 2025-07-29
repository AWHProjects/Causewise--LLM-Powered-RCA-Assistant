from flask import Flask, render_template, request, jsonify
from markupsafe import escape
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from parser import parse_log
from llm import analyze_incident, validate_llm_connection, parse_analysis_output
from utils import save_uploaded_file
from system_monitor import monitor
import os
import threading
import time
import logging
import secrets
from functools import wraps
from werkzeug.exceptions import RequestEntityTooLarge

# Configure secure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('security.log'),
        logging.StreamHandler()
    ]
)
security_logger = logging.getLogger('security')

# Configure Flask to find templates and static files in parent directory
app = Flask(__name__,
            template_folder='../templates',
            static_folder='../static')

# Security configuration
app.config['SECRET_KEY'] = secrets.token_hex(32)  # Generate secure secret key
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max request size

# Initialize rate limiter
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

# Global variables for progress tracking
progress_data = {'percent': 0, 'message': 'Ready', 'processing': False}

def security_headers(response):
    """Add security headers to all responses"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'"
    return response

app.after_request(security_headers)

def log_security_event(event_type, details, ip_address):
    """Log security events for monitoring"""
    security_logger.warning(f"SECURITY EVENT: {event_type} - IP: {ip_address} - Details: {details}")

def validate_input(data, max_length=1000):
    """Validate and sanitize input data"""
    if not data:
        return ""
    
    # Convert to string and limit length
    data_str = str(data)[:max_length]
    
    # Basic XSS prevention - escape HTML
    return escape(data_str)

def progress_callback(percent, message):
    """Callback function for progress updates"""
    global progress_data
    # Sanitize progress message
    safe_message = validate_input(message, 200)
    progress_data = {'percent': percent, 'message': safe_message, 'processing': percent < 100}

@app.errorhandler(413)
@app.errorhandler(RequestEntityTooLarge)
def handle_file_too_large(e):
    """Handle file upload size limit exceeded"""
    log_security_event("FILE_TOO_LARGE", "File upload exceeded size limit", request.remote_addr)
    return render_template('index.html',
                         error="File too large. Maximum size allowed is 10MB.",
                         system_stats=monitor.get_current_stats(),
                         process_info=monitor.get_process_info()), 413

@app.errorhandler(429)
def handle_rate_limit(e):
    """Handle rate limit exceeded"""
    log_security_event("RATE_LIMIT_EXCEEDED", str(e), request.remote_addr)
    return jsonify({"error": "Rate limit exceeded. Please try again later."}), 429

@app.errorhandler(Exception)
def handle_general_error(e):
    """Handle general errors without exposing system details"""
    log_security_event("GENERAL_ERROR", f"Error type: {type(e).__name__}", request.remote_addr)
    # Don't expose detailed error information to users
    return render_template('index.html',
                         error="An error occurred while processing your request. Please try again.",
                         system_stats=monitor.get_current_stats(),
                         process_info=monitor.get_process_info()), 500

@app.route('/')
@limiter.limit("30 per minute")
def home():
    try:
        # Get system stats for display
        system_stats = monitor.get_current_stats()
        process_info = monitor.get_process_info()
        
        return render_template('index.html',
                             system_stats=system_stats,
                             process_info=process_info)
    except Exception as e:
        log_security_event("HOME_ERROR", str(e), request.remote_addr)
        return render_template('index.html',
                             error="Unable to load system information.",
                             system_stats={},
                             process_info={})

@app.route('/analyze', methods=['POST'])
@limiter.limit("10 per minute")
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
            log_security_event("DEMO_ANALYSIS", "Basic log demo used", request.remote_addr)
            
        elif 'demo_splunk' in request.form:
            # Use Splunk JSON format for demo
            sample_log_path = '../data/sample_splunk.json'
            raw_log_data = parse_log(sample_log_path)
            analysis = analyze_incident(raw_log_data, progress_callback)
            demo_type = "Splunk JSON Format"
            log_security_event("DEMO_ANALYSIS", "Splunk demo used", request.remote_addr)
            
        elif 'demo_complex' in request.form:
            # Use complex system log for demo
            sample_log_path = '../data/sample_complex.txt'
            raw_log_data = parse_log(sample_log_path)
            analysis = analyze_incident(raw_log_data, progress_callback)
            demo_type = "Complex System Log"
            log_security_event("DEMO_ANALYSIS", "Complex demo used", request.remote_addr)
            
        elif 'demo_cisco' in request.form:
            # Use Cisco log format for demo
            sample_log_path = '../data/sample_cisco.log'
            raw_log_data = parse_log(sample_log_path)
            analysis = analyze_incident(raw_log_data, progress_callback)
            demo_type = "Cisco Network Log"
            log_security_event("DEMO_ANALYSIS", "Cisco demo used", request.remote_addr)
            
        elif 'demo_polycom' in request.form:
            # Use Polycom log format for demo
            sample_log_path = '../data/sample_polycom.log'
            raw_log_data = parse_log(sample_log_path)
            analysis = analyze_incident(raw_log_data, progress_callback)
            demo_type = "Polycom VoIP Log"
            log_security_event("DEMO_ANALYSIS", "Polycom demo used", request.remote_addr)
            
        elif 'incident_file' in request.files:
            uploaded_file = request.files['incident_file']
            if uploaded_file.filename:
                try:
                    # Secure file upload with validation
                    filepath = save_uploaded_file(uploaded_file)
                    raw_log_data = parse_log(filepath)
                    analysis = analyze_incident(raw_log_data, progress_callback)
                    
                    # Sanitize filename for display
                    safe_filename = validate_input(uploaded_file.filename, 100)
                    demo_type = f"Uploaded File: {safe_filename}"
                    
                    log_security_event("FILE_UPLOAD", f"File uploaded: {safe_filename}", request.remote_addr)
                    
                except ValueError as ve:
                    # Security validation failed
                    log_security_event("FILE_UPLOAD_REJECTED", str(ve), request.remote_addr)
                    progress_data = {'percent': 100, 'message': 'Upload rejected', 'processing': False}
                    return render_template('index.html',
                                         error=f"File upload failed: {str(ve)}",
                                         system_stats=monitor.get_current_stats(),
                                         process_info=monitor.get_process_info())
    
        # Parse the analysis output into structured components
        parsed_analysis = None
        if analysis:
            parsed_analysis = parse_analysis_output(analysis)
        
        # Get updated system stats after processing
        system_stats = monitor.get_current_stats()
        process_info = monitor.get_process_info()
        
        return render_template('index.html',
                             analysis=analysis,
                             parsed_analysis=parsed_analysis,
                             raw_log_data=raw_log_data,
                             demo_type=demo_type,
                             system_stats=system_stats,
                             process_info=process_info)
    
    except Exception as e:
        log_security_event("ANALYSIS_ERROR", f"Analysis failed: {type(e).__name__}", request.remote_addr)
        progress_data = {'percent': 100, 'message': 'Analysis failed', 'processing': False}
        return render_template('index.html',
                             error="Analysis failed. Please check your file format and try again.",
                             system_stats=monitor.get_current_stats(),
                             process_info=monitor.get_process_info())

@app.route('/progress')
@limiter.limit("60 per minute")
def get_progress():
    """API endpoint for progress updates"""
    return jsonify(progress_data)

@app.route('/system_stats')
@limiter.limit("60 per minute")
def get_system_stats():
    """API endpoint for real-time system statistics"""
    try:
        return jsonify({
            'system': monitor.get_current_stats(),
            'process': monitor.get_process_info()
        })
    except Exception as e:
        log_security_event("SYSTEM_STATS_ERROR", str(e), request.remote_addr)
        return jsonify({'error': 'Unable to retrieve system statistics'}), 500

@app.route('/validate_llm')
@limiter.limit("5 per minute")
def validate_llm():
    """API endpoint for LLM validation testing"""
    try:
        validation_result = validate_llm_connection()
        log_security_event("LLM_VALIDATION", "LLM validation requested", request.remote_addr)
        return jsonify(validation_result)
    except Exception as e:
        log_security_event("LLM_VALIDATION_ERROR", str(e), request.remote_addr)
        return jsonify({'error': 'LLM validation failed', 'status': 'error'}), 500

if __name__ == '__main__':
    # Disable debug mode for production security
    app.run(debug=False, host='127.0.0.1', port=5000)