#same same but different

import os
import time
import requests
from datetime import datetime
import pandas as pd
from lxml import html
from google.colab import drive

today_date = datetime.now().strftime('%Y-%m-%d')

def map_level(code):
    """Maps single-letter codes to descriptive levels."""
    return {'L': 'Low', 'M': 'Medium', 'H': 'High'}.get(code, 'Unknown')

def scrape_tide_times(session):
    """Scrapes tide times from the specified URL."""
    url = 'https://www.bbc.co.uk/weather/coast-and-sea/tide-tables/2/113'
    response = session.get(url)
    tree = html.fromstring(response.content)

    tide_times = []

    for time_type in ['low', 'high']:
        times = []
        for period in ['morning', 'evening']:
            xpath = f'//*[@id="section-{today_date}"]/table/tbody/tr[{2 if time_type == "low" else 4}]/td[1]/span'
            elem = tree.xpath(xpath)
            times.append(elem[0].text.strip() if elem else "N/A")
        tide_times.append(tuple(times))

    return tide_times

def get_weather_data(session):
    """Fetches weather data from the specified URL and returns it as a dictionary."""
    url = 'https://www.bbc.com/weather/2643743'
    response = session.get(url)
    tree = html.fromstring(response.content)

    # Helper function to extract and clean data
    def extract_and_clean(xpath, elem_index=0, suffix=None, convert_to_float=False):
        elem = tree.xpath(xpath)
        if elem:
            text = elem[elem_index].text.strip()
            if suffix:
                text = text[:-len(suffix)]
            return float(text) if convert_to_float else text
        return "N/A"

    weather_data = {
        'Time of Search': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'High Temperature(°C)': extract_and_clean('//*[@id="daylink-0"]/div[4]/div[1]/div/div[4]/div/div[1]/span[2]/span/span[1]', suffix='°', convert_to_float=True),
        'Low Temperature(°C)': extract_and_clean('//*[@id="daylink-0"]/div[4]/div[1]/div/div[4]/div/div[2]/span[2]/span/span[1]', suffix='°', convert_to_float=True),
        'Current Temperature(°C)': extract_and_clean('//*[@id="wr-forecast"]/div[4]/div/div[1]/div[2]/div/div/div/div[2]/ol/li[1]/button/div[1]/div[2]/div[3]/div[2]/div/div/div[2]/span/span[1]', suffix='°', convert_to_float=True),
        'Weather Condition': extract_and_clean('//*[@id="wr-forecast"]/div[4]/div/div[1]/div[2]/div/div/div/div[2]/ol/li[1]/button/div[2]/div/span'),
        'Wind Speed': extract_and_clean('//*[@id="wr-forecast"]/div[4]/div/div[1]/div[2]/div/div/div/div[2]/ol/li[1]/button/div[1]/div[2]/div[3]/div[4]/div/span[3]/span/span[1]'),
        'Humidity(%)': extract_and_clean('//*[@id="wr-forecast"]/div[4]/div/div[1]/div[2]/div/div/div/div[2]/ol/li[1]/button/div[2]/div/div/div[1]/dl/dd[1]', suffix='%', convert_to_float=True),
        'Pressure(mb)': extract_and_clean('//*[@id="wr-forecast"]/div[4]/div/div[1]/div[2]/div/div/div/div[2]/ol/li[1]/button/div[2]/div/div/div[1]/dl/dd[2]', suffix=' mb'),
        'Visibility': extract_and_clean('//*[@id="wr-forecast"]/div[4]/div/div[1]/div[2]/div/div/div/div[2]/ol/li[1]/button/div[2]/div/div/div[1]/dl/dd[3]'),
        'Location': extract_and_clean('//*[@id="wr-location-name-id"]'),
        'Wind Direction': extract_and_clean('//*[@id="wr-forecast"]/div[4]/div/div[1]/div[2]/div/div/div/div[2]/ol/li[1]/button/div[2]/div/div/div[4]'),
        'UV Index': map_level(extract_and_clean('//*[@id="wr-forecast"]/div[4]/div/div[1]/div[4]/div/div[1]/div[2]/span[2]/span[1]/span[2]')),
        'Pollen': map_level(extract_and_clean('//*[@id="wr-forecast"]/div[4]/div/div[1]/div[4]/div/div[1]/div[2]/span[1]/span[1]/span[2]')),
        'Pollution': map_level(extract_and_clean('//*[@id="wr-forecast"]/div[4]/div/div[1]/div[4]/div/div[1]/div[2]/span[3]/span[1]/span[2]')),
        'Chance of Precipitation(%)': extract_and_clean('//*[@id="wr-forecast"]/div[4]/div/div[1]/div[2]/div/div/div/div[2]/ol/li[1]/button/div[1]/div[2]/div[3]/div[3]/div[2]', suffix='%', convert_to_float=True),
        'Sunset': extract_and_clean('//*[@id="wr-forecast"]/div[4]/div/div[1]/div[4]/div/div[1]/div[1]/span[2]/span[2]'),
        'Sunrise': extract_and_clean('//*[@id="wr-forecast"]/div[4]/div/div[1]/div[4]/div/div[1]/div[1]/span[1]/span[2]'),
        'Low Tide Morning': scrape_tide_times(session)[0][0],
        'High Tide Morning': scrape_tide_times(session)[1][0],
        'Low Tide Evening': scrape_tide_times(session)[0][1],
        'High Tide Evening': scrape_tide_times(session)[1][1],
    }

    print("Weather data fetched:")
    for key, value in weather_data.items():
        print(f"{key}: {value}")

    return weather_data

def save_to_google_drive(df, file_path):
    """Saves DataFrame to Google Drive."""
    df.to_csv(file_path, index=False)

def main():
    drive.mount('/content/drive')
    session = requests.Session()
    file_path = '/content/drive/My Drive/bbc_weather.csv'

    while True:
        try:
            weather_data = get_weather_data(session)

            df = pd.DataFrame([weather_data])
            if os.path.exists(file_path):
                existing_df = pd.read_csv(file_path)
                df = pd.concat([df, existing_df], ignore_index=True)

            save_to_google_drive(df, file_path)

            time.sleep(1800)  # Wait for 30 minutes before fetching data again
        except Exception as e:
            print(f"Error occurred: {e}")
            time.sleep(1800)  # Wait for 30 minutes before retrying

if __name__ == "__main__":
    main()
