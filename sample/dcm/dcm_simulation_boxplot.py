from utils.charts import get_barchart
from utils.misc import load_from_csv

path = "/Users/hugo/Desktop/PyCRE/dcm/images/"

data_300 = load_from_csv("/Users/hugo/Desktop/PyCRE/dcm/csv/", "dcm_cluster_statistics_300-backup.csv")
data_600 = load_from_csv("/Users/hugo/Desktop/PyCRE/dcm/csv/", "dcm_cluster_statistics_600-backup.csv")
data_900 = load_from_csv("/Users/hugo/Desktop/PyCRE/dcm/csv/", "dcm_cluster_statistics_900-backup.csv")
data_1200 = load_from_csv("/Users/hugo/Desktop/PyCRE/dcm/csv/", "dcm_cluster_statistics_1200-backup.csv")

data_300.columns = ['Number of Clusters', 'Number of Samples per Clusters', 'Number of Outliers']
data_600.columns = ['Number of Clusters', 'Number of Samples per Clusters', 'Number of Outliers']
data_900.columns = ['Number of Clusters', 'Number of Samples per Clusters', 'Number of Outliers']
data_1200.columns = ['Number of Clusters', 'Number of Samples per Clusters', 'Number of Outliers']

cluster_data = [data_300, data_600, data_900, data_1200]

get_barchart(cluster_data, path)
