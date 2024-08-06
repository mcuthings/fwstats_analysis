import pandas as pd
import re
import matplotlib.pyplot as plt
import streamlit as st


logfile = 'fwstats_test.log'

pattern_ht = r'([A-Z]+)\(TxRx\), ([A-Z]{2}), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+),' + \
             r' (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+),' + \
             r' (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+),'

pattern_he = r'([A-Z]+)\(TxRx\), ([A-Z]{2}), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+),' + \
             r' (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+),'
pattern_vht = r'([A-Z]+)\(TxRx\), ([A-Z]{3}), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+),' + \
              r' (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+),'

# Input and select an item
param_type = st.selectbox('Select', ['MCS','SGI','STBC'])
param_gen = st.selectbox('Select Wi-Fi',['HT','VHT','HE'])


def stats():

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

    data_list = []
    total_sum = [0]*num

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
    series_sum = pd.Series(total_sum)
    total_packets = series_sum.sum()
    series_sum_ratio = [0]*num

    # Percentile the number of MCS packets that was transmitted.
    if total_packets == 0:
        st.write('No packet')
        return
    else:
        for i in range(num):
            series_sum_ratio[i] = int((series_sum[i]/total_packets) * 100)

    # Building plots
    fig = plt.figure(figsize=(14, 6))
    #############################
    #    Graph #1 Bar Graph     #
    #############################
    plt.subplot(2,3,1)
    plt.bar(df.index, df[0], label='MCS0 TX')
    plt.title(f'The num of Packets {param_type}', fontsize=12)

    for i in range(num-1):
        if i % 2 == 0:
            label = f'MCS{int(i/2)} RX'
        else:
            label = f'MCS{int((i+1)/2)} TX'

        plt.bar(df.index, df[i+1], bottom=df[i], label=label)
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1.1),ncol=2, fontsize=8)
    plt.xlabel('Time')
    plt.ylabel('Count of Packets')

    #############################
    #    Graph #2 Histgram      #
    #############################
    plt.subplot(2,3,4)
    plt.subplots_adjust(hspace=0.5, bottom=-0.1)
    plt.bar(series_sum.index, series_sum)
    plt.xlabel(f'{param_type} num (TX/RX)')
    # ticks = [str(i) for i in range(24)]
    mcs_labels=['0','1','2','3','4','5','6','7','8','9','10','11']
    plt.xticks([0,2,4,6,8,10,12,14,16,18,20,22], labels=mcs_labels, fontsize=10)
    plt.ylabel('num of packets')
    plt.title(f'num of {param_type} packets', fontsize=12)

    #############################
    #    Graph #3 Pie Graph     #
    #############################
    plt.subplot(2,3,5)
    pie_labels = []
    for i in range(24):
        if i % 2 == 0:
            pie_labels.append(f'{param_type}{int(i/2)} TX')
        else:
            pie_labels.append(f'{param_type}{int(i/2)} RX')
    plt.pie(series_sum_ratio, radius=1.0, startangle=90, autopct='%1.1f%%')
    plt.title('Ratio of each MCS %', fontsize=12)
    plt.legend(pie_labels, loc='upper left', bbox_to_anchor=(1,1), ncol=2, fontsize=8)
    st.pyplot(fig)


if __name__ == '__main__':
    stats()
