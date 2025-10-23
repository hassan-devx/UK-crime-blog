# analytics.py

def get_monthly_trends(df):
    return df.groupby('month_str')['crime_type'].count().sort_index()

def get_top_crimes(df, n=5):
    return df['crime_type'].value_counts().head(n)

def get_hotspots(df, n=5):
    return df['lsoa_name'].value_counts().head(n)

def get_violent_trend(df):
    return df[df['is_violent']].groupby('month_str')['crime_type'].count().sort_index()

def get_property_trend(df):
    return df[df['is_property']].groupby('month_str')['crime_type'].count().sort_index()

def get_city_counts(df, n=10):
    return df['city'].value_counts().head(n).sort_values(ascending=False)

def get_city_crime_matrix(df):
    return df.groupby(['city', 'crime_type']).size().unstack(fill_value=0)


def filter_south_wales(df):
    south_wales = ['Swansea', 'Cardiff', 'Newport', 'Rhondda Cynon Taf', 'Caerphilly', 'Bridgend', 'Merthyr Tydfil', 'Neath Port Talbot', 'Vale Of Glamorgan', 'Blaenau Gwent']
    return df[df['city'].isin(south_wales)]