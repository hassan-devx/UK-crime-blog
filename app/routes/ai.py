from flask import Blueprint
from textblob import TextBlob
from flask_login import login_required
from flask import Blueprint, render_template, request, redirect, url_for
import pandas as pd
import json

from flask_login import current_user

from ..data_utils import load_cleaned_data
df = load_cleaned_data()


ai_bp = Blueprint('ai_bp', __name__)

def analyze_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.2:
        return 'positive'
    elif polarity < -0.2:
        return 'negative'
    else:
        return 'neutral'
    

def summarize_post(text):
    lines = text.strip().split('.')
    summary = '. '.join(lines[:2]) + '.' if len(lines) >= 2 else text
    return summary



from app.ai_tools import generate_crime_summary, detect_crime_trends, generate_top_crimes_chart



from config import DATA_PATH


from analytics import get_monthly_trends, get_top_crimes, get_hotspots, get_city_counts, filter_south_wales
from app.ai_tools import generate_ai_summary


@ai_bp.route('/crime-summary')
@login_required
def crime_summary():
    df = load_cleaned_data()
    selected_month = request.args.get('month')
    selected_region = request.args.get('region') or current_user.region  # fallback to user default


    try:
        df['month'] = pd.to_datetime(df['month'], errors='coerce')
        df = df.dropna(subset=['month'])
        df['month_str'] = df['month'].dt.strftime('%Y-%m')

       
        available_months = sorted(df['month_str'].unique(), reverse=True)
        available_regions = sorted(df['region'].dropna().unique())  # ✅ assumes 'region' column exists
        
        if current_user.role == 'admin':
             available_regions = sorted(df['region'].dropna().unique())
        else:
             available_regions = [current_user.region]

        if selected_month:
            df = df[df['month_str'] == selected_month]

        if selected_region:
            # selected_region = selected_region.strip().title()
            df = df[df['region'] == selected_region]

        summary = generate_crime_summary(df)
        trends = detect_crime_trends(df)
        chart_data = generate_top_crimes_chart(df, selected_month, selected_region)
        ai_insight = generate_ai_summary(df)
       
    
    except Exception as e:
        summary = f"Error loading crime data: {e}"
        trends = ""
        chart_data = {
            "labels": [],
            "values": [],
            "title": "No chart data available"
        }
        ai_insight = "AI insight could not be generated due to a data error."

   
    return render_template('ai/crime_summary.html',
        summary=summary,
        trends=trends,
        selected_month=selected_month,
        chart_data=chart_data,
        ai_insight=ai_insight,
        available_months=available_months,
        available_regions=available_regions,
        selected_region=selected_region
    )



def generate_top_crimes_chart(df, selected_month=None, selected_region=None):
    df['month'] = pd.to_datetime(df['month'], errors='coerce')
    df = df.dropna(subset=['month'])
    df['month_str'] = df['month'].dt.strftime('%Y-%m')

    if selected_month:
        df = df[df['month_str'] == selected_month]
    if selected_region:
        selected_region = selected_region.strip().title()
        df = df[df['region'] == selected_region]

    top_crimes = df['crime_type'].value_counts().head(5)

    if top_crimes.empty:
        return {
            "labels": [],
            "values": [],
            "title": "No chart data available"
        }

    # Build title safely
    title_parts = ["Top Crimes"]
    if selected_region:
        title_parts.append(f"in {selected_region}")
    if selected_month:
        title_parts.append(f"- {selected_month}")
    title = " ".join(title_parts)

    return {
        "labels": top_crimes.index.tolist(),
        "values": top_crimes.values.tolist(),
        "title": title
    }

@ai_bp.route('/user-dashboard')
@login_required
def user_dashboard():
    df = load_cleaned_data()
    selected_month = request.args.get('month')

    # Always filter by the user's assigned region
    selected_region = current_user.region

    df['month'] = pd.to_datetime(df['month'], errors='coerce')
    df = df.dropna(subset=['month'])
    df['month_str'] = df['month'].dt.strftime('%Y-%m')

    available_months = sorted(df['month_str'].unique(), reverse=True)
    available_regions = df['region'].dropna().unique().tolist()
    available_regions.sort()

    if selected_month:
        df = df[df['month_str'] == selected_month]
    if selected_region:
        df = df[df['region'] == selected_region]

    summary = generate_crime_summary(df)
    chart_data = generate_top_crimes_chart(df, selected_month, selected_region)
    ai_insight = generate_ai_summary(df)
    zipped_chart_data = zip(chart_data['labels'], chart_data['values'])

    labels = chart_data['labels']
    values = chart_data['values']


    return render_template('ai/user_dashboard.html',
        summary=summary,
        chart_data=chart_data,
        ai_insight=ai_insight,
        selected_month=selected_month,
        selected_region=selected_region, 
        zipped_chart_data=zipped_chart_data,
        available_months=available_months,
        chart_labels=json.dumps(labels),
        chart_values=json.dumps(values),
        available_regions=available_regions
    )



