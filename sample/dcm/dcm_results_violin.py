import pandas as pd

from utils.charts import get_violinchart
from utils.misc import load_from_csv


db_data_300 = load_from_csv("/Users/hugo/Desktop/PyCRE/dcm/csv/", "dcm_cluster_statistics_300-backup.csv")
db_data_300.columns = ['Mean Number of Clusters', 'Mean Number of Samples per Clusters', 'Number of Outliers']
db_data_300 = db_data_300.assign(Algorithm='DBSCAN')

kmeans_data_300 = load_from_csv("/Users/hugo/Desktop/PyCRE/dcm/csv/", "dcmk_cluster_statistics_300-backup.csv")
kmeans_data_300.columns = ['Mean Number of Clusters', 'Mean Number of Samples per Clusters', 'Number of Outliers']
kmeans_data_300 = kmeans_data_300.assign(Algorithm='KMeans')

# Birch
birch_data_300 = load_from_csv("/Users/hugo/Desktop/PyCRE/dcm/csv/", "dcmk_cluster_statistics_300-backup.csv")
birch_data_300.columns = ['Mean Number of Clusters', 'Mean Number of Samples per Clusters', 'Number of Outliers']
birch_data_300 = birch_data_300.assign(Algorithm='Birch')

# 300
frames = [db_data_300, kmeans_data_300, birch_data_300]
result = pd.concat(frames)
get_violinchart(result, 300)

