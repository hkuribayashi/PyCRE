import pandas as pd
import numpy as np

# Transformação da Data e Nova Geração do CSV
# df = pd.read_csv('/Users/hugo/Downloads/dataset_tsmc2014/dataset_TSMC2014_NYC.txt', header=None, encoding = "ISO-8859-1", sep ='\t')
# df.columns = ['User_ID', 'Venue_ID', 'Venue_category_ID', 'Venue_category_name', 'Latitude', 'Longitude', 'Timezone', 'UTC']
# df['UTC'] = pd.to_datetime(df['UTC'])
# df.to_csv('/Users/hugo/Downloads/dataset_NYC.txt', index=True, sep ='\t')
from si.pso.IncreaseIWPSO import PSO
from utils.charts import get_visual_cluster

df = pd.read_csv('/Users/hugo/Downloads/dataset_NYC.txt', sep ='\t')
# print(df.columns)

# print(df.head)

start_date = '2012-04-04 00:00'
end_date = '2012-04-04 23:59'

mask = (df['UTC'] >= start_date) & (df['UTC'] < end_date)
df_1 = df.loc[mask]

data = []
for ind in df_1.index:
     data.append([df_1['Longitude'][ind], df_1['Latitude'][ind]])

print(data)
X1 = np.array(data)
X1 = X1 * 1000

p = PSO(X1, 50, 100)
p.search()
print(p.g_best.best_epsilon)
print(p.g_best.best_min_samples)
print(p.g_best.evaluation)
print(p.g_best.total_ues.labels_)

get_visual_cluster(p.g_best.total_ues, X1)

