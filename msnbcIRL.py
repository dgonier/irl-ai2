import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import irl.linear_irl as linear_irl
import os

#msnbc = pd.read_table('msnbc990928.seq')
#
#msnbc.columns=['seq']
#msnbc = msnbc.iloc[2:]
#msnbc['seq'] = msnbc['seq'].apply(lambda x: x.strip().split(' '))
#
#name_conversions = {1: 'frontpage',
#                    2: 'news',
#                    3: 'tech',
#                    4: 'local',
#                    5: 'opinion',
#                    6: 'on-air',
#                    7: 'misc',
#                    8: 'weather',
#                    9: 'msn-news',
#                    10: 'health',
#                    11: 'living',
#                    12: 'business',
#                    13: 'msn-sports',
#                    14: 'sports',
#                    15: 'summary',
#                    16: 'bbs',
#                    17: 'travel'}
#
## Group by final page visited
#msnbc['final'] = msnbc['seq'].apply(lambda x: x[-1])
#
#final_groups = msnbc.groupby('final')
#groups = [final_groups.get_group(g) for g in final_groups.groups]
#
#def get_empty_transitions():
#    df1 = pd.DataFrame({'current':list(name_conversions.keys()),'count':0})
#    df2 = pd.DataFrame({'next':list(name_conversions.keys()),'count':0})
#    return pd.merge(df1, df2, on='count')
#
#group_transitions = {}
#    
#
#for group in groups:
#    final = int(group.iloc[0]['final'])
#    print("Starting on group {}".format(final))
#    
#    transitions = get_empty_transitions()
#    
#    total = len(group)
#    iteration = 0
#    for seq in group['seq']:
#        iteration += 1
#        if iteration % 5000 == 0:
#            print('{0:.2f}% done. ({1} of {2})'.format(iteration * 100 / total, iteration, total))
#        l = len(seq)
#        for i in range(l):
#            if i < l - 1:
#                transitions['count'] += ((transitions['current'] == int(seq[i])) & 
#                           (transitions['next'] == int(seq[i + 1])))
#    
#    totals = transitions.groupby('current').sum()['count']
#    transitions['prob'] = 1/ 17
#    for index, row in transitions.iterrows():
#        current = row['current']
#        if totals[current] > 0:
#            row['prob'] = row['count'] / totals[current]
#            transitions.iloc[index] = row
#    
#    group_transitions[final] = transitions

#for k, v in group_transitions.items():
#    filename = 'transitions_{}.csv'.format(k)
#    df = pd.DataFrame(columns=list(name_conversions.keys()))
#    for c in range(1, 18):
#        nexts = v[v['current'] == c][['next', 'prob']].reset_index()
#        nexts = pd.DataFrame(nexts['prob'].tolist(), index=nexts['next'].tolist(), columns=['prob'])
#        df = df.append(nexts['prob'], ignore_index=True)
#    df.to_csv(filename, sep=',', header=False, index=False)
    
transition_probability = pd.DataFrame(np.diag(np.ones(17)), columns=list(range(17)), index=list(range(17)))

for i in range(1, 18):
    filename = 'transitions{}transitions_{}.csv'.format(os.sep, i)
    transitions = pd.read_csv(filename, header=None)
    for j in range(17):
        transitions[j][j] = 0
    policy = transitions.transpose().idxmax()
    policy_file_name = 'policies{}policy_{}.csv'.format(os.sep, i)
    policy.to_csv(policy_file_name)


for i in range (1, 18):
    policy = pd.read_csv('policies{}policy_{}.csv'.format(os.sep, i))
    ##TODO: The following IRL code needs to be fixed to work for the msnbc state space.
    
#    grid_size = 17
#    discount = 0.2
#    
#    r = linear_irl.irl(17, 17, np.array(transition_probability), policy, discount, 1, 5)
#    
#    plt.subplot(1, 2, 1)
#    plt.pcolor(ground_r.reshape((grid_size, grid_size)))
#    plt.colorbar()
#    plt.title("Groundtruth reward")
#    plt.subplot(1, 2, 2)
#    plt.pcolor(r.reshape((grid_size, grid_size)))
#    plt.colorbar()
#    plt.title("Recovered reward")
#    plt.show()


