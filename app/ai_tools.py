import matplotlib
matplotlib.use('Agg')  # ✅ Prevent GUI errors in Flask

import matplotlib.pyplot as plt
import pandas as pd

def generate_crime_summary(df):
    if df.empty:
        return "No crime data available at the moment."

    top_crimes = df['crime_type'].value_counts().head(3).to_dict()
    area = df['lsoa_name'].mode().iloc[0] if 'lsoa_name' in df.columns else "your area"
    total = len(df)

    summary = (
        f"In {area}, a total of {total} crimes were reported. "
        f"The most common types were: "
        + ", ".join([f"{crime} ({count})" for crime, count in top_crimes.items()]) + "."
    )
    return summary


def detect_crime_trends(df):
    import pandas as pd

    # Convert 'Month' to datetime
    df['month'] = pd.to_datetime(df['month'], errors='coerce')
    df = df.dropna(subset=['month'])

    # Create a string column for year-month
    df['month_str'] = df['month'].dt.strftime('%Y-%m')

    # Group by MonthStr and count crimes
    monthly_counts = df.groupby('month_str')['crime_type'].count()

    # Detect trend direction
    if len(monthly_counts) < 2:
        return "Not enough data to detect trends."

    recent = monthly_counts.iloc[-1]
    previous = monthly_counts.iloc[-2]

    if recent > previous:
        return f"Crime reports increased from {previous} to {recent} last month."
    elif recent < previous:
        return f"Crime reports decreased from {previous} to {recent} last month."
    else:
        return f"Crime reports remained steady at {recent} last month."


def generate_top_crimes_chart(df):
    df['month'] = pd.to_datetime(df['month'], errors='coerce')
    df = df.dropna(subset=['month'])
    df['month_str'] = df['month'].dt.strftime('%Y-%m')

    if selected_month:
        df = df[df['month_str'] == selected_month]

    top_crimes = df['crime_type'].value_counts().head(5)

    if top_crimes.empty:
        return {
            "labels": [],
            "values": [],
            "title": "No chart data available"
        }

    return {
        "labels": top_crimes.index.tolist(),
        "values": top_crimes.values.tolist(),
        "title": f"Top 5 Crime Types – {selected_month or 'All Time'}"
    }


def generate_ai_summary(df):
    top_crimes = df['crime_type'].value_counts().head(3)
    top_lsoa = df['lsoa_name'].value_counts().idxmax()
    top_lsoa_count = df['lsoa_name'].value_counts().max()
    monthly = df.groupby('month_str')['crime_type'].count()
    peak_month = monthly.idxmax()
    peak_count = monthly.max()

    print("✅ ai_tools.py loaded successfully")

    return (
        f"{top_crimes.index[0]} leads with {top_crimes.iloc[0]} incidents, "
        f"followed by {top_crimes.index[1]} and {top_crimes.index[2]}. "
        f"The most active hotspot is {top_lsoa} with {top_lsoa_count} incidents. "
        f"Crime peaked in {peak_month} with {peak_count} total reports."
    )