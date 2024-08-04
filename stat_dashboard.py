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
plt.rcParams["font.family"] = "Sans Serif"
df = pd.DataFrame(data_list)
Series_sum = pd.Series(total_sum)
total_packets = Series_sum.sum()
Series_sum_ratio=[0]*24

label = []

# Percentile the number of MCS packets that was transmitted.
for i in range(24):
    Series_sum_ratio[i] = int((Series_sum[i]/total_packets) * 100)

# Building plots
plt.figure(figsize=(14, 6))
#############################
#    Graph #1 Bar Graph     #
#############################
plt.subplot(2,3,1)
plt.bar(df.index, df[0], label='MCS0 RX')
plt.title(f'The num of Packets {param_type}', fontsize=10)
plt.legend(loc='upper left', bbox_to_anchor=(1,1), ncol=2, fontsize=8)

for i in range(23):
    if i % 2 == 0:
        label = f'MCS{int(i/2)} TX'
    else:
        label = f'MCS{int((i+1)/2)} RX'

    plt.bar(df.index, df[i+1], bottom=df[i], label=label)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1),ncol=2, fontsize=8)
plt.xlabel('Time')
plt.ylabel('Count of Packets')

#############################
#    Graph #2 Histgram      #
#############################
plt.subplot(2,3,4)
plt.subplots_adjust(hspace=0.5)
plt.bar(Series_sum.index, Series_sum)
plt.xlabel(f'{param_type} num (TX/RX)')
ticks = [str(i) for i in range(24)]
mcs_labels=['0','1','2','3','4','5','6','7','8','9','10','11']
plt.xticks([0,2,4,6,8,10,12,14,16,18,20,22], labels=mcs_labels, fontsize=10)
plt.ylabel('num of packets')
plt.title(f'num of {param_type} packets', fontsize=10)

#############################
#    Graph #3 Pie Graph     #
#############################
plt.subplot(2,3,5)
pie_labels=['RX 0','TX 0', 'RX 1', 'TX 1', 'RX 2', 'TX 2', 'RX 3', 'TX 3', 'RX 4', 'TX 4', 'RX 5', 'TX 5', 'RX 6', 'TX 6', 'RX 7', 'TX 7', 'RX 8', 'TX 8', 'RX 9', 'TX 9', 'RX 10', 'TX 10', 'RX 11', 'TX 11']
plt.pie(Series_sum_ratio, radius=1.0, labels=pie_labels, startangle=90, autopct='%1.1f%%')
plt.title('Ratio of each MCS %', fontsize=10)

plt.show()

