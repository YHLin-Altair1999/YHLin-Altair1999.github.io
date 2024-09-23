"""
Exoclock Observation Catalog Retrieval

This script retrieves the observation catalog from Exoclock's website, filters the data for specific observers from the Taiwan Astronomical Observation Collaboration Platform (TOP), and creates an Excel file sorted by observation date.

Dependencies:
    - BeautifulSoup (bs4)
    - pandas
    - requests

Parameters:
    url (str): URL of the web page containing the observation catalog.
    fname_html (str): File name to save the downloaded HTML content.
    fname_xlsx (str): File name to save the processed data as an Excel file.
    target_observer_names (list): List of observer names from TOP to filter for.

Returns:
    None

Usage:
    - Run the script to download the observation catalog HTML.
    - Extract relevant data for specified observers.
    - Save the filtered data as an Excel file.

Example:
    ```bash
    python observation_script.py
    ```

Note:
    Make sure to customize the 'target_observer_names' list according to the specific observers you are interested in tracking.

Author:
    Yen-Hsing Lin (julius52700@gapp.nthu.edu.tw)
    Docstring created using ChatGPT (GTP3.5)
"""

from bs4 import BeautifulSoup
import pandas as pd
import requests

# URL of the web page you want to download
url = "https://www.exoclock.space/database/observations_by_observer"
fname_html = 'Exoclock.html'
fname_xlsx = 'TOP_ObservationLog.xlsx'
fname_csv = 'TOP_ObservationLog.csv'
target_observer_names = pd.read_excel('observer_list.xlsx')['Name'].tolist()

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Get the content of the response, which contains the HTML
    html_content = response.text

    # Open the file in binary write mode and save the HTML content
    with open(fname_html, "w", encoding="utf-8") as file:
        file.write(html_content)

    print(f"HTML file downloaded and saved as {fname_html}")
else:
    print(f"Failed to download the HTML. Status code: {response.status_code}")

with open(fname_html, 'r', encoding="utf-8") as file:
    data = file.read()

html_content = data

# Parse HTML using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find all rows in the table
rows = soup.find_all('tr', {'style': 'border-bottom: dotted 1px'})

# Initialize lists to store extracted data
planet_names = []
observation_dates = []
observers = []
observatories = []
links = []

# Extract data from each row
for row in rows:
    columns = row.find_all('td')
    
    # Extracting data from columns
    planet_name = columns[0].find('font').text.strip()
    observation_date = columns[0].contents[-1]
    observer = columns[1].contents[0]
    observatory = columns[1].contents[2]
    #link = columns[4].contents[0]
    link = 'https://www.exoclock.space' + columns[4].find_all('a', href=True)[0]['href']
    
    if observer in target_observer_names:
        # Append data to lists
        planet_names.append(planet_name)
        observation_dates.append(observation_date)
        observers.append(observer)
        observatories.append(observatory)
        links.append(link)

# Create a Pandas DataFrame
data = {
    'Planet': planet_names,
    'Observation Date': observation_dates,
    'Observer': observers,
    'Observatory': observatories,
    'Links': links
}

df = pd.DataFrame(data).sort_values(by='Observation Date')
df.to_excel(fname_xlsx, index=False, engine='openpyxl')
df.to_csv(fname_csv, index=False)