# ⛅ BBC Weather and Tide Times Scraper 🌊

This script scrapes weather data and tide times from the BBC Weather website and outputs it to a CSV file in Google Drive.

## 📋 Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Functions](#functions)
  - [map_level](#map_level)
  - [scrape_tide_times](#scrape_tide_times)
  - [get_weather_data](#get_weather_data)
  - [save_to_google_drive](#save_to_google_drive)
- [Scheduler](#scheduler)
- [Notes](#notes)

## 📦 Requirements

- Python 3.x
- Google Colab
- Packages: `os`, `time`, `requests`, `datetime`, `pandas`, `lxml`, `google.colab`

## 🛠 Installation

1. **Google Colab**: This script is designed to run in Google Colab, so there's no need to install anything on your local machine. Simply open a new notebook in Google Colab and copy the script.

2. **Install required packages**:
    ```python
    !pip install requests pandas lxml google-colab
    ```

## 🚀 Usage

1. **Mount Google Drive**:
    The script automatically mounts your Google Drive to save the output CSV file.

2. **Run the script**:
    Execute the script in Google Colab. The script will scrape the weather data and tide times, then save it to a CSV file in your Google Drive.

3. **Schedule**:
    The script fetches the data every 30 minutes and appends it to the existing CSV file.

## 🔧 Functions

### `map_level(code)` 🗺️
Maps single-letter codes to descriptive levels.

- **Parameters**: `code` (str) - Single-letter code.
- **Returns**: `str` - Descriptive level.

### `scrape_tide_times()` 🌊
Scrapes the tide times from the BBC tide tables page.

- **Returns**: `list` - List of tuples containing morning and evening low/high tide times.

### `get_weather_data()` ⛅
Scrapes weather data from the BBC Weather page and tide times from the BBC tide tables page.

- **Returns**: `dict` - Dictionary containing weather data and tide times.

### `save_to_google_drive(df, file_path)` 💾
Saves the DataFrame to a CSV file in Google Drive.

- **Parameters**:
  - `df` (pandas.DataFrame) - DataFrame containing weather data.
  - `file_path` (str) - Path to the CSV file in Google Drive.

## ⏰ Scheduler

The script fetches the data every 30 minutes and appends it to the existing CSV file in Google Drive.

## 📝 Notes

- Ensure you have a stable internet connection while running the script in Google Colab.
- The CSV file will be saved in your Google Drive at `/content/drive/My Drive/bbc_weather.csv`.

---

By using this script, you can continuously monitor and log weather data and tide times from the BBC website, saving it conveniently in your Google Drive for further analysis.
