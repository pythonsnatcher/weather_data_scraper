from google.colab import drive
import requests
from datetime import datetime
from lxml import html
import pytz
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

# Get today's date in the required format (e.g., '2023-07-12')
today_date = datetime.now().strftime('%Y-%m-%d')

# Mount Google Drive
drive.mount('/content/drive')

# Define London timezone
london_tz = pytz.timezone('Europe/London')

# Get the current time in London timezone
now_london = datetime.now(london_tz)

# Format the current time as YYYY-MM-DD HH:MM in London time
time_of_search = now_london.strftime('%Y-%m-%d %H:%M')

def map_level(code):
    """Maps single-letter codes to descriptive levels."""
    return {'L': 'Low', 'M': 'Medium', 'H': 'High'}.get(code, 'Unknown')



def scrape_tide_times(session):
    """Scrapes tide times and heights from the specified URL."""
    url = 'https://www.bbc.co.uk/weather/coast-and-sea/tide-tables/2/113'
    response = session.get(url)
    tree = html.fromstring(response.content)

    tide_times = []

    # Extract low tide times and heights
    low_tide_xpath_morning_time = f'//*[@id="section-{today_date}"]/table/tbody/tr[1]/td[1]/span'
    low_tide_xpath_morning_height = f'//*[@id="section-{today_date}"]/table/tbody/tr[1]/td[2]'
    low_tide_xpath_evening_time = f'//*[@id="section-{today_date}"]/table/tbody/tr[3]/td[1]/span'
    low_tide_xpath_evening_height = f'//*[@id="section-{today_date}"]/table/tbody/tr[3]/td[2]'

    low_tide_elem_morning_time = tree.xpath(low_tide_xpath_morning_time)
    low_tide_elem_morning_height = tree.xpath(low_tide_xpath_morning_height)
    low_tide_elem_evening_time = tree.xpath(low_tide_xpath_evening_time)
    low_tide_elem_evening_height = tree.xpath(low_tide_xpath_evening_height)
    
    low_tide_time_morning = low_tide_elem_morning_time[0].text.strip() if low_tide_elem_morning_time else "N/A"
    low_tide_height_morning = low_tide_elem_morning_height[0].text.strip() if low_tide_elem_morning_height else "N/A"
    low_tide_time_evening = low_tide_elem_evening_time[0].text.strip() if low_tide_elem_evening_time else "N/A"
    low_tide_height_evening = low_tide_elem_evening_height[0].text.strip() if low_tide_elem_evening_height else "N/A"

    tide_times.append((low_tide_time_morning, low_tide_height_morning, low_tide_time_evening, low_tide_height_evening))

    # Extract high tide times and heights
    high_tide_xpath_morning_time = f'//*[@id="section-{today_date}"]/table/tbody/tr[2]/td[1]/span'
    high_tide_xpath_morning_height = f'//*[@id="section-{today_date}"]/table/tbody/tr[2]/td[2]'
    high_tide_xpath_evening_time = f'//*[@id="section-{today_date}"]/table/tbody/tr[4]/td[1]/span'
    high_tide_xpath_evening_height = f'//*[@id="section-{today_date}"]/table/tbody/tr[4]/td[2]'

    high_tide_elem_morning_time = tree.xpath(high_tide_xpath_morning_time)
    high_tide_elem_morning_height = tree.xpath(high_tide_xpath_morning_height)
    high_tide_elem_evening_time = tree.xpath(high_tide_xpath_evening_time)
    high_tide_elem_evening_height = tree.xpath(high_tide_xpath_evening_height)

    high_tide_time_morning = high_tide_elem_morning_time[0].text.strip() if high_tide_elem_morning_time else "N/A"
    high_tide_height_morning = high_tide_elem_morning_height[0].text.strip() if high_tide_elem_morning_height else "N/A"
    high_tide_time_evening = high_tide_elem_evening_time[0].text.strip() if high_tide_elem_evening_time else "N/A"
    high_tide_height_evening = high_tide_elem_evening_height[0].text.strip() if high_tide_elem_evening_height else "N/A"

    tide_times.append((high_tide_time_morning, high_tide_height_morning, high_tide_time_evening, high_tide_height_evening))

    return tide_times


def convert_to_datetime(time_str):
    """Converts a string time format into datetime format."""
    try:
        return datetime.strptime(time_str, '%H:%M')
    except ValueError:
        return "N/A"


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

    # Fetch tide times dynamically
    tide_times = scrape_tide_times(session)

    weather_data = {
        'Time of Search': time_of_search,
        'High Temperature(°C)': extract_and_clean('//*[@id="daylink-0"]/div[4]/div[1]/div/div[4]/div/div[1]/span[2]/span/span[1]', suffix='°', convert_to_float=True),
        'Low Temperature(°C)': extract_and_clean('//*[@id="daylink-0"]/div[4]/div[1]/div/div[4]/div/div[2]/span[2]/span/span[1]', suffix='°', convert_to_float=True),
        'Current Temperature(°C)': extract_and_clean('//*[@id="wr-forecast"]/div[4]/div/div[1]/div[2]/div/div/div/div[2]/ol/li[1]/button/div[1]/div[2]/div[3]/div[2]/div/div/div[2]/span/span[1]', suffix='°', convert_to_float=True),
        'Weather Condition': extract_and_clean('//*[@id="wr-forecast"]/div[4]/div/div[1]/div[2]/div/div/div/div[2]/ol/li[1]/button/div[2]/div/span'),
        'Wind Speed(mph)': extract_and_clean('//*[@id="wr-forecast"]/div[4]/div/div[1]/div[2]/div/div/div/div[2]/ol/li[1]/button/div[1]/div[2]/div[3]/div[4]/div/span[3]/span/span[1]'),
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
        'Low Tide Morning Time': tide_times[0][0],
        'Low Tide Morning Height(M)': tide_times[0][1],
        'High Tide Morning Time': tide_times[1][0],
        'High Tide Morning Height(M)': tide_times[1][1],
        'Low Tide Evening Time': tide_times[0][2],
        'Low Tide Evening Height(M)': tide_times[0][3],
        'High Tide Evening Time': tide_times[1][2],
        'High Tide Evening Height(M)': tide_times[1][3],
        
    }

    return weather_data


def update_google_sheet(weather_data):
    """Updates the Google Sheet with the fetched weather data."""
    # Load credentials from JSON key file
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('/content/drive/My Drive/weather-data-429210-af2c31cf7a66.json', scope)
    
    # Authorize the client and open the spreadsheet
    gc = gspread.authorize(credentials)
    sheet_url = 'https://docs.google.com/spreadsheets/d/1Z9VKcE05zaiLd6rUOWAuvDVOzcB6B6qPs2EvGBUPQL4/edit?gid=0#gid=0'
    worksheet = gc.open_by_url(sheet_url).sheet1  # Open the first sheet

    # Append new data to the spreadsheet
    new_row = [weather_data[key] for key in weather_data.keys()]
    worksheet.append_row(new_row)
    print("Updated Google Sheet successfully!")
    
def main():
    """Main function to fetch weather data and update Google Sheet."""
    while True:
        try:
            # Start a session
            session = requests.Session()

            # Fetch weather data
            weather_data = get_weather_data(session)

            # Update Google Sheet
            update_google_sheet(weather_data)

            print("Weather data updated successfully.")

            # Wait for 30 minutes
            time.sleep(1800)  # 1800 seconds = 30 minutes

        except Exception as e:
            print(f"Error occurred: {e}")
            print("Retrying in 30 minutes...")
            time.sleep(1800)  # Wait for 30 minutes before retrying

# Run the main function
if __name__ == "__main__":
    main()

    
