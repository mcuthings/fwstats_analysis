import pandas as pd
import re
import matplotlib.pyplot as plt
import streamlit as st
import pathlib


# logfile = 'fwstats_test.log'
file_name = 'fwstats_test.log'

pattern_ht = r'([A-Z]+)\(TxRx\), ([A-Z]{2}), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+),' + \
             r' (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+),' + \
             r' (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+),'

pattern_he = r'([A-Z]+)\(TxRx\), ([A-Z]{2}), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+),' + \
             r' (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+),'
pattern_vht = r'([A-Z]+)\(TxRx\), ([A-Z]{3}), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+),' + \
              r' (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+),'

pattern_nss = r'NSS\(TxRx\), (\d+),(\d+), (\d+),(\d+),'
pattern_bw = r'BW\(TxRx\), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+),'
pattern_preamble = r'PREAMBLE\(TxRx\), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+),(\d+), (\d+), (\d+),'
pattern_rts = r'RTS\(Tx\), (\d+),'
pattern_ldpc = r'LDPC\(Tx\), (\d+),'
pattern_rssi_ack = r'RSSI_ACK\(Tx\), (\d+),'
pattern_txbf = r'LDPC_TXBF\(Rx\), (\d+),(\d+),'
pattern_nsts = r'NSTS\(Rx\), (\d+),'
pattern_rssi = r'RSSI\(Rx\), ([+-]?\d+),([+-]?\d+),'
pattern_rssi_ant0 = r'RSSI_ANT0\(Rx\), ([+-]?\d+),([+-]?\d+),([+-]?\d+),([+-]?\d+),'
pattern_rssi_ant1 = r'RSSI_ANT1\(Rx\), ([+-]?\d+),([+-]?\d+),([+-]?\d+),([+-]?\d+),'

NSS_NUM = 4
BW_NUM = 6
PREAMBLE_NUM = 10
RTS_NUM = 1
LDPC_NUM = 1
RSSI_ACK_NUM = 1
TXBF_NUM = 2
NSTS_NUM = 1
RSSI_NUM = 2
RSSI_ANT0_NUM = 4
RSSI_ANT1_NUM = 4

param_type = ''
param_gen = ''


class NoLogfileError(Exception):
    pass

def find_logfile(file):
    file_path = pathlib.Path('./')
    file_path = file_path / file
    if not file_path.exists():
        raise NoLogfileError(file)
    return file_path


def counting_packets(_pattern, num, line):
    match = re.search(_pattern, line)
    if match:
        return [int(match.group(i+1)) for i in range(num)]
    return


def st_sidebar():
    with st.sidebar:
        global param_type
        global param_gen
        st.title('Select Packet and 80211 class')
        param_type = st.selectbox('Select', ['MCS','SGI','STBC'])
        param_gen = st.selectbox('Select Wi-Fi Class',['HT','VHT','HE'])


def stats():
    st.title('Packet statistics analysis')

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
    nss_list = []
    bw_list = []
    preamble_list = []
    rts_list = []
    ldpc_list = []
    rssi_ack_list = []
    txbf_list = []
    nsts_list =[]
    rssi_list = []
    rssi_ant0_list = []
    rssi_ant1_list = []

    # Open and search the pattern
    try:
        logfile = find_logfile(file_name)
    except NoLogfileError as err:
        st.write('Couldn\'t find {}'.format(file_name))
        return

    with open(file=logfile, mode='r', encoding='utf8') as f:
        for line in f:
            match = re.search(pattern, line)

            if match and match.group(1) == param_type and match.group(2) == param_gen:
                value_list = [int(match.group(i + 3)) for i in range(num)]
                data_list.append(value_list)
                total_sum = [x + y for x, y in zip(total_sum,value_list)]

            # nss
            nss_packets = counting_packets(pattern_nss, NSS_NUM, line)
            if nss_packets:
                nss_list.append(nss_packets)

            # bw
            bw_packets = counting_packets(pattern_bw, BW_NUM, line)
            if bw_packets:
                bw_list.append(bw_packets)

            # PREAMBLE
            preamble_packets = counting_packets(pattern_preamble, PREAMBLE_NUM, line)
            if preamble_packets:
                preamble_list.append(preamble_packets)

            # rts
            rts_packets = counting_packets(pattern_rts, RTS_NUM, line)
            if rts_packets:
                rts_list.append(rts_packets)

            # RSSI ACK
            rssi_ack_packets = counting_packets(pattern_rssi_ack, RSSI_ACK_NUM, line)
            if rssi_ack_packets:
                rssi_ack_list.append(rssi_ack_packets)

            # LDPC
            ldpc_packets = counting_packets(pattern_ldpc, LDPC_NUM, line)
            if ldpc_packets:
                ldpc_list.append(ldpc_packets)

            # TXBF
            txbf_packets = counting_packets(pattern_txbf, TXBF_NUM, line)
            if txbf_packets:
                txbf_list.append(txbf_packets)

            # NSTS
            nsts_packets = counting_packets(pattern_nsts, NSTS_NUM, line)
            if nsts_packets:
                nsts_list.append(nsts_packets)

            # RSSI
            rssi_packets = counting_packets(pattern_rssi, RSSI_NUM, line)
            if rssi_packets:
                rssi_list.append(rssi_packets)

            # RSSI_ANT0
            rssi_ant0_packets = counting_packets(pattern_rssi_ant0, RSSI_ANT0_NUM, line)
            if rssi_ant0_packets:
                rssi_ant0_list.append(rssi_ant0_packets)

            # RSSI_ANT1
            rssi_ant1_packets = counting_packets(pattern_rssi_ant1, RSSI_ANT1_NUM, line)
            # st.write(rssi_ant1_packets)
            if rssi_ant1_packets:
                rssi_ant1_list.append(rssi_ant1_packets)

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
    x_labels = [i for i in range(int(num/2))]
    x_ticks =[i for i in range(num) if i % 2 == 0]
    plt.xticks(x_ticks, labels=x_labels, fontsize=10)

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

    ##########################################################################
    #    Graph NSS/BW/NSTS/RTS/TXBF/LDPC/RSSI_ACK/RSSI/RSSI_ANT0/RSSI_ANT1   #
    ##########################################################################
    fig2 = plt.figure(figsize=(14, 6))
    # RSSI
    plt.subplot(4, 3, 1)
    plt.subplots_adjust(hspace=0.5, bottom=-0.7)
    plt.plot(rssi_list, label=['path1','path2'])
    plt.title(f'RSSI', fontsize=12)
    plt.xlabel('Time')
    plt.ylabel('Rx signal [dBm]')
    plt.ylim(-80, -20)
    plt.legend()

    # RSSI ANT0
    plt.subplot(4, 3, 2)
    plt.plot(rssi_ant0_list, label=['path1','path2', 'path3','path4'])
    plt.title(f'RSSI ANT0', fontsize=12)
    plt.xlabel('Time')
    plt.ylabel('Rx signal [dBm]')
    plt.ylim(-20, -80)
    plt.legend()

    # RSSI ANT1
    plt.subplot(4, 3, 3)
    plt.plot(rssi_ant1_list, label=['path1','path2', 'path3','path4'])
    plt.title(f'RSSI ANT1', fontsize=12)
    plt.xlabel('Time')
    plt.ylabel('Rx signal [dBm]')
    plt.gca().invert_yaxis()
    plt.ylim(-20, -80)
    plt.legend()

    # NSS
    plt.subplot(4, 3, 4)
    plt.plot(nss_list, label=['Stream 1 TX', 'Stream 1 RX', 'Stream 2 TX', 'Stream 2 RX',])
    plt.title(f'Num of Spacial Stream', fontsize=12)
    plt.xlabel('Time')
    plt.ylabel('Number of Packets')
    plt.legend()

    # BW
    plt.subplot(4, 3, 5)
    plt.plot(bw_list, label=['20MHz Tx','20MHz Rx','40MHz Tx','40MHz Rx','80MHz Tx','80MHz Rx'])
    plt.title(f'Packet per BW', fontsize=12)
    plt.xlabel('Time')
    plt.ylabel('Number of Packets')
    plt.legend()

    # Preamble
    plt.subplot(4, 3, 6)
    plt.plot(preamble_list)
    plt.title(f'Packets of Preamble', fontsize=12)
    plt.xlabel('Time')
    plt.ylabel('Number of Packets')

    # RTS
    plt.subplot(4, 3, 7)
    plt.plot(rts_list)
    plt.title(f'RTS', fontsize=12)
    plt.xlabel('Time')
    plt.ylabel('Number of Packets')

    # LDPC
    plt.subplot(4, 3, 8)
    plt.plot(ldpc_list)
    plt.title(f'LDPC', fontsize=12)
    plt.xlabel('Time')
    plt.ylabel('Number of Packets')

    # RSSI ACK
    plt.subplot(4, 3, 9)
    plt.plot(rssi_ack_list)
    plt.title(f'Packets of RSSI ACK', fontsize=12)
    plt.xlabel('Time')
    plt.ylabel('Number of Packets')

    # TXBF
    plt.subplot(4, 3, 10)
    plt.plot(txbf_list)
    plt.title(f'Packets of TXBF', fontsize=12)
    plt.xlabel('Time')
    plt.ylabel('Number of Packets')

    # NSTS
    plt.subplot(4, 3, 11)
    plt.plot(nsts_list)
    plt.title(f'Packets of NSTS', fontsize=12)
    plt.xlabel('Time')
    plt.ylabel('Number of Packets')

    st.pyplot(fig2)


if __name__ == '__main__':
    st_sidebar()
    stats()
