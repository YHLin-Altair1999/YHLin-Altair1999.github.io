"""
This code is made by Yen-Hsing Lin (NTHU/TOP) on 2024.04.22.
The goal is to use this code to visualize the relative contribution from different types of observatories
(private, university, high school, etc.) to the ExoClock Project within the Taiwan astronomical
Observation collaboration Platform (TOP), with a stacked bar chart.

The code takes in the CSV file generated by the "Make_ObserveTable.py" code and performs statistics
to analyze the relative contributions. It's worth noting that for the code to work, it requires another file
"observatory_info.csv", which describes the mapping between the observatory's name and the category it belongs to.
This file needs to be manually maintained. One way to efficiently use it is to run this code, identify which
observatories are assigned to "Other", and then add those observatories to the "observatory_info.csv" file.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Set LaTeX rendering and font for plots
#plt.rcParams.update({"text.usetex": True})
#plt.rcParams['font.family'] = 'STIXGeneral'


class TransitObservationAnalysis:
    """
    A class to analyze transit observations and plot a stacked bar chart
    showing the accumulated number of observations by observatory type over time.
    """

    def __init__(self, observation_file, observatory_info_file):
        """
        Initialize the TransitObservationAnalysis object.

        Args:
            observation_file (str): Path to the CSV file containing observation data.
            observatory_info_file (str): Path to the CSV file containing observatory information.
        """
        self.observation_data = pd.read_csv(observation_file)
        self.observatory_info = pd.read_csv(observatory_info_file)
        self.process_data()

    def process_data(self):
        """
        Process the observation and observatory data to prepare for analysis.
        """
        # Convert observation dates to datetime format
        self.observation_data['Observation Date'] = pd.to_datetime(self.observation_data['Observation Date'])

        # Extract month and year from observation dates
        self.observation_data['Month'] = self.observation_data['Observation Date'].dt.month
        self.observation_data['Year'] = self.observation_data['Observation Date'].dt.year

        # Merge observatory information with observation data
        self.observation_data = pd.merge(self.observation_data, self.observatory_info, left_on='Observatory',
                                         right_on='Observatory', how='left')

        # Fill missing observatory types with 'Others'
        self.observation_data['Type'] = self.observation_data['Type'].fillna('Others')
        print(self.observation_data[self.observation_data['Type']=='Others'])

    def plot_stacked_bar_chart(self):
        """
        Plot a stacked bar chart showing the accumulated number of observations by observatory type over time.
        """
        # Group observations by month, year, and observatory type, and count the occurrences
        grouped_data = self.observation_data.groupby(['Month', 'Year', 'Type']).size().reset_index(name='Count')

        # Sort the data by month and year
        grouped_data = grouped_data.sort_values(['Year', 'Month'])

        # Create a date range from the first observation to now
        min_year = grouped_data['Year'].min()
        min_month = grouped_data[grouped_data['Year'] == min_year]['Month'].min()

        first_observation = datetime(min_year, min_month, 1)
        current_month = datetime.now().replace(day=1)
        date_range = pd.date_range(start=first_observation, end=current_month, freq='MS')

        # Create a template dataframe with all months
        template = pd.DataFrame({'date': date_range})
        template['Year'] = template['date'].dt.year
        template['Month'] = template['date'].dt.month
        template['Year_Month'] = template['date'].dt.strftime('%Y-%m')

        # Split the data by observatory type and merge with the template to fill missing months
        dfs = {name: group.drop('Type', axis=1) for name, group in grouped_data.groupby('Type')}
        for name, group in dfs.items():
            dfs[name] = template.merge(group, how='left', on=['Year', 'Month']).fillna(0)

        # Calculate the accumulated count for each observatory type
        for name, group in dfs.items():
            group['Accumulated_Count'] = [sum(group['Count'][:i + 1]) for i in range(len(group))]

        # Sort the categories based on their contribution (total accumulated count) in descending order
        sorted_categories = sorted(dfs.keys(), key=lambda x: dfs[x]['Accumulated_Count'].iloc[-1], reverse=True)
        
        # Create the stacked bar chart
        fig, ax = plt.subplots(figsize=(8, 4))
        bottom = np.zeros(len(template['Year_Month']))
        colors = ['C{}'.format(i) for i in range(len(sorted_categories))]  # Assign colors based on the sorted order
        for name, color in zip(sorted_categories, colors):
            group = dfs[name]
            print(f"{name} has {group['Accumulated_Count'].iloc[-1]} observations")
            ax.bar(group['Year_Month'], group['Accumulated_Count'], label=name, bottom=bottom, color=color)
            bottom += group['Accumulated_Count']

        # Set plot title and axis labels
        current_date = datetime.now().strftime("%Y-%m-%d")
        ax.set_title(f'Accumulated Number of TOP ExoClock Observations ({current_date})')
        ax.set_ylabel('Accumulated Number of Observations')

        # Adjust x-axis ticks and labels
        k = 2  # Display a tick every 6 months
        all_labels = group['Year_Month'].tolist()
        ax.set_xticks(all_labels[::k])  # Select every kth label
        ax.set_xticklabels(all_labels[::k], rotation=45)

        # Add legend
        ax.legend()

        # Adjust spacing between subplots
        plt.tight_layout()

        # Save the plot
        fig.savefig("ExoClock_TransitStatistics.png", dpi=300)


# Usage example
if __name__ == '__main__':
    observation_file = 'TOP_ObservationLog.csv'
    observatory_info_file = 'observatory_info.csv'  # Provide the observatory information file

    analysis = TransitObservationAnalysis(observation_file, observatory_info_file)
    analysis.plot_stacked_bar_chart()