import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

from matplotlib.font_manager import FontProperties
font = FontProperties(fname='/Library/Fonts/Arial Unicode.ttf', size=10)
df1 = pd.read_csv('./output/201812.csv', encoding='utf-8')
df1 = df1[df1['TownID'] == 'A17'].reset_index(drop=True)
df1 = df1[['Time', 'Longitude', 'Latitude', 'Age1', 'Age2', 'Age3', 'Age4', 'Age5', 'Age6', 'Total']]
df1["Time"] = pd.to_datetime(df1["Time"])
df1["day"] = df1["Time"].dt.day
df1["hour"] = df1["Time"].dt.hour
df1 = df1[df1['day'] == 31].reset_index(drop=True)
# df1 = df1[df1['Longitude'] < 121.56].reset_index(drop=True)
# df1 = df1[df1['Latitude'] < 25.055].reset_index(drop=True)
# df1 = df1[df1['Longitude'] > 121.54].reset_index(drop=True)
# df1 = df1[df1['Latitude'] > 25.045].reset_index(drop=True)
df1.to_csv('out.csv')
time = sorted(df1['hour'].unique().tolist())

dd = pd.to_datetime(pd.Series(time), format='%H')
dd = dd.apply(lambda i: i.strftime('%H:%M:%S'))

# total = df1.groupby('hour')['Total'].sum()
age1 = df1.groupby('hour')['Age1'].sum()
age2 = df1.groupby('hour')['Age2'].sum()
age3 = df1.groupby('hour')['Age3'].sum()
age4 = df1.groupby('hour')['Age4'].sum()
age5 = df1.groupby('hour')['Age5'].sum()
age6 = df1.groupby('hour')['Age6'].sum()
plt.plot(dd, age1, color='blue', label="Age0-19")
plt.plot(dd, age2, color='orange', label="Age20-29")
plt.plot(dd, age3, color='green', label="Age30-39")
plt.plot(dd, age4, color='red', label="Age40-49")
plt.plot(dd, age5, color='purple', label="Age50-59")
plt.plot(dd, age6, color='brown', label="Age60-99")
plt.xlabel('TIME')
plt.ylabel('POPULATION')
plt.legend(loc=2)
plt.xticks(rotation=45)
plt.ylim(top=5000)
plt.title("平常日20180715-台北小巨蛋", fontproperties=font, fontsize=20)
plt.show()