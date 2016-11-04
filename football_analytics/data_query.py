
import sqlite3
import pandas as pd

def retrieve_data_impact_sample(league, fields_to_return):
    """Retrieve the month sample for comparison to non WB periods"""
    league_dict = {'England Premier League':1729,'France Ligue 1':4769,'Germany 1. Bundesliga':7809,
                'Italy Serie A':10257,'Portugal Liga ZON Sagres':17647,'Scotland Premier League':19694,
                    'Spain LIGA BBVA':21518}
    #first date in league_wb is the WB start date for Dec,
    #second date is the wb end date For Jan
    #Since the actual dates vary year to year and are league specific,
    #the data for the date cutoffs is a rough estimate
    league_wb = {'England Premier League':(None,None),'France Ligue 1':('24','10'),'Germany 1. Bundesliga':('23','18'),
                'Italy Serie A':('23','05'),'Portugal Liga ZON Sagres':('18','05'),'Scotland Premier League':('31','17'),
                    'Spain LIGA BBVA':('23','05')}
    league_id = league_dict[league]
    dec_date = league_wb[league][0]
    jan_date = league_wb[league][1]
    conn = sqlite3.connect('/Users/baronabramowitz/Downloads/database.sqlite')
    if league == 'England Premier League':
        df = pd.read_sql_query("""SELECT date, {fields_to_return} FROM Match 
                        WHERE league_id = 1729 
                        AND (strftime('%m', date) = '12' AND strftime('%d', date) > '20')
                        OR (strftime('%m', date) = '01' AND strftime('%d', date) < '15' );"""
                        .format(fields_to_return = fields_to_return),conn)
    else:
        # Retrieve data for sepcific league for month following following winter break
        df = pd.read_sql_query("""SELECT date, {fields_to_return} FROM Match 
                        WHERE league_id = {league_id_qy} 
                        AND (strftime('%m', date) = '01' AND strftime('%d', date) > {jan_date})
                        OR (strftime('%m', date) = '02' AND strftime('%d', date) < {feb_date} );""".format(
                            fields_to_return = fields_to_return, league_id_qy = league_id,
                            jan_date = jan_date, feb_date = jan_date)
                        ,conn)
    conn.close()
    return df

def retrieve_data_outside_impact(league, fields_to_return):
    league_dict = {'England Premier League':1729,'France Ligue 1':4769,'Germany 1. Bundesliga':7809,
                'Italy Serie A':10257,'Portugal Liga ZON Sagres':17647,'Scotland Premier League':19694,
                    'Spain LIGA BBVA':21518}
    #first date in league_wb is the WB start date for Dec,
    #second date is the wb end date For Jan
    #Since the actual dates vary year to year and are league specific,
    #the data for the date cutoffs is a rough estimate
    league_wb = {'England Premier League':(None,None),'France Ligue 1':('24','10'),'Germany 1. Bundesliga':('23','18'),
                'Italy Serie A':('23','05'),'Portugal Liga ZON Sagres':('18','05'),'Scotland Premier League':('31','17'),
                    'Spain LIGA BBVA':('23','05')}
    league_id = league_dict[league]
    dec_date = league_wb[league][0]
    jan_date = league_wb[league][1]
    conn = sqlite3.connect('/Users/baronabramowitz/Downloads/database.sqlite')
    if league == 'England Premier League':
        df = pd.read_sql_query("""SELECT date, {fields_to_return} FROM Match 
                        WHERE league_id = 1729 
                        AND NOT (strftime('%m', date) = '12' AND strftime('%d', date) > '20')
                        OR NOT (strftime('%m', date) = '01' AND strftime('%d', date) < '15' );"""
                        .format(fields_to_return = fields_to_return),conn)
    else:
        # Retrieve data for sepcific league for month following following winter break
        df = pd.read_sql_query("""SELECT date, {fields_to_return} FROM Match 
                        WHERE league_id = {league_id_qy} 
                        AND NOT (strftime('%m', date) = '01' AND strftime('%d', date) > {jan_date})
                        OR NOT (strftime('%m', date) = '02' AND strftime('%d', date) < {feb_date} );""".format(
                            fields_to_return = fields_to_return, league_id_qy = league_id,
                            jan_date = jan_date, feb_date = jan_date)
                        ,conn)
    conn.close()
    return df

def retrieve_all_match_data(league, fields_to_return):
    league_dict = {'England Premier League':1729,'France Ligue 1':4769,'Germany 1. Bundesliga':7809,
                'Italy Serie A':10257,'Portugal Liga ZON Sagres':17647,'Scotland Premier League':19694,
                    'Spain LIGA BBVA':21518}
    league_id = league_dict[league]
    conn = sqlite3.connect('/Users/baronabramowitz/Downloads/database.sqlite')
    df = pd.read_sql_query("""SELECT date, {fields_to_return} FROM Match 
                        WHERE league_id = {league_id_qy};""".format(
                        fields_to_return = fields_to_return, league_id_qy = league_id), conn)
    conn.close()
    return df

if __name__ == "__main__":
    #print(retrieve_data_outside_impact('Italy Serie A','home_team_goal, away_team_goal'))
    #print(retrieve_data_impact_sample('Italy Serie A','home_team_goal, away_team_goal'))
    print(retrieve_all_match_data('Italy Serie A','home_team_goal, away_team_goal'))