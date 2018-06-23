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