# BBC Weather Data Scraper 🌦️📊

## Overview
The BBC Weather Data Scraper is a Python script designed to fetch real-time weather data and tide times from the BBC Weather and BBC Coast & Sea websites using web scraping techniques. It retrieves various weather metrics such as temperature, humidity, wind speed, visibility, UV index, pollen count, pollution level, sunrise, sunset times, and tide timings for both morning and evening periods. The fetched data is stored in a CSV file on Google Drive, allowing for easy access, analysis, and historical tracking of weather conditions.

## Features
- **Real-time Weather Data**: Fetches current weather conditions including temperature (high, low, and current), humidity, wind speed, visibility, UV index, pollen count, pollution level, sunrise, and sunset times.
- **Tide Times**: Scrapes tide timings for both low and high tides in the morning and evening from BBC Coast & Sea.
- **Data Storage**: Saves all fetched data into a CSV file (`bbc_weather.csv`) stored on Google Drive, ensuring a persistent record of weather and tide information over time.
- **Automatic Updates**: Runs the data fetching process automatically at regular intervals (every 30 minutes by default) to ensure the data is up-to-date.

## Requirements
- Python 3.x
- Python libraries: `requests`, `pandas`, `lxml`
- Google account (for Google Drive API access)

## Installation
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-repo/bbc_weather_scraper.git
   cd bbc_weather_scraper
