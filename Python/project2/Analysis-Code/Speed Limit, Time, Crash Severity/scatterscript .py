
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from matplotlib.ticker import FormatStrFormatter

######################################################################

data = pd.read_csv("time_altered_analysis.csv")

dataset = data[['Time', 'Speed Limit', 'Total Units', 'Total Fatalities', 'Total Serious Injuries', 'Total Minor Injuries']]
cor = dataset.corr()
sns.heatmap(cor, square = True)

scaler = StandardScaler()
scaler.fit_transform(dataset)


model = KMeans(3)
model.fit(dataset)
clust = model.predict(dataset)
center = model.cluster_centers_
kmeans = pd.DataFrame(clust)
dataset.insert((dataset.shape[1]),'kmeans',kmeans)


ax = plt.figure().add_subplot(111)
scatter = ax.scatter(dataset['Speed Limit'],dataset['Time'], c=kmeans[0],s=10)
ax.set_xlabel('Speed Limit (km/hr)')
ax.set_ylabel('Time (HH.MM)')
ax.set_title('Cluster Graph - Crashes in Time Vs Speed Limit')
start, end = ax.get_ylim()
ax.yaxis.set_ticks(np.arange(start, end, 5.04))
ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
plt.colorbar(scatter)
plt.xticks(rotation=45)
