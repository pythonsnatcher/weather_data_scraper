# 🌦️ Weather Data Scraper and Logger 🌊

Tuco was a great help while I developed this project! 🚀

## Overview
This Python script is designed to fetch and log weather and tide data from BBC Weather. It runs continuously, updating weather information every 30 minutes and storing it in a CSV file on Google Drive. Whether you're tracking the latest temperature trends, planning outdoor activities around tide schedules, or gathering data for future weather app development, this script provides a robust foundation.

## Features
### Weather Data
- **Current Conditions:** Includes high and low temperatures, current temperature, weather condition (e.g., cloudy, sunny), wind speed and direction, humidity, pressure, visibility, UV index, pollen level, pollution level, and chance of precipitation.
- **Sunrise and Sunset:** Essential for planning your day around daylight hours.

### Tide Data
- **Tide Times:** Retrieves both morning and evening times for low and high tides.
- **Tide Heights:** Provides heights corresponding to low and high tides, crucial for coastal activities and safety.

### Data Storage
- **CSV Logging:** Saves fetched data into a CSV file (`bbc_weather.csv`) on Google Drive. Each fetch appends new entries, ensuring a comprehensive record over time.

## Future Plans
The ultimate goal is to leverage accumulated data to develop a user-friendly weather application. This app will utilize historical data to provide insights into weather patterns, forecast trends, and personalized alerts. By harnessing the power of data analytics and user feedback, the aim is to create a valuable tool for weather enthusiasts, travelers, and anyone dependent on accurate weather information.

## Requirements
- **Python Environment:** Compatible with Python 3.x.
- **Libraries:** Requires `requests`, `datetime`, `pandas`, and `lxml` for web scraping and data manipulation.

## Getting Started
1. **Google Drive Setup:** Ensure Google Drive is mounted in your Python environment, such as Google Colab.
2. **Execute the Script:** Run the script (`bbc_weather_scraper.py`) to initiate data fetching and logging.
3. **Output Handling:** Weather data will be displayed in the console and simultaneously saved to `bbc_weather.csv` on your Google Drive.

## Customization
Feel free to customize the script to suit specific needs. You can modify data extraction parameters, enhance error handling, or integrate additional functionalities. This flexibility allows adaptation to diverse weather data requirements and potential future applications.

## Collaboration
Collaboration and feedback are welcome! Whether you're interested in enhancing the script's functionality, contributing to future app development, or sharing insights, your participation is valued. Together, we can create an innovative weather solution that benefits users worldwide.

Explore, experiment, and enjoy exploring weather data with this versatile Python script! ⛅🌍
