# Project Samarth - Agriculture & Climate Q&A Chatbot

An intelligent Q&A system for answering complex questions about Indian agriculture and climate using government datasets from data.gov.in.

## 🌾 Features

- **Interactive Chat Interface**: Modern, responsive web-based chatbot
- **Rainfall Analysis**: Compare monsoon rainfall between states
- **Crop Statistics**: Get top crops by production in different states
- **Trend Analysis**: Analyze crop production trends over years
- **State Statistics**: Comprehensive statistics for any state
- **Real-time Data**: Fetches live data from government APIs

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Internet connection (for fetching data from APIs)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Ensure Data Files Are Present

Make sure you have these files in the project directory:
- `Rainfallallindia_AI_1901-2021.csv`
- `Sub_Divisionalmonthlyrainfall_IMD_2017.csv`
- `qa_model1.pkl`

### 3. Run the Application

```bash
python app.py
```

The application will be available at: **http://localhost:5000**

## 📁 Project Structure

```
samrathproj/
│
├── app.py                      # Flask backend server
├── backend_logic.py            # Core Q&A logic and data processing
├── samrath_projupdated.py      # Original data processing script
├── qa_model1.pkl              # Trained machine learning model
├── requirements.txt            # Python dependencies
│
├── templates/
│   └── index.html             # Frontend HTML template
│
├── static/
│   ├── style.css              # Frontend styles
│   └── script.js              # Frontend JavaScript
│
└── data files (CSV files)
```

## 🎯 Usage Examples

### Sample Queries

1. **Rainfall Comparison**
   - "Compare rainfall in Maharashtra and Kerala for last 5 years"
   - "Compare monsoon rainfall between Gujarat and Rajasthan"

2. **Top Crops**
   - "Show top crops in Punjab"
   - "What are the top crops in Tamil Nadu?"

3. **Production Trends**
   - "Show production trend of Rice in Tamil Nadu"
   - "What is the trend of Wheat production in Uttar Pradesh?"

4. **State Statistics**
   - "What are the statistics for Karnataka?"
   - "Show information about Maharashtra"

## 🌐 Deployment

### Local Development

For local development, simply run:
```bash
python app.py
```

### Production Deployment

#### Option 1: Using Gunicorn (Recommended for Linux/Mac)

1. Install Gunicorn:
```bash
pip install gunicorn
```

2. Run with Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

#### Option 2: Using Waitress (Recommended for Windows)

1. Install Waitress:
```bash
pip install waitress
```

2. Create a production script `run_production.py`:
```python
from waitress import serve
from app import app

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000)
```

3. Run:
```bash
python run_production.py
```

#### Option 3: Deploy to Cloud Platforms

##### Heroku

1. Create `Procfile`:
```
web: gunicorn app:app
```

2. Deploy:
```bash
heroku create your-app-name
git push heroku main
```

##### PythonAnywhere

1. Upload all files to your PythonAnywhere account
2. Configure WSGI file to point to `app.py`
3. Reload web app

##### AWS Elastic Beanstalk

1. Create `requirements.txt` (already included)
2. Package application:
```bash
zip -r samarth-app.zip . -x "*.git*" "*.pyc" "__pycache__/*"
```

3. Upload to AWS Elastic Beanstalk console

##### Google Cloud Platform

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

## 🔧 Configuration

### API Key Configuration

The application uses data.gov.in API. To use your own API key:

1. Register at [data.gov.in](https://data.gov.in)
2. Get your API key
3. Update `backend_logic.py`:
```python
params = {
    "api-key": "YOUR_API_KEY_HERE",
    ...
}
```

## 🐛 Troubleshooting

### Data Loading Issues

If you encounter errors loading data:
- Ensure CSV files are in the correct directory
- Check internet connection (API data fetching)
- Verify file paths in `backend_logic.py`

### Model Loading Issues

If the model file is missing:
- The system will fall back to rule-based responses
- Train a new model using `samrath_projupdated.py` if needed

### Port Already in Use

If port 5000 is already in use:
- Change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8080)
```

## 📊 Data Sources

- **Rainfall Data**: IMD (India Meteorological Department) via data.gov.in
- **Crop Production Data**: Ministry of Agriculture via data.gov.in
- **API Endpoint**: https://api.data.gov.in/resource/35be999b-0208-4354-b557-f6ca9a5355de

## 🛠️ Development

### Running Tests

Test the API endpoints:
```bash
# Health check
curl http://localhost:5000/api/health

# Example queries
curl http://localhost:5000/api/examples

# Chat endpoint
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Compare rainfall in Maharashtra and Kerala"}'
```

## 📝 License

This project is developed for educational and research purposes using publicly available government data.

## 👨‍💻 Contributing

Feel free to submit issues and enhancement requests!

## 📧 Support

For issues or questions, please check the troubleshooting section or open an issue in the repository.

---

**Developed with ❤️ for Project Samarth**

