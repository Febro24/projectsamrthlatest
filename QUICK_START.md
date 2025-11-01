# Quick Start Guide - Project Samarth

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start the Server

**Windows:**
```bash
start.bat
```
or
```bash
python app.py
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```
or
```bash
python3 app.py
```

### Step 3: Open Your Browser
Navigate to: **http://localhost:5000**

## 💬 Try These Queries

1. "Compare rainfall in Maharashtra and Kerala for last 5 years"
2. "Show top crops in Punjab"
3. "What is the production trend of Rice in Tamil Nadu?"
4. "What are the statistics for Karnataka?"

## 📁 Required Files

Make sure these files are in your project directory:
- ✅ `Rainfallallindia_AI_1901-2021.csv`
- ✅ `Sub_Divisionalmonthlyrainfall_IMD_2017.csv`
- ✅ `qa_model1.pkl`

## 🔧 Troubleshooting

**Port already in use?**
- Change port in `app.py` (line 61): `port=8080`

**Data not loading?**
- Check if CSV files exist
- Check internet connection (for API calls)
- Review console output for errors

**Module not found?**
- Run: `pip install -r requirements.txt`

## 📖 Full Documentation

- See `README.md` for complete documentation
- See `DEPLOYMENT_GUIDE.md` for deployment options

---

**Happy Chatting! 🌾**

