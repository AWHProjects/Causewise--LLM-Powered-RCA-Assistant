import os
import mimetypes
from werkzeug.utils import secure_filename
from pathlib import Path

# Security configuration
ALLOWED_EXTENSIONS = {'.log', '.txt', '.json', '.csv'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB limit
ALLOWED_MIME_TYPES = {
    'text/plain', 'application/json', 'text/csv', 
    'application/csv', 'text/x-log', 'application/octet-stream'
}

def validate_file_security(file):
    """Comprehensive file security validation"""
    if not file or not file.filename:
        return False, "No file provided"
    
    # Check file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        return False, f"File type {file_ext} not allowed. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
    
    # Check MIME type
    mime_type, _ = mimetypes.guess_type(file.filename)
    if mime_type and mime_type not in ALLOWED_MIME_TYPES:
        return False, f"MIME type {mime_type} not allowed"
    
    # Check file size (read first chunk to estimate)
    file.seek(0, 2)  # Seek to end
    size = file.tell()
    file.seek(0)  # Reset to beginning
    
    if size > MAX_FILE_SIZE:
        return False, f"File too large. Maximum size: {MAX_FILE_SIZE // (1024*1024)}MB"
    
    return True, "File validation passed"

def save_uploaded_file(uploaded_file, folder='data'):
    """Secure file upload with comprehensive validation"""
    # Security validation
    is_valid, message = validate_file_security(uploaded_file)
    if not is_valid:
        raise ValueError(f"Security validation failed: {message}")
    
    # Secure filename processing
    filename = secure_filename(uploaded_file.filename)
    if not filename:
        raise ValueError("Invalid filename after security processing")
    
    # Prevent path traversal - ensure folder is absolute and secure
    folder = os.path.abspath(folder)
    filepath = os.path.abspath(os.path.join(folder, filename))
    
    # Critical security check: ensure file stays within upload directory
    if not filepath.startswith(folder):
        raise ValueError("Path traversal attempt detected")
    
    # Ensure upload directory exists
    os.makedirs(folder, exist_ok=True)
    
    # Save file securely
    try:
        uploaded_file.save(filepath)
        return filepath
    except Exception as e:
        raise ValueError(f"Failed to save file: {str(e)}")