from bs4 import BeautifulSoup
import pandas as pd
import re
import requests
import matplotlib.pyplot as plt

# URL of the web page you want to download
url = "https://www.exoclock.space/database/observations_by_observer"
fname_html = 'Exoclock.html'
fname_xlsx = 'Exoclock.xlsx'

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

file_path = 'Exoclock.html'  # Replace 'your_data.txt' with the actual file path
with open(file_path, 'r', encoding="utf-8") as file:
    data = file.read()

# Parse the HTML using Beautiful Soup
soup = BeautifulSoup(data, 'lxml')
bullet_points = str(soup.find('div', class_='col-sm-12 col-md-3')).split("• ")

# Initialize lists to store extracted data
names = []
observations = []

for bullet_point in bullet_points[1:]:
    # Extract name and observations from the bullet points
    bullet_point = BeautifulSoup(bullet_point, 'lxml')
    name = bullet_point.find('a', style="padding-bottom:10px; color:#C46127").get_text()
    #observation = float(re.search(r'([\d.]+)\s*Observation\(s\)', str(bullet_point)).group(1))
    #text_content = bullet_point.get_text()
    #obs_text = text_content.split("Observation(s)")[0].strip()
    #print(obs_text)
    observation = float(str(bullet_point).split('<br/>')[1].split(' ')[0])
    names.append(name)
    observations.append(observation)

# Create a pandas DataFrame
data = {'Name': names, 'Observations': observations}
df = pd.DataFrame(data)
df.to_excel(fname_xlsx, index=False, header = False, engine='openpyxl')
print(f"Observer statistics in now stored in {fname_xlsx}.")
'''
# Sort the DataFrame by the number of observations in descending order
df = df.sort_values(by='Observations', ascending=False)

# Create a rank column based on the sorted order
df['Rank'] = range(1, len(df) + 1)
# Find the rank of "Yen-Hsing Lin"
yen_hsing_lin_rank = df[df['Name'] == "Yen-Hsing Lin"]['Rank'].values[0]

# Create the bar plot
fig, ax = plt.subplots(figsize=(5, 3))
ax.bar(df['Rank'], df['Observations'], color='b')
ax.bar(yen_hsing_lin_rank, df[df['Name'] == "Yen-Hsing Lin"]['Observations'], color='r', label=f'Yen-Hsing Lin (Rank {yen_hsing_lin_rank})')

ax.set_xlim(0, yen_hsing_lin_rank*1.1)
ax.set_xlabel('Rank')
ax.set_ylabel('Number of Observations')
ax.set_yscale('log')
ax.legend()
plt.tight_layout()
fig.savefig('Exoclock_ObservationStatistics.png', dpi=300)
'''