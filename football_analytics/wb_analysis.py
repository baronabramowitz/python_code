import pandas as pd
import data_query as dq
from scipy import stats
import xmltodict
import matplotlib.pyplot as plt

def wb_impact_analysis(league):
    impact_data = dq.retrieve_data_impact_sample(league, 'home_team_goal, away_team_goal, shoton, shotoff, cross, corner')
    impact_data['Total Goals'] = impact_data['home_team_goal'] + impact_data['away_team_goal']
    #impact_data['shoton_count'] = [len(xmltodict.parse(item)) if item != None else item for item in impact_data['shoton']]
    #impact_data['shotoff_count'] = [len(xmltodict.parse(item)) if item != None else item  for item in impact_data['shotoff']]
    #impact_data['Total Shots'] = impact_data['shoton_count'] + impact_data['shotoff_count']
    comp_sample = dq.retrieve_data_outside_impact(league, 'home_team_goal, away_team_goal, shoton, shotoff, cross, corner')
    comp_sample['Total Goals'] = comp_sample['home_team_goal'] + comp_sample['away_team_goal']
    #comp_sample['shoton_count'] = [len(xmltodict.parse(item)) if item != None else item for item in comp_sample['shoton']]
    #comp_sample['shotoff_count'] = [len(xmltodict.parse(item)) if item != None else item  for item in comp_sample['shotoff']]
    #comp_sample['Total Shots'] = comp_sample['shoton_count'] + comp_sample['shotoff_count']
    #print(comp_sample)
    goal_comps = stats.ttest_ind(comp_sample['Total Goals'], impact_data['Total Goals'], equal_var = False, nan_policy = 'omit')
    #shot_comps = stats.ttest_ind(comp_sample['Total Shots'], impact_data['Total Shots'], equal_var = False, nan_policy = 'omit')
    return(goal_comps)#,shot_comps)

def T_test_leagues():
    league_list = ['England Premier League','France Ligue 1','Germany 1. Bundesliga','Italy Serie A',
                    'Portugal Liga ZON Sagres','Scotland Premier League','Spain LIGA BBVA']
    impact_results = [wb_impact_analysis(league) for league in league_list]
    res_pairs = list(zip(league_list,impact_results))
    for pair in res_pairs:
        print(pair)

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
    #League sets for testing
    #T_test_leagues()
    print(build_seasonal_set('Germany 1. Bundesliga'))