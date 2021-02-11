# Libraries
import matplotlib.pyplot as plt
import pandas as pd
from math import pi

# Set data
df = pd.DataFrame({
'group': ['A','B','C','D'],
'U': [100*(4/23), 99, 30, 4],
'NU': [100*(6/23), 99, 9, 34],
'E': [100*(9/23), 99, 23, 24],
'P': [100*(3/23), 99, 33, 14],
'PQ': [100*(16/23), 99, 32, 14],
'eMBB': [100*(20/23), 99, 32, 14],
'URLLC': [100*(12/23), 99, 32, 14],
'M': [100*(8/23), 99, 32, 14]
})



# ------- PART 1: Create background

# number of variable
categories=list(df)[1:]
N = len(categories)

# What will be the angle of each axis in the plot? (we divide the plot / number of variable)
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]

# Initialise the spider plot
ax = plt.subplot(111, polar=True)

# If you want the first axis to be on top:
ax.set_theta_offset(pi / 2)
ax.set_theta_direction(-1)

# Draw one axe per variable + add labels labels yet
plt.xticks(angles[:-1], categories)

# Draw ylabels
ax.set_rlabel_position(0)
plt.yticks([10,30,50,70,90], ["10","30","50","70","90"], color="grey", size=7)
plt.ylim(0,100)


# ------- PART 2: Add plots

# Plot each individual = each line of the data
# I don't do a loop, because plotting more than 3 groups makes the chart unreadable

# Ind1
values=df.loc[0].drop('group').values.flatten().tolist()
values += values[:1]
ax.plot(angles, values, linewidth=1, linestyle='solid', label="Média Trabalhos Correlatos")
ax.fill(angles, values, 'b', alpha=0.1)

# Ind2
values=df.loc[1].drop('group').values.flatten().tolist()
values += values[:1]
ax.plot(angles, values, linewidth=1, linestyle='solid', label="Proposta de Framework")
ax.fill(angles, values, 'r', alpha=0.1)

# Add legend
plt.legend(loc='lower center', bbox_to_anchor=(0.1, 0.1))
