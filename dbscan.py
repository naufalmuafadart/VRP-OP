import matplotlib.pyplot as plt
from sklearn.datasets import make_circles
# from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd

df = pd.read_csv('./dataset/places.csv')
# df = df[df['id'] < 100]
df = df.head(99)

X = []
for i in range(len(df)):
    X.append([df.iloc[i]['latitude'].item(), df.iloc[i]['longitude'].item()])

# print(X)
# Create a concentric circle dataset
# X, _ = make_circles(n_samples=500, factor=.5, noise=.03, random_state=4)

# Apply DBSCAN to the dataset
kmeans = KMeans(n_clusters=1, random_state=42)
# Fit and predict clusters
clusters = kmeans.fit_predict(X)

# Print cluster assignments
print("Cluster labels:", clusters)

# Number of points per cluster
unique, counts = np.unique(clusters, return_counts=True)
print("Points per cluster:", dict(zip(unique, counts)))

df['cluster'] = clusters
print(df.head())
print(len(df))

# Plotting
# plt.scatter(X[:, 0], X[:, 1], c=clusters, cmap='viridis', marker='o')
# plt.title("DBSCAN Clustering of Concentric Circles")
# plt.xlabel("Feature 0")
# plt.ylabel("Feature 1")
# plt.show()