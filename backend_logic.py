# -*- coding: utf-8 -*-
"""
Backend logic for Samarth Agriculture & Climate Q&A System
Refactored for Flask backend integration
"""

import pandas as pd
import requests
import re
import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

# Global variables to store loaded data
merged_df = None
qa_model = None

def load_data():
    """Load and merge all datasets."""
    global merged_df
    
    try:
        # Read Rainfall CSVs
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        rainfall_allindia_path = os.path.join(base_dir, 'Rainfallallindia_AI_1901-2021.csv')
        rainfall_subdiv_path = os.path.join(base_dir, 'Sub_Divisionalmonthlyrainfall_IMD_2017.csv')
        
        if not os.path.exists(rainfall_allindia_path):
            print(f"⚠️ Warning: {rainfall_allindia_path} not found. Trying alternate path...")
            rainfall_allindia_path = 'Rainfallallindia_AI_1901-2021.csv'
        
        if not os.path.exists(rainfall_subdiv_path):
            print(f"⚠️ Warning: {rainfall_subdiv_path} not found. Trying alternate path...")
            rainfall_subdiv_path = 'Sub_Divisionalmonthlyrainfall_IMD_2017.csv'
        
        rainfall_allindia = pd.read_csv(rainfall_allindia_path)
        rainfall_subdiv = pd.read_csv(rainfall_subdiv_path)
        
        # Fetch data from data.gov.in API
        url = "https://api.data.gov.in/resource/35be999b-0208-4354-b557-f6ca9a5355de"
        params = {
            "api-key": "579b464db66ec23bdd000001923d57b91b764d344ad3f46f31fb8ebd",
            "format": "json",
            "limit": 1000000
        }
        
        response = requests.get(url, params=params, timeout=30)
        data = response.json()
        crop_df = pd.DataFrame(data['records'])
        
        # Clean column names
        crop_df.columns = crop_df.columns.str.strip().str.lower()
        crop_df['crop_year'] = pd.to_numeric(crop_df['crop_year'], errors='coerce')
        crop_df['area_'] = pd.to_numeric(crop_df['area_'], errors='coerce')
        crop_df['production_'] = pd.to_numeric(crop_df['production_'], errors='coerce')
        crop_df = crop_df.dropna(subset=['crop_year'])
        crop_df['state_name'] = crop_df['state_name'].str.strip()
        crop_df['district_name'] = crop_df['district_name'].str.strip()
        crop_df['season'] = crop_df['season'].str.strip()
        crop_df['crop'] = crop_df['crop'].str.strip()
        
        # Clean rainfall data
        rainfall_allindia.columns = rainfall_allindia.columns.str.strip().str.lower()
        if 'year' not in rainfall_allindia.columns:
            if 'year.1' in rainfall_allindia.columns:
                rainfall_allindia.rename(columns={'year.1': 'year'}, inplace=True)
        
        rainfall_allindia['year'] = pd.to_numeric(rainfall_allindia['year'], errors='coerce')
        rainfall_allindia = rainfall_allindia.dropna(subset=['year'])
        
        # Merge datasets - check if required columns exist
        if 'year' not in rainfall_allindia.columns:
            if 'year.1' in rainfall_allindia.columns:
                rainfall_allindia.rename(columns={'year.1': 'year'}, inplace=True)
            else:
                print(" Error: 'year' column not found in rainfall data")
                return False
        
        # Check for required columns before merge
        required_rainfall_cols = ['year', 'jun-sep']
        if not all(col in rainfall_allindia.columns for col in required_rainfall_cols):
            print(f" Error: Required columns not found. Available: {rainfall_allindia.columns.tolist()}")
            # Try alternative column names
            if 'jun_sep' in rainfall_allindia.columns:
                rainfall_allindia.rename(columns={'jun_sep': 'jun-sep'}, inplace=True)
            else:
                return False
        
        # Merge datasets
        merged_df = pd.merge(
            crop_df,
            rainfall_allindia[['year', 'jun-sep']],
            left_on='crop_year',
            right_on='year',
            how='inner'
        )
        if 'year' in merged_df.columns:
            merged_df.drop('year', axis=1, inplace=True)
        
        print(" Data loaded successfully!")
        print(f"Merged dataset shape: {merged_df.shape}")
        return True
        
    except Exception as e:
        print(f" Error loading data: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def load_model():
    """Load the trained QA model."""
    global qa_model
    
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(base_dir, 'qa_model1.pkl')
        
        if os.path.exists(model_path):
            qa_model = joblib.load(model_path)
            print(" QA model loaded successfully!")
            return True
        else:
            print(" Model file not found, will use rule-based responses")
            return False
    except Exception as e:
        print(f" Error loading model: {str(e)}")
        return False

def compare_rainfall(state1, state2, n_years=5):
    """Compare average monsoon rainfall for two states for last n years."""
    global merged_df
    if merged_df is None:
        return "Data not loaded. Please wait..."
    
    df = merged_df.copy()
    recent_years = sorted(df['crop_year'].unique())[-n_years:]
    comparison = df[df['crop_year'].isin(recent_years)]
    
    result = comparison.groupby('state_name')['jun-sep'].mean().reset_index()
    result = result[result['state_name'].isin([state1, state2])]
    return result

def top_crops_by_state(state, n=5):
    """Top crops by total production in a state."""
    global merged_df
    if merged_df is None:
        return "Data not loaded. Please wait..."
    
    df = merged_df[merged_df['state_name'] == state]
    if df.empty:
        return f"No data found for state: {state}"
    
    top_crops = df.groupby('crop')['production_'].sum().sort_values(ascending=False).head(n)
    result = pd.DataFrame({
        'Crop': top_crops.index,
        'Total Production (tonnes)': top_crops.values
    })
    return result

def crop_trend(crop_name, region=None):
    """Analyze production and monsoon rainfall trend of a crop (optionally for a state)."""
    global merged_df
    if merged_df is None:
        return "Data not loaded. Please wait..."
    
    df = merged_df[merged_df['crop'] == crop_name]
    if region:
        df = df[df['state_name'] == region]
    
    if df.empty:
        return f"No data found for crop: {crop_name}" + (f" in {region}" if region else "")
    
    trend = df.groupby('crop_year')[['production_', 'jun-sep']].mean().reset_index()
    trend.columns = ['Year', 'Production (tonnes)', 'Monsoon Rainfall (mm)']
    return trend

def get_state_stats(state):
    """Get general statistics for a state."""
    global merged_df
    if merged_df is None:
        return "Data not loaded. Please wait..."
    
    df = merged_df[merged_df['state_name'] == state]
    if df.empty:
        return f"No data found for state: {state}"
    
    stats = {
        'state': state,
        'total_crops': df['crop'].nunique(),
        'avg_production': df['production_'].mean(),
        'avg_rainfall': df['jun-sep'].mean(),
        'total_years': df['crop_year'].nunique()
    }
    return stats

def samarth_query(query):
    """Main query processing function."""
    global merged_df
    if merged_df is None:
        return {"error": "Data not loaded. Please wait..."}
    
    query_lower = query.lower()
    
    # Rainfall comparison
    if "compare" in query_lower and "rainfall" in query_lower:
        states = re.findall(r"(?:in|between)\s+([a-zA-Z\s]+?)(?:\s+and\s+|\s*,\s*)([a-zA-Z\s]+)", query_lower)
        if not states:
            states = re.findall(r"(\w+)\s+and\s+(\w+)", query_lower)
        
        years = re.findall(r"last\s+(\d+)", query_lower)
        n = int(years[0]) if years else 5
        
        if states:
            s1, s2 = states[0]
            s1 = s1.strip().title()
            s2 = s2.strip().title()
            result = compare_rainfall(s1, s2, n)
            if isinstance(result, pd.DataFrame):
                return {"type": "dataframe", "data": result.to_dict('records'), "query_type": "rainfall_comparison"}
            return {"type": "text", "data": str(result)}
    
    # Top crops
    if "top" in query_lower and "crop" in query_lower:
        state_match = re.search(r"in\s+([a-zA-Z\s]+)", query_lower)
        if state_match:
            state = state_match.group(1).strip().title()
            result = top_crops_by_state(state)
            if isinstance(result, pd.DataFrame):
                return {"type": "dataframe", "data": result.to_dict('records'), "query_type": "top_crops"}
            return {"type": "text", "data": str(result)}
    
    # Crop trend
    if "trend" in query_lower or "over years" in query_lower or "production trend" in query_lower:
        crop_match = re.search(r"(?:of|for)\s+([a-zA-Z\s]+?)(?:\s+in\s+|\s*$)", query_lower)
        state_match = re.search(r"in\s+([a-zA-Z\s]+)", query_lower)
        
        if crop_match:
            crop = crop_match.group(1).strip().title()
            state = state_match.group(1).strip().title() if state_match else None
            result = crop_trend(crop, state)
            if isinstance(result, pd.DataFrame):
                return {"type": "dataframe", "data": result.to_dict('records'), "query_type": "crop_trend"}
            return {"type": "text", "data": str(result)}
    
    # State statistics
    if "statistics" in query_lower or "stats" in query_lower or "information" in query_lower:
        state_match = re.search(r"for\s+([a-zA-Z\s]+)|([a-zA-Z\s]+)\s+statistics", query_lower)
        if state_match:
            state = (state_match.group(1) or state_match.group(2)).strip().title()
            result = get_state_stats(state)
            return {"type": "json", "data": result, "query_type": "state_stats"}
    
    # Try to use ML model if available
    global qa_model
    if qa_model is not None:
        try:
            prediction = qa_model.predict([query])[0]
            return {"type": "text", "data": prediction, "query_type": "ml_prediction"}
        except:
            pass
    
    return {
        "type": "text",
        "data": "I couldn't understand your question. Try asking about:\n- Comparing rainfall between states\n- Top crops in a state\n- Production trends of crops\n- Statistics for a state",
        "query_type": "default"
    }

# Initialize on import
if __name__ != "__main__":
    load_data()
    load_model()

