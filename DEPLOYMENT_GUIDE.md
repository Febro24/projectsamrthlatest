# Deployment Guide - Project Samarth

Complete step-by-step guide for deploying the Samarth Agriculture & Climate Q&A Chatbot.

## 📋 Pre-Deployment Checklist

- [ ] Python 3.8+ installed
- [ ] All CSV data files in project directory
- [ ] `qa_model1.pkl` model file present
- [ ] Internet connection for API calls
- [ ] API key from data.gov.in (optional, default key included)

## 🚀 Quick Deployment Steps

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Verify Files

Ensure these files exist:
- `Rainfallallindia_AI_1901-2021.csv`
- `Sub_Divisionalmonthlyrainfall_IMD_2017.csv`
- `qa_model1.pkl`

### Step 3: Test Locally

```bash
python app.py
```

Visit: http://localhost:5000

## 🌐 Production Deployment Options

### Option A: Windows Server (Recommended for Windows)

#### Using Waitress

1. Install Waitress:
```bash
pip install waitress
```

2. Run production server:
```bash
python run_production.py
```

3. Access at: http://your-server-ip:5000

#### Using IIS with FastCGI

1. Install `wfastcgi`:
```bash
pip install wfastcgi
```

2. Configure IIS to use Python FastCGI
3. Point to `app.py`

### Option B: Linux Server

#### Using Gunicorn (Recommended)

1. Install Gunicorn:
```bash
pip install gunicorn
```

2. Run:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 app:app
```

#### Using systemd Service

1. Create `/etc/systemd/system/samarth.service`:
```ini
[Unit]
Description=Samarth Q&A Chatbot
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/samrathproj
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app

[Install]
WantedBy=multi-user.target
```

2. Enable and start:
```bash
sudo systemctl enable samarth
sudo systemctl start samarth
```

3. Configure Nginx reverse proxy (optional but recommended)

### Option C: Cloud Platforms

#### Heroku

1. Install Heroku CLI

2. Create `Procfile`:
```
web: gunicorn app:app
```

3. Create `runtime.txt`:
```
python-3.11.0
```

4. Deploy:
```bash
heroku login
heroku create samarth-chatbot
git push heroku main
```

#### PythonAnywhere

1. Sign up at pythonanywhere.com
2. Upload files via Files tab
3. Go to Web tab → Add new web app
4. Select Flask, Python 3.8+
5. Set source code path
6. Reload web app

#### AWS Elastic Beanstalk

1. Install EB CLI:
```bash
pip install awsebcli
```

2. Initialize:
```bash
eb init -p python-3.8 samarth-app
```

3. Create environment:
```bash
eb create samarth-env
```

4. Deploy:
```bash
eb deploy
```

#### Google Cloud Platform (App Engine)

1. Create `app.yaml`:
```yaml
runtime: python39

handlers:
- url: /.*
  script: app.app
```

2. Deploy:
```bash
gcloud app deploy
```

#### Azure App Service

1. Install Azure CLI

2. Create app:
```bash
az webapp up --name samarth-chatbot --runtime "PYTHON:3.9"
```

3. Deploy files:
```bash
az webapp up --name samarth-chatbot
```

## 🔒 Security Considerations

### 1. Environment Variables

Create `.env` file:
```
API_KEY=your_data_gov_in_api_key
SECRET_KEY=your_flask_secret_key
```

Update `backend_logic.py` to use:
```python
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv('API_KEY')
```

### 2. CORS Configuration

For production, restrict CORS:
```python
CORS(app, origins=["https://yourdomain.com"])
```

### 3. Rate Limiting

Install Flask-Limiter:
```bash
pip install flask-limiter
```

Add to `app.py`:
```python
from flask_limiter import Limiter
limiter = Limiter(app, key_func=get_remote_address)

@app.route('/api/chat', methods=['POST'])
@limiter.limit("10 per minute")
def chat():
    ...
```

## 📊 Monitoring & Logging

### Enable Logging

Add to `app.py`:
```python
import logging
logging.basicConfig(
    filename='samarth.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)
```

### Health Monitoring

The `/api/health` endpoint can be used for monitoring:
```bash
curl http://your-server/api/health
```

## 🔧 Troubleshooting

### Port Already in Use

Change port in `app.py`:
```python
app.run(debug=False, host='0.0.0.0', port=8080)
```

### Data Loading Errors

1. Check file paths
2. Verify CSV files exist
3. Check internet connection for API
4. Review logs for specific errors

### Model Loading Issues

The system will work without model file, using rule-based responses only.

### Memory Issues

For large datasets:
1. Reduce API limit
2. Use data caching
3. Increase server RAM
4. Use pagination for responses

## 📈 Performance Optimization

1. **Caching**: Implement Redis for query caching
2. **Data Preloading**: Pre-load datasets on startup
3. **CDN**: Use CDN for static files
4. **Database**: Consider moving to PostgreSQL for large datasets

## 🔄 Updates & Maintenance

1. Pull latest changes
2. Update dependencies: `pip install -r requirements.txt --upgrade`
3. Restart service
4. Monitor logs

## 📞 Support

For deployment issues:
1. Check logs
2. Verify all dependencies installed
3. Test API endpoints manually
4. Review error messages

---

**Happy Deploying! 🚀**

