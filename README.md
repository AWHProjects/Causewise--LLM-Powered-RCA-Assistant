# Causewise: LLM-Powered RCA Assistant

🔍 **Advanced AI-powered Root Cause Analysis tool** that transforms raw incident logs into structured, actionable insights using local LLM inference via LM Studio.

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Security](https://img.shields.io/badge/security-enhanced-green.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## 🚀 **Key Features**

### 🧠 **Structured AI Analysis**
- **Thinking Process Visualization**: See how the AI reasons through problems in a dedicated red-themed section
- **Step-by-Step Analysis**: Clean, organized breakdown of incident investigation
- **TLDR Summaries**: Plain-language explanations for non-technical stakeholders
- **Metadata Tracking**: Analysis timing, model information, and processing details

### 🛡️ **Enterprise Security**
- **Input Sanitization**: Advanced protection against prompt injection attacks
- **Rate Limiting**: Configurable request throttling to prevent abuse
- **Security Logging**: Comprehensive audit trail for all operations
- **File Upload Validation**: Secure handling of uploaded incident files
- **XSS Protection**: Multiple layers of cross-site scripting prevention

### 📊 **Real-Time Monitoring**
- **System Resource Tracking**: Live CPU, memory, and process monitoring
- **Progress Indicators**: Real-time analysis progress with detailed status updates
- **LLM Connection Validation**: Built-in connectivity testing for local models
- **Performance Metrics**: Response time tracking and analysis statistics

### 🎯 **Multi-Format Support**
- **Enterprise Log Formats**: Splunk JSON, Cisco IOS, Polycom VoIP, and more
- **Intelligent Parsing**: Auto-detection and smart formatting of various log types
- **Demo Scenarios**: Pre-loaded examples for testing and demonstration
- **File Upload**: Secure handling of .log, .txt, .json, and .csv files

---

## 🏗️ **Project Architecture**

```
Causewise--LLM-Powered-RCA-Assistant/
├── 📁 data/                          # Sample log files and test data
│   ├── sample_incident.log           # Basic log format example
│   ├── sample_splunk.json           # Splunk JSON export format
│   ├── sample_complex.txt           # Complex multi-system logs
│   ├── sample_cisco.log             # Cisco network device logs
│   └── sample_polycom.log           # VoIP communication logs
├── 📁 src/                           # Core application logic
│   ├── app.py                       # Flask web application & security
│   ├── llm.py                       # LLM integration & structured parsing
│   ├── parser.py                    # Log parsing & format detection
│   ├── utils.py                     # File handling & validation utilities
│   └── system_monitor.py            # Real-time system monitoring
├── 📁 templates/                     # HTML templates
│   └── index.html                   # Main web interface with footer
├── 📁 static/                        # CSS and static assets
│   └── style.css                    # Responsive styling with themes
├── .env                             # Environment configuration
├── requirements.txt                 # Python dependencies
└── README.md                        # This documentation
```

---

## 🔧 **Installation & Setup**

### Prerequisites
1. **Python 3.8+** installed on your system
2. **LM Studio** (v0.3.20+) from [https://lmstudio.ai/](https://lmstudio.ai/)
3. **Compatible LLM Model** (recommended: `deepseek/deepseek-r1-0528-qwen3-8b`)

### Quick Start
```bash
# Clone the repository
git clone https://github.com/atom5ive/Causewise--LLM-Powered-RCA-Assistant.git
cd Causewise--LLM-Powered-RCA-Assistant

# Install dependencies
pip install -r requirements.txt

# Configure environment (optional - defaults provided)
cp .env.example .env  # Edit if needed

# Start the application
python src/app.py
```

### LM Studio Configuration
1. **Download & Install** LM Studio from the official website
2. **Load a Model**: Download `deepseek/deepseek-r1-0528-qwen3-8b` or similar
3. **Enable API Service**:
   - Go to **App Settings → Developer**
   - Enable **"Local LLM Service"**
   - Verify at `http://localhost:1234/v1/models`
4. **Start Analysis**: Navigate to `http://localhost:5000`

---

## 🛡️ **Security Enhancements**

### Input Validation & Sanitization
- **Prompt Injection Protection**: Advanced filtering of malicious input patterns
- **File Upload Security**: Secure filename handling and content validation
- **XSS Prevention**: Multiple layers of cross-site scripting protection
- **Content Security Policy**: Strict CSP headers for enhanced security

### Rate Limiting & Monitoring
- **Request Throttling**: Configurable limits (200/day, 50/hour by default)
- **Security Event Logging**: Comprehensive audit trail in `security.log`
- **IP-based Tracking**: Monitor and limit requests per IP address
- **Error Handling**: Secure error messages without system information exposure

### Data Privacy
- **Local Processing**: All analysis performed locally via LM Studio
- **No External APIs**: No data sent to third-party services
- **Secure File Handling**: Temporary file cleanup and secure storage
- **Environment Protection**: Sensitive configuration in `.env` files

---

## 📊 **Usage Examples**

### Web Interface
1. **Upload Log Files**: Drag & drop or select incident logs
2. **Try Demo Formats**: Test with pre-loaded enterprise log examples
3. **View Structured Analysis**: 
   - 🧠 **Thinking Process** (red section)
   - 🔍 **Step-by-Step Analysis** (blue section)
   - 📋 **TLDR Summary** (green section)
   - 📊 **Metadata** (gray section)

### Supported Log Formats
- **Plain Text Logs** (`.log`, `.txt`)
- **JSON Structured Logs** (Splunk exports, application logs)
- **CSV Data** (comma-separated log entries)
- **Cisco IOS Logs** (network device logs with facility codes)
- **VoIP Logs** (Polycom, Asterisk, and other communication systems)

---

## 🔍 **API Endpoints**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main web interface |
| `/analyze` | POST | Process log analysis |
| `/progress` | GET | Real-time analysis progress |
| `/system_stats` | GET | Live system monitoring data |
| `/validate_llm` | GET | Test LLM connectivity |

---

## ⚙️ **Configuration**

### Environment Variables (`.env`)
```bash
# LM Studio Configuration
OPENAI_API_BASE=http://localhost:1234/v1
OPENAI_API_KEY=lm-studio
MODEL_NAME=deepseek/deepseek-r1-0528-qwen3-8b
```

### Security Settings
- **Rate Limits**: Configurable in `src/app.py`
- **File Size Limits**: 10MB maximum upload size
- **Allowed File Types**: `.log`, `.txt`, `.json`, `.csv`
- **Security Logging**: Enabled by default

---

## 🚨 **Troubleshooting**

### Common Issues
| Problem | Solution |
|---------|----------|
| **Connection Refused** | Ensure LM Studio's "Local LLM Service" is enabled |
| **Model Not Found** | Update `MODEL_NAME` in `.env` to match loaded model |
| **Slow Analysis** | Use smaller models or increase timeout settings |
| **Upload Failures** | Check file size (<10MB) and format (.log, .txt, .json, .csv) |
| **Rate Limit Errors** | Wait for rate limit reset or adjust limits in code |

### Debug Mode
```bash
# Enable debug logging
export FLASK_DEBUG=1
python src/app.py
```

---

## 📈 **Performance Metrics**

- **Analysis Speed**: 15-30 seconds per incident (model-dependent)
- **Memory Usage**: ~500MB baseline + model requirements
- **Concurrent Users**: Supports multiple simultaneous analyses
- **File Processing**: Up to 10MB log files supported
- **Response Time**: Real-time progress updates every 500ms

---

## 🎯 **Professional Value**

**Causewise** demonstrates advanced capabilities in:

### 🔧 **Technical Skills**
- **AI/ML Integration**: Practical LLM implementation for business operations
- **Security Engineering**: Multi-layered security architecture
- **Full-Stack Development**: Flask backend with responsive frontend
- **System Monitoring**: Real-time performance tracking and alerting

### 💼 **Business Impact**
- **Incident Response**: Accelerated root cause analysis from hours to minutes
- **Knowledge Transfer**: Structured analysis accessible to all skill levels
- **Cost Reduction**: Local processing eliminates external API costs
- **Compliance**: Enhanced security for sensitive operational data

### 🎖️ **Career Relevance**
Perfect showcase for **Site Reliability Engineer**, **DevOps Engineer**, **Technical Account Manager**, or **Security Engineer** roles, highlighting practical AI application in enterprise operations.

---

## 📋 **Development Roadmap**

### ✅ **Completed Features**
- [x] Structured AI analysis output with thinking process visualization
- [x] Multi-format log parsing (Splunk, Cisco, Polycom, etc.)
- [x] Real-time system monitoring and progress tracking
- [x] Comprehensive security enhancements and input validation
- [x] Rate limiting and security event logging
- [x] Responsive web interface with themed sections
- [x] LLM connectivity validation and error handling

### 🔄 **In Progress**
- [ ] Advanced log correlation across multiple sources
- [ ] Custom analysis templates for specific incident types
- [ ] Integration with popular monitoring tools (Grafana, Prometheus)

### 🎯 **Planned Features**
- [ ] **Multi-Model Support**: Integration with multiple LLM providers
- [ ] **Historical Analysis**: Trend analysis and pattern recognition
- [ ] **API Authentication**: JWT-based API access control
- [ ] **Export Capabilities**: PDF/Word report generation
- [ ] **Webhook Integration**: Automated incident response workflows
- [ ] **Custom Dashboards**: Personalized monitoring interfaces
- [ ] **Machine Learning**: Automated incident classification
- [ ] **Team Collaboration**: Multi-user analysis and commenting
- [ ] **Mobile Interface**: Responsive mobile-first design
- [ ] **Plugin Architecture**: Extensible analysis modules

### 🔧 **Technical Improvements**
- [ ] **Database Integration**: PostgreSQL/MySQL support for analysis history
- [ ] **Caching Layer**: Redis integration for improved performance
- [ ] **Container Support**: Docker and Kubernetes deployment
- [ ] **CI/CD Pipeline**: Automated testing and deployment
- [ ] **Load Balancing**: Multi-instance deployment support
- [ ] **Backup & Recovery**: Automated data backup solutions
- [ ] **Monitoring Integration**: Prometheus metrics and Grafana dashboards
- [ ] **Log Aggregation**: ELK stack integration
- [ ] **Performance Optimization**: Async processing and queue management

---

## 🤝 **Contributing**

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Fork and clone the repository
git clone https://github.com/yourusername/Causewise--LLM-Powered-RCA-Assistant.git

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If available

# Run tests
python -m pytest tests/

# Start development server
python src/app.py
```

---

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📞 **Support & Contact**

For questions, issues, or contributions:

- 👤 **Creator**: Adam Hobgood
- 💼 **LinkedIn**: [https://www.linkedin.com/in/awhobgood/](https://www.linkedin.com/in/awhobgood/)
- 🐛 **Issues**: [GitHub Issues](https://github.com/atom5ive/Causewise--LLM-Powered-RCA-Assistant/issues)
- 📖 **Documentation**: [Security Guide](https://github.com/atom5ive/Causewise--LLM-Powered-RCA-Assistant/blob/main/SECURITY.md)

---

## 🙏 **Acknowledgments**

- **LM Studio Team** for providing excellent local LLM infrastructure
- **OpenAI** for the API compatibility standard
- **Flask Community** for the robust web framework
- **DeepSeek** for high-quality open-source models

---

*Built with ❤️ for the DevOps and SRE community*
