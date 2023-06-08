import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

from app.Machine_Learning.Analysis import AnalyzerBase


class ClusterAnalyzer(AnalyzerBase):

    def __init__(self, overrideData=None):
        super().__init__()

        if overrideData is not None:
            self.mergedData = overrideData

    def getClusterPlot(self, features, n_clusters=5, random_state=1, title='K-means Clustering'):
        reduced_data, labels, centroids = self.createClusterData(features, n_clusters, random_state)

        # Create a scatter plot
        plt.scatter(reduced_data[:, 0], reduced_data[:, 1], c=labels, cmap='viridis', alpha=0.5)
        plt.scatter(centroids[:, 0], centroids[:, 1], marker='x', color='white', linewidths=2, s=100)

        # Add labels and title to the plot
        plt.xlabel('PC1')
        plt.ylabel('PC2')
        plt.title(title)

        plt.xticks([])
        plt.yticks([])

        return plt

    def createClusterData(self, features, n_clusters=5, random_state=1):
        # Subset the data based on the selected features
        dataframe = self.mergedData[features].dropna()

        # Convert categorical variables to dummy/indicator variables
        X = pd.get_dummies(dataframe, columns=features)

        # Perform dimensionality reduction using PCA
        reduced_data = PCA(n_components=2).fit_transform(X)

        # Apply K-means clustering
        kmeans = KMeans(init="k-means++", n_clusters=n_clusters, n_init=4, random_state=random_state)

        kmeans.fit(reduced_data)
        labels = kmeans.labels_
        centroids = kmeans.cluster_centers_

        return reduced_data, labels, centroids
