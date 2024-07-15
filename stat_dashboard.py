import pandas as pd
import re
import matplotlib.pyplot as plt

logfile = 'fwstats_test.log'
# logfile = 'mlan_stat_all_xperia.log'

pattern_ht = r'([A-Z]+)\(TxRx\), ([A-Z]{2}), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+),' + \
             r' (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+),' + \
             r' (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+),'

pattern_he = r'([A-Z]+)\(TxRx\), ([A-Z]{2}), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+),' + \
             r' (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+),'
pattern_vht = r'([A-Z]+)\(TxRx\), ([A-Z]{3}), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+),' + \
              r' (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+),'

value_list = [0]*32
data_list = []
total_sum = [0]*32

# Input and select an item
param_type = input('Select MCS/SGI/STBC: ')
param_gen = input('Select HT/VHT/HE: ')

# Define the value to count MCS(Tx/Rx)
if param_gen == 'HT':
    num = 32
    pattern = pattern_ht
elif param_gen == 'VHT':
    num = 20
    pattern = pattern_vht
elif param_gen == 'HE':
    num = 24
    pattern = pattern_he
else:
    num = 24
    pattern = pattern_he

# Open and search the pattern
with open(file=logfile, mode='r', encoding='utf8') as f:
    for line in f:
        match = re.search(pattern, line)

        if match and match.group(1) == param_type and match.group(2) == param_gen:
            value_list = [int(match.group(i + 3)) for i in range(num)]
            data_list.append(value_list)
            total_sum = [x + y for x, y in zip(total_sum,value_list)]

# Prepare plotting, create a dataframe
plt.rcParams["font.family"] = "DejaVu Serif"
df = pd.DataFrame(data_list)
Series_sum = pd.Series(total_sum)
total_packets = Series_sum.sum()

# Percentile the number of MCS packets that was transmitted.
for i in range(24):
    Series_sum[i] = (Series_sum[i]/total_packets) * 100

#plt.figure()
#fig, ax = plt.subplot(121)

# Building plots

plt.figure(figsize=(10, 6))
#############################
#    Graph #1 Bar Graph     #
#############################
plt.subplot(2,2,1)
plt.bar(df.index, df[0])
for i in range(23):
    plt.bar(df.index, df[i+1], bottom=df[i])
#############################
#    Graph #2 Histgram      #
#############################
plt.subplot(2,2,2)
plt.bar(Series_sum.index, Series_sum)
#############################
#    Graph #3 Pie Graph     #
#############################
plt.subplot(2,2,3)
plt.pie(Series_sum, radius=1.2)

plt.show()

