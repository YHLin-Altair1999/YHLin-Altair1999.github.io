import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

#plt.rcParams.update({"text.usetex": True})
#plt.rcParams['font.family'] = 'STIXGeneral'

# Sample DataFrame
df = pd.read_excel('Exoclock.xlsx', names=['Name', 'Observations'])

# Sort the DataFrame by the number of observations in descending order
df = df.sort_values(by='Observations', ascending=False)

# Create a rank column based on the sorted order
df['Rank'] = range(1, len(df) + 1)
#print(df['Rank'])
# Find the rank of "Yen-Hsing Lin"
yen_hsing_lin_rank = df[df['Name'] == "Yen-Hsing Lin"]['Rank'].values[0]
yen_hsing_lin_num = df[df['Name'] == "Yen-Hsing Lin"]['Observations'].values[0]

# Create the bar plot
fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(df['Rank'], df['Observations'], color='b')
ax.bar(yen_hsing_lin_rank, df[df['Name'] == "Yen-Hsing Lin"]['Observations'], color='r', label=f'Yen-Hsing Lin (Rank {yen_hsing_lin_rank}, {yen_hsing_lin_num} obs.)')

ax.set_xlim(0, yen_hsing_lin_rank*1.1)
ax.set_xlabel('Rank')
ax.set_ylabel('Number of Observations')
ax.set_title(f'ExoClock Observer Rank ({datetime.now().strftime("%Y-%m-%d")})')
# Show the plot
#ax.set_yscale('log')
plt.legend()
plt.tight_layout()
fig.savefig('Exoclock_ObserverRank.png', dpi=300)
#plt.show()
