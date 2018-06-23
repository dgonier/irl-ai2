"""
use associative learning in general to map out different state proximities?

determine reward function for users based on browser history frequency for a type of article

"""

import pandas as pd

msnbc = pd.read_table('msnbc990928.seq')
msnbc.columns=['seq']
msnbc['seq'] = msnbc['seq'].apply(lambda x: x.split(' '))

def count(i, seq_list):
    count = 0
    for x in seq_list:
        if str(x) == str(i):
            count+=1
    return count


for i in range(1,18):
    msnbc[i] = msnbc['seq'].apply(lambda x: count(i, x))

#determine transition probability? -- how associated are subjects?

universal_trans_dict = {}

name_conversions = {'1': 'frontpage',
'2': 'news',
'3': 'tech',
'4': 'local',
'5': 'opinion',
'6': 'on-air',
'7': 'misc',
'8': 'weather',
'9': 'msn-news',
'10': 'health',
'11': 'living',
'12': 'business',
'13': 'msn-sports',
'14': 'sports',
'15': 'summary',
'16': 'bbs',
'17': 'travel',}



def transition_probability(df):
    trans_dict = {}
    for x in range(1,17):
        for y in range(1,17):
            if x == y:
                continue
            elif (df[x]>0) and (df[y]> 0):
                trans_dict[str(x) + str(y)] = (df[x] + df[y])/df.sum()
                universal_trans_dict[name_conversions[str(x)] + "-" + name_conversions[str(y)]] = (df[x] + df[y])/df.sum()
    return trans_dict



msnbc['trans_dict'] = msnbc[list(range(1,18))].apply(lambda x: transition_probability(x), axis=1)

total = 0
for key, value in universal_trans_dict.items():
    total += value

universal_combinations_prob = {}
for key, value in universal_trans_dict.items():
    universal_combinations_prob[key] = value/total

uc_df = pd.Series(universal_combinations_prob)

uc_df = pd.DataFrame(uc_df)
uc_df = uc_df.reset_index()
uc_df.columns=['mappings', 'probabilities']
uc_df['from'] = uc_df['mappings'].apply(lambda x: x.split('-')[0])
uc_df['to'] = uc_df['mappings'].apply(lambda x: x.split('-')[1])
uc_df['prob_color'] = uc_df['probabilities'].apply(lambda x: round(x*100,1))
import networkx as nx
import matplotlib.pyplot as plt
G=nx.from_pandas_edgelist(uc_df, 'from', 'to', create_using=nx.Graph() )
nx.draw(G, with_labels=True, node_color='skyblue', node_size=1500, edge_color='red', width=uc_df['prob_color'])
plt.savefig('msnbc_network.png')
plt.show()

"""
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
 
# Build a dataframe with your connections
df = pd.DataFrame({ 'from':['A', 'B', 'C','A'], 'to':['D', 'A', 'E','C'], 'value':[1, 10, 5, 5]})
df
 
# Build your graph
G=nx.from_pandas_dataframe(df, 'from', 'to', create_using=nx.Graph() )
 
# Custom the nodes:
nx.draw(G, with_labels=True, node_color='skyblue', node_size=1500, edge_color=df['value'], width=10.0, edge_cmap=plt.cm.Blues)
https://python-graph-gallery.com/325-map-colour-to-the-edges-of-a-network/


"""