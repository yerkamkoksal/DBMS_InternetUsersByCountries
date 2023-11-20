# -*- coding: utf-8 -*-
"""InternetUsersByCountry

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BOBnOq7WqVfz20RiUzfl3cCnuNlKBQPw
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from os.path import join

# %matplotlib inline

"""names of the views from mySQL

"""

#community_mobile_vs_internet_users
#democracy_vs_subs
#most_free_and_democratic_countries
#ststs_for_highest_internet_usage_country
#ststs_for_lowest_internet_usage_country

"""the mySQL views are exported from github

# COMMUNITY MOBILE VS. INTERNET USERS
"""

url= 'https://raw.githubusercontent.com/tansylu/view-dumps/main/community_mobile_vs_internet_users.csv'
df = pd.read_csv(url, on_bad_lines='skip', sep=";")
df = df.sort_values(by='Mobile_vs_Internet')
grouped_df = df.groupby('Year')

# Create a scatter plot for each country
fig, ax = plt.subplots(figsize=(8,40))

for name, group in grouped_df:
    group.plot(x='Mobile_vs_Internet', y='Country_name', ax=ax, label=name, kind='scatter', s=50)
ax.set_xlabel('Ratio')
ax.set_ylabel('Countries')
ax.set_title('Mobile vs. Internet Users Rate by Country and Year')

ax.legend(title='Country')

plt.show()

"""# DEMOCRACY VS. SUBSCRIPTIONS"""

url= 'https://raw.githubusercontent.com/tansylu/view-dumps/main/democracy_vs_subs.csv'
df = pd.read_csv(url, on_bad_lines='skip', sep=";")

grouped = df.groupby('Country_name')

fig, axs = plt.subplots(2, 2, figsize=(25, 8))

# Create a subplot for each variable
axs[0, 0].bar(grouped.groups.keys(), grouped['Mobile_cellular_subscriptions'].last(), color='red')
axs[0, 0].set_title('Mobile Cellular Subscriptions')
axs[0, 0].tick_params(axis='x', rotation=90)

axs[0, 1].bar(grouped.groups.keys(), grouped['Landline_internet_subscriptions'].last(), color='green')
axs[0, 1].set_title('Landline Internet Subscriptions')
axs[0, 1].tick_params(axis='x', rotation=90)

axs[1, 0].bar(grouped.groups.keys(), grouped['Freedom_estimate'].last(), color='blue')
axs[1, 0].set_title('Freedom Estimate')
axs[1, 0].tick_params(axis='x', rotation=90)

axs[1, 1].bar(grouped.groups.keys(), grouped['Democracy_estimate'].last(), color='orange')
axs[1, 1].set_title('Democracy Estimate')
axs[1, 1].tick_params(axis='x', rotation=90)

plt.tight_layout()
plt.show()

"""MOST FREE AND DEMOCRATIC COUNTRIES"""

url= 'https://raw.githubusercontent.com/tansylu/view-dumps/main/most_free_and_democratic_countries.csv'
df = pd.read_csv(url, on_bad_lines='skip', sep=";")

plt.figure(figsize = (20,12))
plt.scatter(df['Democracy_estimate'], df['Freedom_estimate'])
plt.title('Democracy vs. Freedom')
plt.xlabel('Democracy Estimate')
plt.ylabel('Freedom Estimate')

# Add labels for each point
for i, row in df.iterrows():
    plt.annotate(row['Country_name'], (row['Democracy_estimate'], row['Freedom_estimate']),rotation = 25)

# Show the scatter plot
plt.show()

"""# STATS FOR HIGHEST INTERNET USAGE FOR COUNTRIES




"""

url= 'https://raw.githubusercontent.com/tansylu/view-dumps/main/stats_for_highest_internet_usage_country.csv'
df = pd.read_csv(url, on_bad_lines='skip', sep=";")
plt.figure(figsize = (25,20))

plt.subplot(2, 1, 1)
plt.stackplot(df['Country_name'], df['Urban_population'], df['Electricity_access_urban'], labels=['Urban Population', 'Electricity Access'])
plt.legend(loc='upper left')
plt.xlabel('Country')
plt.ylabel('Population (in millions)')
plt.title('Distribution of Urban Population with Electricity Access Highlighted')
plt.tick_params(axis='x', rotation=90)

plt.subplot(2, 2, 3)
plt.plot(df['max_internet_users_year'], df['Internet_users'], color='blue')
plt.axvline(df['max_internet_users_year'].iloc[0], color='red', linestyle='--')
plt.xlabel('Year')
plt.ylabel('Internet Users (in % of population)')
plt.title('Internet Usage Trend with Max Year Highlighted')

plt.subplot(2, 2, 4)
plt.hist(df['GDP'], bins=20)
plt.xlabel('GDP (in USD)')
plt.ylabel('Count')
plt.title('Distribution of GDP Values across Countries')

"""STATS FOR LOWEST INTERNET USAGE COUNTRY"""

url= 'https://raw.githubusercontent.com/tansylu/view-dumps/main/stats_for_lowest_internet_usage_country.csv'
df = pd.read_csv(url, on_bad_lines='skip', sep=";")
df.head()

#!pip install geopandas

import geopandas as gpd

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world = world[(world.name!="Antarctica")]
world.head()

# df3=df[["Country_name","min_internet_users_year"]].copy()
# df3.head()
# df3.rename(columns={"Country_name":"name"},inplace=True)
# import matplotlib.colors as colors
# cmap = plt.get_cmap('RdYlGn')

# cmap = colors.ListedColormap(cmap(np.linspace(0, 0.7, cmap.N))[::-1])

# merged = pd.merge(world,df3,on = "name",how="outer")
# merged.plot(column='min_internet_users_year', figsize=(20, 10), legend=True,missing_kwds={'color': 'lightgrey'},cmap=cmap).set_axis_off()

# plt.title("Lowest Internet Usage Year")
# plt.show()


df3=df[["Country_name","min_internet_users_year", "Code"]].copy()
df3.rename(columns={"Country_name":"name"},inplace=True)

# Step 4: Merge world geospatial data with DataFrame
merged = world.merge(df3, left_on='iso_a3', right_on='Code', how='left')

# Step 5: Set up colormap
cmap = plt.cm.get_cmap('RdYlGn_r')

# Step 6: Set up color range based on min and max years
min_year = merged['min_internet_users_year'].min()
max_year = merged['min_internet_users_year'].max()

# Step 7: Plot world map heatmap
fig, ax = plt.subplots(figsize=(20, 10))
merged.plot(column='min_internet_users_year', cmap=cmap, linewidth=0.8, ax=ax, edgecolor='0.5', vmin=min_year, vmax=max_year)

# Step 8: Add colorbar
sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=min_year, vmax=max_year))
cbar = fig.colorbar(sm)

# Step 9: Set axis off and display plot
ax.set_axis_off()
plt.title("Year Heatmap")
plt.show()