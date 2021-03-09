from utils.charts import get_barchart
from utils.misc import load_from_csv

path = "/Users/hugo/Desktop/PyCRE/dcm/images/"

db_data_300 = load_from_csv("/Users/hugo/Desktop/PyCRE/dcm/csv/", "dcm_cluster_statistics_300-backup.csv")
db_data_600 = load_from_csv("/Users/hugo/Desktop/PyCRE/dcm/csv/", "dcm_cluster_statistics_600-backup.csv")
db_data_900 = load_from_csv("/Users/hugo/Desktop/PyCRE/dcm/csv/", "dcm_cluster_statistics_900-backup.csv")
db_data_1200 = load_from_csv("/Users/hugo/Desktop/PyCRE/dcm/csv/", "dcm_cluster_statistics_1200-backup.csv")

db_data_300.columns = ['Number of Clusters', 'Number of Samples per Clusters', 'Number of Outliers']
db_data_600.columns = ['Number of Clusters', 'Number of Samples per Clusters', 'Number of Outliers']
db_data_900.columns = ['Number of Clusters', 'Number of Samples per Clusters', 'Number of Outliers']
db_data_1200.columns = ['Number of Clusters', 'Number of Samples per Clusters', 'Number of Outliers']
dbscan_data = [db_data_300, db_data_600, db_data_900, db_data_1200]

kmeans_data_300 = load_from_csv("/Users/hugo/Desktop/PyCRE/dcm/csv/", "dcmk_cluster_statistics_900.csv")
kmeans_data_600 = load_from_csv("/Users/hugo/Desktop/PyCRE/dcm/csv/", "dcmk_cluster_statistics_900.csv")
kmeans_data_900 = load_from_csv("/Users/hugo/Desktop/PyCRE/dcm/csv/", "dcmk_cluster_statistics_900.csv")
kmeans_data_1200 = load_from_csv("/Users/hugo/Desktop/PyCRE/dcm/csv/", "dcmk_cluster_statistics_900.csv")
kmeans_data = [kmeans_data_300, kmeans_data_600, kmeans_data_900, kmeans_data_1200]

other_data = [db_data_300, db_data_600, db_data_900, db_data_1200]

data = {'DBSCAN': dbscan_data, 'KMeans': kmeans_data, 'Other': other_data}

get_barchart(data, path)
