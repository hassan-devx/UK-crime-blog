import os

# 🔐 Flask App Configuration
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True

# 📊 Data Pipeline Configuration
DATA_PATH = "C:/Users/User/Desktop/UK-crime-blog/data_analysis/notebooks/cleaned_crime_data.csv"

DATASETS = {
    "south_wales": "data_analysis/notebooks/cleaned_crime_data.csv",
    "filtered": "filtered_crime_data.csv",
    "raw": "raw_crime_data.csv"
}

def warn_if_using_old_path(path):
    if "filtered_crime_data.csv" in path:
        print("⚠️ WARNING: You're using the old filtered file. Switch to DATA_PATH.")

warn_if_using_old_path(DATA_PATH)