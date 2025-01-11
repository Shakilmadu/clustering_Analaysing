# -*- coding: utf-8 -*-
"""Untitled6.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1njOn70rR1fQebqYvinDW6efgUTZTtKKi
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import seaborn as sns

# Load Dataset
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data"
columns = ["age", "workclass", "fnlwgt", "education", "education_num", "marital_status", "occupation",
           "relationship", "race", "sex", "capital_gain", "capital_loss", "hours_per_week", "native_country", "income"]

data = pd.read_csv(url, header=None, names=columns, na_values="?")

# Drop missing values
data.dropna(inplace=True)

# Encode categorical features
label_encoders = {}
for column in data.select_dtypes(include=['object']).columns:
    le = LabelEncoder()
    data[column] = le.fit_transform(data[column])
    label_encoders[column] = le

# Normalize numerical features
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)

# K-Means Clustering
kmeans = KMeans(n_clusters=2, random_state=42)
kmeans_labels = kmeans.fit_predict(data_scaled)

# Evaluate K-Means
silhouette_kmeans = silhouette_score(data_scaled, kmeans_labels)

# Visualize Clusters using PCA
pca = PCA(n_components=2)
data_pca = pca.fit_transform(data_scaled)

plt.figure(figsize=(10, 7))
sns.scatterplot(x=data_pca[:, 0], y=data_pca[:, 1], hue=kmeans_labels, palette="viridis")
plt.title("K-Means Clustering Visualization (PCA)")
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.show()

# Hierarchical Clustering
hierarchical = AgglomerativeClustering(n_clusters=2)
hierarchical_labels = hierarchical.fit_predict(data_scaled)

# Evaluate Hierarchical Clustering
silhouette_hierarchical = silhouette_score(data_scaled, hierarchical_labels)

# Plot Dendrogram
from scipy.cluster.hierarchy import dendrogram, linkage
linked = linkage(data_scaled, method='ward')

plt.figure(figsize=(15, 7))
dendrogram(linked, truncate_mode='lastp', p=30, leaf_rotation=45, leaf_font_size=10)
plt.title("Hierarchical Clustering Dendrogram")
plt.show()

# Compare Metrics
print("Silhouette Score for K-Means:", silhouette_kmeans)
print("Silhouette Score for Hierarchical Clustering:", silhouette_hierarchical)