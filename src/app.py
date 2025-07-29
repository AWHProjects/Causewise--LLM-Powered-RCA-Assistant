from flask import Flask, render_template, request
from src.parser import parse_log
from src.llm import analyze_incident
from src.utils import save_uploaded_file

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    analysis = None
    if request.method == 'POST':
        uploaded_file = request.files['incident_file']
        if uploaded_file.filename:
            filepath = save_uploaded_file(uploaded_file)
            log_data = parse_log(filepath)
            analysis = analyze_incident(log_data)
    return render_template('index.html', analysis=analysis)

if __name__ == '__main__':
    app.run(debug=True)