import pandas as pd
import data_query as dq
from scipy import stats
import matplotlib.pyplot as plt
from xml.etree import ElementTree as ET
from xml.dom import minidom

# pylint: disable=C0301

def wb_impact_analysis(league):
    impact_data = dq.retrieve_data_impact_sample(
        league, 'home_team_goal, away_team_goal, shoton, shotoff, cross, corner')
    impact_data = impact_data.dropna(axis=0, how='any')
    
    impact_data['Total Goals'] = impact_data['home_team_goal'] + impact_data['away_team_goal']
    impact_data['Shoton Count'] = [len(ET.fromstring(item)) for item in impact_data['shoton']]
    impact_data['Shotoff Count'] = [len(ET.fromstring(item)) for item in impact_data['shotoff']]
    impact_data['Cross Count'] = [len(ET.fromstring(item)) for item in impact_data['cross']]
    impact_data['Corner Count'] = [len(ET.fromstring(item)) for item in impact_data['corner']]
    impact_data['Total Shots'] = impact_data['Shoton Count'] + impact_data['Shotoff Count']

    comp_sample = dq.retrieve_data_outside_impact(
        league, 'home_team_goal, away_team_goal, shoton, shotoff, cross, corner')
    comp_sample = comp_sample.dropna(axis=0, how='any')

    comp_sample['Total Goals'] = comp_sample['home_team_goal'] + comp_sample['away_team_goal']
    comp_sample['Shoton Count'] = [len(ET.fromstring(item)) for item in comp_sample['shoton']]
    comp_sample['Shotoff Count'] = [len(ET.fromstring(item)) for item in comp_sample['shotoff']]
    comp_sample['Cross Count'] = [len(ET.fromstring(item)) for item in comp_sample['cross']]
    comp_sample['Corner Count'] = [len(ET.fromstring(item)) for item in comp_sample['corner']]
    comp_sample['Total Shots'] = comp_sample['Shoton Count'] + comp_sample['Shotoff Count']
    
    
    #print(comp_sample)

    goal_comps = stats.ttest_ind(comp_sample['Total Goals'], impact_data['Total Goals'],
                                equal_var = False, nan_policy = 'omit')
    goal_comps = ('t-stat ' + str(round(goal_comps[0],4)),'p-val ' + str(round(goal_comps[1],4)))
    shot_comps = stats.ttest_ind(comp_sample['Total Shots'], impact_data['Total Shots'], 
                                equal_var = False, nan_policy = 'omit')
    shot_comps = ('t-stat ' + str(round(shot_comps[0],4)),'p-val ' + str(round(shot_comps[1],4)))
    cross_comps = stats.ttest_ind(comp_sample['Cross Count'], impact_data['Cross Count'], 
                                equal_var = False, nan_policy = 'omit')
    cross_comps = ('t-stat ' + str(round(cross_comps[0],4)),'p-val ' + str(round(cross_comps[1],4)))
    corner_comps = stats.ttest_ind(comp_sample['Corner Count'], impact_data['Corner Count'], 
                                equal_var = False, nan_policy = 'omit')
    corner_comps = ('t-stat ' + str(round(corner_comps[0],4)),'p-val ' + str(round(corner_comps[1],4)))

    
    return(goal_comps,shot_comps,cross_comps,corner_comps)

def T_test_leagues():
    league_list = ['England Premier League',
                    'France Ligue 1',
                    'Germany 1. Bundesliga',
                    'Italy Serie A',
                    'Scotland Premier League',
                    'Spain LIGA BBVA']
    test_set = ['Goals: ', 'Shots: ', 'Crosses: ','Corners: ']
    impact_results = [wb_impact_analysis(league) for league in league_list]
    labeled_results = [list(zip(test_set,league_result)) for league_result in impact_results]
    res_pairs = list(zip(league_list,labeled_results))
    for pair in res_pairs:
        print(pair[0])
        for item in pair[1]:
            print(item[0]+item[1][0]+' '+item[1][1])

def build_seasonal_set(league):
    league_data_set = dq.retrieve_all_match_data(league,'home_team_goal, away_team_goal, shoton, shotoff, cross, corner')
    league_data_set['date'] = pd.to_datetime(league_data_set['date'])
    league_data_set = league_data_set.set_index('date')
    league_data_set['Total Goals'] = league_data_set['away_team_goal'] + league_data_set['home_team_goal']
    data_monthly = league_data_set.resample('1m').mean()
    #data_monthly.plot(data_monthly.index.values, kind = 'scatter', y='Total Goals')
    #monthly_change = data_monthly.diff(1)
    #print(monthly_change)
    plt.plot(data_monthly.index.values, data_monthly['Total Goals'],'g', lw=3, alpha=0.7)
    plt.show()
    return data_monthly

if __name__ == "__main__":
    #print(wb_impact_analysis('England Premier League'))
    #League sets for testing
    T_test_leagues()
    #print(build_seasonal_set('Germany 1. Bundesliga'))


