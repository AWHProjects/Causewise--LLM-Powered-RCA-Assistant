# Causewise: LLM-Powered RCA Assistant

Upload logs or incident descriptions and get AI-suggested root causes and mitigation steps. Built using LangChain + local LLM like Mistral via Ollama.

---

## 🚧 Project Structure:

```
Causewise/
├── data/
│   └── sample_incident.log
├── src/
│   ├── llm.py
│   ├── parser.py
│   ├── app.py
│   └── utils.py
├── templates/
│   └── index.html
├── static/
│   └── style.css
└── requirements.txt
```

---

## 📄 **requirements.txt**

```
flask
langchain
ollama
python-dotenv
```

---

## 📌 **.env** *(remember not to commit this file)*

```
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral
```

---

## 📖 **sample\_incident.log** *(Dummy log file sample)*

```
[2024-07-29 12:45:10] ERROR: Connection timeout at api.service.internal
[2024-07-29 12:45:12] WARN: Retrying connection
[2024-07-29 12:46:15] ERROR: Database transaction deadlock detected
```

---

## 🧩 **parser.py**

```python
def parse_log(filepath):
    with open(filepath, 'r') as f:
        return f.read()
```

---

## 🧠 **llm.py**

```python
from langchain_community.llms import Ollama
import os
from dotenv import load_dotenv

load_dotenv()

ollama_model = os.getenv("OLLAMA_MODEL")
ollama_url = os.getenv("OLLAMA_BASE_URL")

llm = Ollama(model=ollama_model, base_url=ollama_url)

def analyze_incident(log_data):
    prompt = (
        "Analyze the following incident log and suggest likely root causes "
        "and actionable mitigation steps:\n\n" + log_data
    )
    response = llm.invoke(prompt)
    return response
```

---

## 🛠️ **utils.py**

```python
import os
from werkzeug.utils import secure_filename

def save_uploaded_file(uploaded_file, folder='data'):
    filename = secure_filename(uploaded_file.filename)
    filepath = os.path.join(folder, filename)
    uploaded_file.save(filepath)
    return filepath
```

---

## ⚙️ **app.py (Flask Application)**

```python
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
```

---

## 📑 **index.html**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Causewise RCA Assistant</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <h1>Causewise: LLM-Powered RCA Assistant</h1>
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="incident_file" required>
        <button type="submit">Analyze</button>
    </form>
    {% if analysis %}
        <h2>Incident Analysis:</h2>
        <pre>{{ analysis }}</pre>
    {% endif %}
</body>
</html>
```

---

## 🎨 **style.css**

```css
body {
    font-family: Arial, sans-serif;
    background-color: #fafafa;
    margin: 2rem auto;
    padding: 2rem;
    max-width: 800px;
}

h1, h2 {
    color: #333;
}

form {
    margin-bottom: 1.5rem;
}

input, button {
    padding: 0.5rem;
    font-size: 1rem;
}

pre {
    background: #f0f0f0;
    padding: 1rem;
    white-space: pre-wrap;
    word-wrap: break-word;
    border-radius: 5px;
}
```

---

## 🚀 **Local Setup & Run Instructions**

```bash
git clone https://github.com/YourUsername/Causewise.git
cd Causewise
pip install -r requirements.txt
# Ensure Ollama server is running locally:
ollama serve mistral
python src/app.py
```

Navigate to `http://localhost:5000`.

---

## 🎯 **Value to Employers (Pitch):**

> **Causewise** highlights your ability to practically integrate advanced AI models into real-world workflows. By streamlining Root Cause Analysis (RCA) using local LLMs, you're showcasing your readiness for Technical Account Manager or Site Reliability Engineer roles—demonstrating an aptitude for proactive incident management, process improvement, and practical AI application in operations.
