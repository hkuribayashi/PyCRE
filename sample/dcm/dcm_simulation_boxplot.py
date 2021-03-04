from utils.charts import get_boxplot
from utils.misc import load_from_csv

path = "/Users/hugo/Desktop/PyCRE/dcm/images/"
filename = "boxplot.eps"

data_local = load_from_csv("/Users/hugo/Desktop/PyCRE/dcm/csv/", "dcm_cluster_statistics_300-local.csv")
data_servidor = load_from_csv("/Users/hugo/Desktop/PyCRE/dcm/csv/", "dcm_cluster_statistics_300-servidor.csv")

data_local.columns = ['Number of Clusters', 'Number of Samples per Clusters', 'Number of Outliers']
data_servidor.columns = ['Number of Clusters', 'Number of Samples per Clusters', 'Number of Outliers']

get_boxplot(data_local, data_servidor, path, filename)