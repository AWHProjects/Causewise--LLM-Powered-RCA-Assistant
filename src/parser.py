import json
import csv
import os
from io import StringIO

def detect_log_format(filepath):
    """Detect the format of the log file based on extension and content"""
    _, ext = os.path.splitext(filepath.lower())
    
    if ext == '.json':
        return 'json'
    elif ext == '.csv':
        return 'csv'
    elif ext in ['.txt', '.log']:
        # Try to detect if it's structured data
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            first_line = f.readline().strip()
            if first_line.startswith('[') or first_line.startswith('{'):
                return 'json'
            elif ',' in first_line and '"' in first_line:
                return 'csv'
            else:
                return 'text'
    else:
        return 'text'

def parse_log(filepath):
    """Enhanced parser that handles multiple log formats"""
    content = ""
    try:
        log_format = detect_log_format(filepath)
        
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        if log_format == 'json':
            return parse_json_logs(content)
        elif log_format == 'csv':
            return parse_csv_logs(content)
        else:
            return parse_text_logs(content)
            
    except Exception as e:
        return f"Error reading file: {str(e)}\n\nRaw content:\n{content if content else 'Unable to read file'}"

def parse_json_logs(content):
    """Parse JSON formatted logs (like Splunk exports)"""
    try:
        # Try to parse as JSON array first
        data = json.loads(content)
        if isinstance(data, list):
            # Splunk-style JSON logs
            parsed_logs = []
            for entry in data:
                if isinstance(entry, dict):
                    # Extract key information
                    timestamp = entry.get('_time', entry.get('timestamp', 'Unknown'))
                    level = entry.get('level', entry.get('severity', 'INFO'))
                    message = entry.get('message', entry.get('_raw', str(entry)))
                    host = entry.get('host', 'Unknown')
                    source = entry.get('source', entry.get('sourcetype', 'Unknown'))
                    
                    parsed_logs.append(f"[{timestamp}] {level} [{host}] {source}: {message}")
            
            return "\n".join(parsed_logs) + f"\n\n--- ORIGINAL JSON DATA ---\n{content}"
        else:
            # Single JSON object
            return f"JSON Log Entry:\n{json.dumps(data, indent=2)}\n\n--- RAW DATA ---\n{content}"
    except json.JSONDecodeError:
        # Not valid JSON, treat as text
        return f"Invalid JSON format. Treating as text:\n\n{content}"

def parse_csv_logs(content):
    """Parse CSV formatted logs"""
    try:
        # Use StringIO to treat string as file
        csv_file = StringIO(content)
        reader = csv.DictReader(csv_file)
        
        parsed_logs = []
        for row in reader:
            # Try to identify common log fields
            timestamp = row.get('timestamp', row.get('time', row.get('date', 'Unknown')))
            level = row.get('level', row.get('severity', row.get('priority', 'INFO')))
            message = row.get('message', row.get('description', row.get('event', str(row))))
            
            parsed_logs.append(f"[{timestamp}] {level}: {message}")
        
        return "\n".join(parsed_logs) + f"\n\n--- ORIGINAL CSV DATA ---\n{content}"
    except Exception as e:
        return f"Error parsing CSV: {str(e)}\n\nRaw content:\n{content}"

def parse_text_logs(content):
    """Parse plain text logs with intelligent formatting"""
    lines = content.split('\n')
    parsed_lines = []
    
    for line in lines:
        if line.strip():
            # Try to identify and highlight important patterns
            if any(keyword in line.upper() for keyword in ['ERROR', 'CRITICAL', 'FATAL']):
                parsed_lines.append(f"🔴 {line}")
            elif any(keyword in line.upper() for keyword in ['WARN', 'WARNING']):
                parsed_lines.append(f"🟡 {line}")
            elif any(keyword in line.upper() for keyword in ['INFO', 'DEBUG', 'TRACE']):
                parsed_lines.append(f"🔵 {line}")
            else:
                parsed_lines.append(f"⚪ {line}")
    
    return "\n".join(parsed_lines)