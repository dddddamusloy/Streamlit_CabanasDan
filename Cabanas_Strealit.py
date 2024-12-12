import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Title of the App
st.title("Hospital General Information Dashboard")

# File upload
uploaded_file = st.file_uploader("Upload Hospital Data (CSV)", type="csv")

if uploaded_file:
    # Load data into DataFrame
    data = pd.read_csv(uploaded_file)

    # Display the first few rows of the data
    st.write(data.head())

    # Show available column names to ensure correct reference
    st.write("Available Columns:", data.columns)

    # Clean data (fill missing values for easier processing)
    data['Hospital Type'] = data['Hospital Type'].fillna('Unknown')

    # Hospital Rating Distribution Plot
    st.subheader('Hospital Ratings Distribution')
    # Check if the column name matches exactly
    if 'Hospital overall rating' in data.columns:
        rating_fig = px.histogram(data, x='Hospital overall rating', nbins=10, title="Hospital Rating Distribution")
        st.plotly_chart(rating_fig)
    else:
        st.write("Column 'Hospital overall rating' not found in the data.")

    # Region filter: Select state
    region_filter = st.selectbox("Select a Region", data['State'].unique())
    filtered_data = data[data['State'] == region_filter]

    # Show filtered data
    st.write(f"Displaying data for hospitals in {region_filter}")
    st.write(filtered_data)

    # Hospital Services vs Ratings (Boxplot)
    st.subheader('Hospital Services vs Ratings')
    if 'Hospital Type' in filtered_data.columns and 'Hospital overall rating' in filtered_data.columns:
        service_ratings_fig = sns.boxplot(x='Hospital Type', y='Hospital overall rating', data=filtered_data)
        plt.title('Hospital Services vs Ratings')
        st.pyplot(service_ratings_fig.figure)
    else:
        st.write("Necessary columns are missing for this plot.")

    # Geographical visualization of hospitals (using Plotly)
    st.subheader('Hospital Locations Map')
    if 'Provider Zip' in filtered_data.columns:
        location_fig = px.scatter_geo(filtered_data, locations="Provider Zip", color="Hospital Type", 
                                      hover_name="Hospital Name", title="Hospital Locations")
        st.plotly_chart(location_fig)
    else:
        st.write("Geographical data is missing or malformed.")
