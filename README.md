# IBS_App Food and Symptom Tracker

A web-based application made with Streamlit that allows users to log meals and symptoms, pertaining to gastrointestines, visualize food-symptom correlations, and detect patterns based on time-based analysis.

**Deployment Link:** https://ibs-food-symptom-tracker-app-hz4ebgdyqto9owvcqchree.streamlit.app/

## Features

- **Articles**: Images and clickable links to reputable IBS-related articles.
- **FODMAP Search**: Users can search up a food to see its FODMAP, based on a CSV file containing foods and associated FODMAPs. If the food is not found, they can request for that food to be added to the CSV file.
- **Food Journal**: Users can log meals with timestamps.
- **Symptoms Tracker**: Users can record symptoms and triggers with timestamps.
- **Pattern Detection**: Automatic detection of food-symptom combinations that occur within 5 hours in table format. Shows table of top three most frequent food-symptom pairs with their count.
- **Custom Analysis**: Users can filter entries by food or time range, as well as hours window after eating when symptoms occur. Users can then see affected visual.
- **Data Visualizations**: Shows tables and bar charts of most frequent food-symptom pairs and their counts. Has interactive customizable bar chart for data insight exploration.

## Technologies
- **Python**
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation
- **Datetime**: Time-based analysis, time window filtering analysis
- **OS**: local file handling, CSV management
 
## Planned Improvements
- Let users group by symptoms
- Let users see previous entries
