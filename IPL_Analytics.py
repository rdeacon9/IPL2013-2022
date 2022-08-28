import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time
from sklearn.linear_model import LinearRegression
import textwrap

raw_data = pd.read_csv(r"C:\Users\Ryan\Documents\GitHub\IPL2013-2022\IPLPlayerAuctionData.csv")
standings = pd.ExcelFile(r"C:\Users\Ryan\Documents\GitHub\IPL2013-2022\table export.xlsx")

def clear_console():
    clear = ("\n" * 100)
    print(clear)
    print(clear)

def wrap_labels(ax, width, break_long_words=False):
    labels = []
    for label in ax.get_xticklabels():
        text = label.get_text()
        labels.append(textwrap.fill(text, width=width,
                      break_long_words=break_long_words))
    ax.set_xticklabels(labels, rotation=0)

#Fixing and moving the data around. Converting Indian Rupee to Euro
for index, row in raw_data.iterrows():
    raw_data.loc[index, 'EURO Value'] = int(row['Amount'] * 0.012)

raw_data['EURO Value'] = raw_data['EURO Value'].astype(str).apply(lambda x: x.replace('.0', ''))
raw_data['Year'] = raw_data['Year'].astype(str).apply(lambda x: x.replace('.0', ''))
raw_data['EURO Value'] = raw_data['EURO Value'].astype('int')
u_data = raw_data.sort_values(['Player','Year'],ascending=[True,False]).drop_duplicates('Player').reset_index(drop=True)
raw_data = raw_data.sort_values(['Player','Year'],ascending=[True,False]).reset_index(drop=True)
np_data_playername_sin = np.array(u_data['Player'])
np_data_playername_multi = np.array(raw_data['Player'])
np_data_role_all = np.array(raw_data['Role'])
np_data_role_latest = np.array(u_data['Role'])
np_data_EValue_sin = np.array(u_data['EURO Value'],dtype=float)
np_data_EValue_multi = np.array(raw_data['EURO Value'],dtype=float)
np_data_team_latest = np.array(u_data['Team'])
np_data_team_all = np.array(raw_data['Team'])
np_data_year_latest = np.array(u_data['Year'])
np_data_year_all = np.array(raw_data['Year'])
np_data_origin_latest = np.array(u_data['Player Origin'])
np_data_origin_all = np.array(raw_data['Player Origin'])

#Dictonary of lists needed for all options
dic_list = {"Overall_or_Latest": ["Overall", "Latest"],
            "start": ['1. Avg breakdown', '2. Sum breakdown', '3. Player Breakdown', '4. Next' , "5. Standings", "6. Stop"],
            "avg_list": ['1. Avg per role', '2. Avg per team', '3. Avg per year', '4. Avg per player origin'],
            "next_list": ['1. Comparing the 4 roles', "2. Comparing 2 teams spending", "3. Comparing player origin", "4. Model for 10 year data"],
            "player_option_list": ['1. Player movement', '2. Lowest cost vs highest cost', '3. Value per player '],
            "team_standings": ["1. Team specific", "2. Year specific"],
            "sum_list": ['1. Sum per role', '2. Sum per team', '3. Sum per year', '4. Sum per player origin'],
            }



#order values
def order_values(data,option_min_max):
    print('')
    if option_min_max == False: 
        order_by = input('Sort values by ascending, descending or option selected? Input A, D or O to sort ').lower()
        if order_by == 'a':
            new = data.sort_values(by='EURO Value',ascending=False)
            return new
        elif order_by == 'd':
            new = data.sort_values(by='EURO Value',ascending=True)
            return new
        elif order_by == 'o': 
            return data
        else:
            print('Invalid option')
            menu()
    else:
        min_or_max = input('Which option do you want to sort? Min or Max? ').lower()
        print('')
        if min_or_max == 'min':
            order_by = input('Sort values by ascending, descending? Input A or D to sort ').lower()
            if order_by == 'a':
                new = data.sort_values(by=('amin', 'EURO Value'),ascending=False)
                return new
            elif order_by == 'd':
                new = data.sort_values(by=('amin', 'EURO Value'),ascending=True)
                return new
            else:
                return data
        elif min_or_max == 'max':
            order_by = input('Sort values by ascending, descending? Input A or D to sort ').lower()
            if order_by == 'a':
                new = data.sort_values(by=('amax', 'EURO Value'),ascending=False)
                return new
            elif order_by == 'd':
                new = data.sort_values(by=('amax', 'EURO Value'),ascending=True)
                return new
            else:
                return data
        else:
            print('Invalid option')
            menu()      

#show option lists better
def display_list(unique_list,add_all):
    for i in unique_list:
        print(i)
    if add_all == True:
        print('All')
    print('')

#building graph 
def display_graph(values,option_selected,avg_or_sum,latest_or_overall):
    print('')
    user_input_new = input('Would you like to see this in graph format? Y/N ').lower()
    values = pd.DataFrame(values)
    if user_input_new == 'y':
        x_option = option_selected
        if x_option == 'Full_Name':
            ax = sns.barplot(y='Full_Name',x='EURO Value',data=values)
            x_option = 'Team'
            if avg_or_sum == 'a':
                if latest_or_overall:
                    ax.set_title(f'Overall average of each {x_option}')
                    ax.set_xlabel('Cost in EURO Value')
                    ax.xaxis.get_major_formatter().set_scientific(False)
                    ax.xaxis.get_major_formatter().set_useOffset(False)
                else: 
                    ax.set_title(f'Latest average of each {x_option}')
                    ax.set_xlabel('Cost in EURO Value')
                    ax.xaxis.get_major_formatter().set_scientific(False)
                    ax.xaxis.get_major_formatter().set_useOffset(False)
            else:
                if latest_or_overall: 
                    ax.set_title(f'Overall total of each {x_option}')
                    ax.set_xlabel('Cost in EURO Value in Millions')
                    ax.xaxis.get_major_formatter().set_scientific(False)
                    ax.xaxis.get_major_formatter().set_useOffset(False)
                else:
                    ax.set_title(f'Latest total of each {x_option}')
                    ax.set_xlabel('Cost in EURO Value in Millions') 
                    ax.xaxis.get_major_formatter().set_scientific(False)
                    ax.xaxis.get_major_formatter().set_useOffset(False)
        else:
            ax = sns.barplot(x=values.index,y='EURO Value',data=values)
            
            if x_option == 'Origin':
                ax.set_xlabel(x_option)
            else:
                ax.set_xlabel(f"{x_option}s")
            if avg_or_sum == 'a':
                if latest_or_overall:
                    ax.set_title(f'Overall average of each {x_option}')
                    ax.set_ylabel('Cost in EURO Value')
                    ax.bar_label(ax.containers[0])
                else: 
                    ax.set_title(f'Latest average of each {x_option}')
                    ax.set_ylabel('Cost in EURO Value')
                    ax.bar_label(ax.containers[0])
            else:
                if latest_or_overall: 
                    ax.set_title(f'Overall total of each {x_option}')
                    ax.set_ylabel('Cost in EURO Value in Millions')
                    ax.yaxis.get_major_formatter().set_scientific(False)
                    ax.yaxis.get_major_formatter().set_useOffset(False)
                else: 
                    ax.set_title(f'Latest total of each {x_option}')
                    ax.set_ylabel('Cost in EURO Value in Millions')
                    ax.yaxis.get_major_formatter().set_scientific(False)
                    ax.yaxis.get_major_formatter().set_useOffset(False)
        plt.show()
    else:
        return False

#fill missing values
def check_if_all_year(data):
    check_index = True
    checker = data
    start_index = 2013
    ix = 0
    fill_missing = []
    if len(checker) != 10:
        while check_index:
            if checker.index[-1] != '2022':
                temphold = pd.Series([]).astype(dtype=int)
                default_year_list = np.unique(np_data_year_all)
                default_values = [0,0,0,0,0,0,0,0,0,0]
                default_dic = {'0': default_values}
                default_df = pd.DataFrame(default_dic,index=default_year_list)
                temphold = pd.DataFrame([])
                for index, value in checker.iteritems():
                # copy over available values to default pandas Dataframe
                    default_df.at[index,'0'] = value
                default_df.sort_index(inplace=True)
                default_df.iloc[:,0] = default_df.iloc[:,0].astype(str).apply(lambda x: x.replace('.0', ''))
                default_df.iloc[:,0] = default_df.iloc[:,0].astype(int)
                return default_df
            else:
                #Fill the gaps with the existing Dataframe with 0
                if str(start_index) != checker.index[ix]:
                    fill_missing.append(start_index)
                    start_index += 1
                else:
                    start_index += 1
                    ix += 1        
            if start_index == 2023:
                check_index = False 
                                
    leng = len(fill_missing)
    if leng > 0:
        temphold = pd.Series([]).astype(dtype=int)
        for i in range(leng):
            build = pd.DataFrame([0],index=[str(fill_missing[i])])
            temphold = pd.concat([temphold, build])
        df_checker = pd.concat([checker, temphold])
        df_checker = pd.DataFrame(df_checker)
        df_checker.sort_index(inplace=True)
        df_checker.iloc[:,0] = df_checker.iloc[:,0].astype(str).apply(lambda x: x.replace('.0', ''))
        df_checker.iloc[:,0] = df_checker.iloc[:,0].astype(int)
        return df_checker
    else:
        return checker

#standings
def display_standings():
    year_list = np.unique(np_data_year_all)
    team_list = np.unique(np_data_team_all)
    print(' ')
    display_list(dic_list["team_standings"], False)
    user_input = input('Please select year specific or team specific: ').lower()
    if user_input == '1' or user_input == 'team':
        display_list(team_list,False)
        user_input = input('Please select a team: ').title()
        if user_input in team_list:
            df_name = pd.read_excel(standings, sheet_name='details_of_teams')
            team_hold = df_name.query(f"team_name == '{user_input}'")
            team_id = pd.DataFrame(team_hold['team_id'])
            team_id1 = int(team_id.loc[:,'team_id'])
            default_df = pd.DataFrame([])
            for y in range(2013,2023):
                temp = pd.read_excel(standings, sheet_name='standings_'+str(y))
                try:
                    temp_hold = temp.query("team_id == "+ str(team_id1))
                    team_pos = int(temp_hold.loc[:,'position'])
                    default_df.loc[y,'Position'] = int(team_pos)
                except:
                    team_pos = 'NaN'
                    default_df.loc[y,'Position'] = team_pos            
            print(default_df)
            print('')
            spending_vs_position_t(user_input.title(),default_df)
            menu()
        else:
            print('Team not in list')
            display_standings()

    elif user_input == '2' or user_input == 'year':
        display_list(year_list,False)
        user_input = input('Please select a year: ')
        if user_input in year_list: 
            df = pd.read_excel(standings, sheet_name='standings_'+user_input)
            df_name = pd.read_excel(standings, sheet_name='details_of_teams')
            new_df = df.merge(df_name,on='team_id', how='left')
            new_df1 = new_df[["position",'team_name','won','lost','points']]
            pos_data = new_df1.sort_values(by=['position'],ascending=True)
            pos_data = pos_data.reset_index(drop=True)
            pos_data.rename(columns = {'team_name':'Team','won':'Won','lost':'Lost','points':'Points', 'position':'Position'}, inplace=True)
            print(pos_data) 
            spending_vs_position_y(user_input,pos_data)
        else:
            print('Year not in list')
            display_standings()
    else:
        display_standings()

#displaying the final log positions and the total spent for a specific team
def spending_vs_position_t(user_input,pos_data):
    year_list = np.unique(np_data_year_all)
    if input('Display spending vs final log position? ').lower() == 'y':
        team = raw_data[raw_data['Team']==user_input][['EURO Value','Year']]
        team = team.groupby('Year')['EURO Value'].sum()
        team = check_if_all_year(team)
        team = pd.DataFrame(team)
        pos_data = pd.DataFrame(pos_data)
        print(pos_data)
        try: 
            pos_data['Position'] = pos_data['Position'].astype(int)
        except ValueError:
            pos_data['Position'] = pos_data['Position'].fillna(10)
            pos_data['Position'] = pos_data['Position'].astype(int)
        print(pos_data)
        try: 
            data_display = pd.DataFrame(pos_data.compare(team, keep_shape=True,keep_equal=True))
            data_display.rename(columns = {'Year': 'Year', 'self':'Position','other':'Spending'}, inplace = True)
        except ValueError:
            if pos_data.equals(team) == False:
                default_year_list = np.unique(np_data_year_all)
                data_display = pd.DataFrame(index=default_year_list)
            if 'Position' in pos_data.columns:
                data_display['Position'] = pos_data.iloc[:,0]
                print(data_display)
            else:
                data_display['Position'] = pos_data['Position']
            if '' in team.columns:
                data_display['Spending'] = team['']
            else:
                data_display['Spending'] = team.iloc[:,0]
        print(data_display)
        
        data_display['Spending'] = data_display['Spending'].astype(float)
        print(data_display)
        ax1 = sns.lineplot(x=data_display.index,y='Position',data=data_display,color='red',markers=True)
        ax1.set_ylabel('Final log position')
        ax1.legend(['Team Position'], loc="upper left") 
        ax1.set_ylim(10,1)      
        ax2 = ax1.twinx()
        sns.barplot(x=data_display.index,y='Spending',data=data_display,alpha=0.5,color='blue',ax=ax2)
        ax2.grid(visible=False)
        ax2.set_ylabel('Spent in millions')
        ax2.legend(['Team Spending'], loc="upper right")
        ax1.set_title(f"Spending vs Log Position for the Team: {user_input} ")
        plt.show()
    else:
        menu()

#Displaying the final log positions and the total spent for a specific year
def spending_vs_position_y(user_input,pos_data):
    print('')
    year_list = np.unique(np_data_year_all)
    if input('Display spending vs final log position? ').lower() == 'y':
        team = raw_data[raw_data['Year']==user_input][['EURO Value','Team']]
        team = team.groupby('Team')['EURO Value'].sum()
        team = pd.DataFrame(team)
        pos_data = pd.DataFrame(pos_data)
        data_display = team.merge(pos_data,on='Team')
        data_display = pd.DataFrame(data_display)
        data_display = data_display.sort_values(by=['Position'],ascending=True)
        print('')
        print(data_display)
        ax1 = sns.lineplot(x='Team',y='Position',data=data_display,color='red',marker=True)
        ax1.set_ylabel('Final log position')
        ax1.legend(['Team Position'], loc="upper left") 
        ax1.set_ylim(10,1)
        ax2 = ax1.twinx()
        sns.barplot(x='Team',y='EURO Value',data=data_display,alpha=0.5,color='blue',ax=ax2)
        ax2.grid(visible=False)
        ax2.set_ylabel('Spent in millions')
        wrap_labels(ax2,10)
        ax1.set_title(f"Spending vs Log Position for the year: {user_input} ")
        plt.show()
        print('')
    else:
        menu()

#main Options
def main_menu():
    display_list(dic_list['start'],False)
    user_input = input('Please select an option in the above list:  ' ).lower()

#go to Avg Breakdown list
    if user_input == 'avg breakdown' or user_input == '1':
        if Averages() == False:
            return False
        else:
            main_menu()

#go to Sum Breakdown list    
    elif user_input == 'sum breakdown' or user_input == '2':
        if Sum() == False:
            return False
        else:
            main_menu()

#go to Player Breakdown list    
    elif user_input == 'player breakdown' or user_input == '3':
        if other_player_info() == False:
            return False
        else:
            main_menu()

#go to Additional Option    
    elif user_input == 'next' or user_input == '4':
        if deeper_comparison() == False:
            return False
        else:
            main_menu()

#go to Standings   
    elif user_input == 'standings' or user_input == '5':
        display_standings()
        main_menu()   

#stop anaysis  
    elif user_input == 'stop' or user_input == '6':
        return False

    else:
        print('Invalid option selected ')
        menu()

def Averages():
#start of averages
    print('')
    display_list(dic_list["avg_list"],False)
    user_input = input('Please select an option in the above list: ').lower()
    
    if user_input == 'avg per role' or user_input == '1':
        user_input = input(dic_list['Overall_or_Latest'][0] + ' or ' + dic_list['Overall_or_Latest'][1] + '? ').lower()

#ROLE AVERAGE 
        if user_input == 'overall':
            role_option = np.unique(np_data_role_latest)
            display_list(role_option,True)
            user_input = input('Which role? ').title()
            if user_input not in np.unique(np_data_role_all):
                temphold = np.around(raw_data.groupby("Role")['EURO Value'].mean(),2)
                df_temphold = pd.DataFrame(temphold)
                print('Role not selected, here is the mean values for all Roles')
                print(order_values(df_temphold,False))
                
                display_graph(df_temphold,'Role','a',True)
                print(' ')
                menu()
            else:
                temphold = np.around(np.mean(np_data_EValue_multi[(user_input).title() == np_data_role_all]),2)
                print('The mean value for the role ' + user_input.title() + ' is: ' + str(temphold))
                print(' ')
                menu()
        else:
            role_option = np.unique(np_data_role_latest)
            display_list(role_option,True)
            user_input = input('Which role? ').title()
            if user_input not in np.unique(np_data_role_all):
                temphold = np.around(u_data.groupby("Role")['EURO Value'].mean(),2)
                df_temphold = pd.DataFrame(temphold)
                print('Role not selected, here is the mean values for all Roles')
                print(order_values(df_temphold,False))
                display_graph(df_temphold,'Role','a',False)
                print(' ')
                menu()
            else:
                temphold = np.around(np.mean(np_data_EValue_sin[(user_input).title() == np_data_role_latest]),2)
                print('The mean value for the role ' + user_input.title() + ' is: ' + str(temphold))
                print(' ')
                menu()
                             
#TEAM AVERAGE
    elif user_input == 'avg per team' or user_input == '2':
        user_input = input(dic_list['Overall_or_Latest'][0] + ' or ' + dic_list['Overall_or_Latest'][1]+ ' ? ').lower()
        if user_input == 'overall':
            team = np.unique(np_data_team_all)
            display_list(team,True)
            user_input = input('Which team? ').title()
            
            if user_input not in np.unique(np_data_team_all):
                temphold = np.around(raw_data.groupby("Team")['EURO Value'].mean(),2)
                hold = pd.DataFrame(temphold)
                df_temphold = hold.merge(df_short_name,how='left', left_on='Team',right_on='Full_Name')
                print('Team not selected, here is the mean values for all Teams')
                print(order_values(df_temphold,False))
                
                display_graph(df_temphold,'Full_Name','a',True)
                print(' ')
                menu()
            else:
                temphold = np.around(np.mean(np_data_EValue_multi[np_data_team_all == (user_input).title()]),2)
                print('The mean value for the team: ' + (user_input).title() + ' is ' + str(temphold))
                print(' ')
                menu()
        else:
            team = np.unique(np_data_team_all)
            display_list(team,True)
            user_input = input('Which team? ').title()
            
            if user_input not in np.unique(np_data_team_all):
                temphold = np.around(u_data.groupby("Team")['EURO Value'].mean(),2)
                hold = pd.DataFrame(temphold)
                df_temphold = hold.merge(df_short_name,how='left', left_on='Team',right_on='Full_Name')
                print('Team not selected, here is the mean values for all Teams')
                print(order_values(df_temphold,False))
                
                display_graph(df_temphold,'Full_Name','a',False)
                print(' ')
                menu()
            else:
                temphold = np.around(np.mean(np_data_EValue_sin[np_data_team_latest == (user_input).title()]),2)
                print('The mean value for the team: ' + (user_input).title() + ' is ' + str(temphold))
                print(' ')
                menu()

#YEAR AVERAGE
    elif user_input == 'avg per year' or user_input == '3':
        user_input = input(dic_list['Overall_or_Latest'][0] + ' or ' + dic_list['Overall_or_Latest'][1]+ '? ').lower()
        if user_input == 'overall':
            temphold = np.around(raw_data.groupby("Year")['EURO Value'].mean(),2)
            df_temphold = pd.DataFrame(temphold)
            print(order_values(df_temphold,False))
            
            display_graph(temphold,'Year','a',True)
            menu()
        else: 
            year_values = np.unique(np_data_year_all)
            display_list(year_values,False)
            user_input = input('Which Year? ').lower()
            if user_input in (year_values):
                temphold = np.around(np.mean(np_data_EValue_sin[np_data_year_latest == (user_input).title()]),2)
                print('The mean value for the latest year: ' + (user_input).title() + ' is ' + str(temphold))
                menu()
            else:
                print('Year data not available')
                menu()

#ORIGIN AVERAGE
    elif user_input == 'avg per player origin' or user_input == '4':
        user_input = input(dic_list['Overall_or_Latest'][0] + ' or ' + dic_list['Overall_or_Latest'][1] + ' ? ').lower()
        if user_input == 'overall':
            player_origin = np.unique(np_data_origin_all)
            display_list(player_origin,True)
            user_input = input('Which origin? ').title()
            if user_input not in player_origin:
                temphold = np.around(raw_data.groupby("Player Origin")['EURO Value'].mean(),2)
                df_temphold = pd.DataFrame(temphold)
                print(order_values(df_temphold,False))
                display_graph(df_temphold,'Origin','a',True)
                menu()
            else:
                temphold = np.around(np.mean(np_data_EValue_multi[np_data_origin_all == (user_input).title()]),2)
                print('The mean value for the player origin: ' + (user_input).title() + ' is ' + str(temphold))
                menu()
        else:
            player_origin = np.unique(np_data_origin_all)
            display_list(player_origin,True)
            user_input = input('Which origin? ').title()
            if user_input not in player_origin:
                temphold = np.around(u_data.groupby("Player Origin")['EURO Value'].mean(),2)
                df_temphold = pd.DataFrame(temphold)
                print(order_values(df_temphold,False))
                display_graph(df_temphold,'Origin','a',False)
                menu()
            else:
                temphold = np.around(np.mean(np_data_EValue_sin[np_data_origin_latest == (user_input).title()]),2)
                print('The mean value for the player origin: ' + (user_input).title() + ' is ' + str(temphold))
                menu()

#End of averages
    else:
        print('Invalid option selected ')
        menu()

def Sum():
#Start of Sum
    print('')
    display_list(dic_list['sum_list'],False)
    user_input = input('Please select an option in the above list: ').lower()
    
    if user_input == 'avg per role' or user_input == '1':
        user_input = input(dic_list['Overall_or_Latest'][0] + ' or ' + dic_list['Overall_or_Latest'][1] + '? ').lower()

#ROLE SUM 
        if user_input == 'overall':
            role_option = np.unique(np_data_role_latest)
            display_list(role_option,True)
            user_input = input('Which role? ').title()
            if user_input not in np.unique(np_data_role_all):
                
                temphold = np.around(raw_data.groupby("Role")['EURO Value'].sum(),2)
                df_temphold = pd.DataFrame(temphold)
                print('Role not selected, here is the sum values for all Roles')
                print(order_values(df_temphold,False))
                display_graph(df_temphold,'Role','s',True)
                print(' ')
                menu()
            else:
                temphold = np.around(np.sum(np_data_EValue_multi[(user_input).title() == np_data_role_all]),2)
                print('The sum value for the role ' + user_input.title() + ' is: ' + str(temphold))
                print(' ')
                menu()
        else:
            role_option = np.unique(np_data_role_latest)
            display_list(role_option,True)
            user_input = input('Which role? ').title()
            if user_input not in np.unique(np_data_role_all):
                print('Role spelt incorrectly but here is the sum values for all Roles')
                temphold = np.around(u_data.groupby("Role")['EURO Value'].sum(),2)
                df_temphold = pd.DataFrame(temphold)
                print(order_values(df_temphold,False))
                display_graph(df_temphold,'Role','s',False)
                print(' ')
                menu()
            else:
                temphold = np.around(np.sum(np_data_EValue_sin[(user_input).title() == np_data_role_latest]),2)
                print('The sum value for the role ' + user_input.title() + ' is: ' + str(temphold))
                print(' ')
                menu()
                             
#TEAM SUM
    elif user_input == 'avg per team' or user_input == '2':
        user_input = input(dic_list['Overall_or_Latest'][0] + ' or ' + dic_list['Overall_or_Latest'][1]+ ' ? ').lower()
        if user_input == 'overall':
            team = np.unique(np_data_team_all)
            display_list(team,True)
            user_input = input('Which team? ').title()
            
            if user_input not in np.unique(np_data_team_all):
                temphold = np.around(raw_data.groupby("Team")['EURO Value'].sum(),2)
                hold = pd.DataFrame(temphold)
                df_temphold = hold.merge(df_short_name,how='left', left_on='Team',right_on='Full_Name')
                print('Team not selected, here is the sum values for all Teams')
                print(order_values(df_temphold,False))
                display_graph(df_temphold,'Full_Name','s',True)
                print(' ')
                menu()
            else:
                temphold = np.around(np.mean(np_data_EValue_multi[np_data_team_all == (user_input).title()]),2)
                print('The sum value for the team: ' + (user_input).title() + ' is ' + str(temphold))
                print(' ')
                menu()
        else:
            team = np.unique(np_data_team_all)
            display_list(team,True)
            user_input = input('Which team? ').title()
            
            if user_input not in np.unique(np_data_team_all):
                temphold = np.around(u_data.groupby("Team")['EURO Value'].sum(),2)
                hold = pd.DataFrame(temphold)
                df_temphold = hold.merge(df_short_name,how='left', left_on='Team',right_on='Full_Name')
                print('Team not selected, here is the sum values for all Teams')
                print(order_values(df_temphold,False))
                display_graph(df_temphold,'Full_Name','s',False)
                print(' ')
                menu()
            else:
                temphold = np.around(np.mean(np_data_EValue_sin[np_data_team_latest == (user_input).title()]),2)
                print('The sum value for the team: ' + (user_input).title() + ' is ' + str(temphold))
                print(' ')
                menu()

#YEAR SUM
    elif user_input == 'sum per year' or user_input == '3':
        user_input = input(dic_list['Overall_or_Latest'][0] + ' or ' + dic_list['Overall_or_Latest'][1]+ '? ').lower()
        if user_input == 'overall':
            temphold = np.around(raw_data.groupby("Year")['EURO Value'].sum(),2)
            df_temphold = pd.DataFrame(temphold)
            print(order_values(df_temphold,False))
            display_graph(df_temphold,'Year','s',True)
            menu()
        else: 
            year_values = np.unique(np_data_year_all)
            display_list(year_values,False)
            user_input = input('Which Year? ').lower()
            if user_input in (year_values):
                temphold = np.around(np.sum(np_data_EValue_sin[np_data_year_latest == (user_input).title()]),2)
                print('The sum value for the latest year: ' + (user_input).title() + ' is ' + str(temphold))
                menu()
            else:
                print('Year data not available')
                menu()

#ORIGIN SUM
    elif user_input == 'sum per player origin' or user_input == '4':
        user_input = input(dic_list['Overall_or_Latest'][0] + ' or ' + dic_list['Overall_or_Latest'][1] + ' ? ').lower()
        if user_input == 'overall':
            player_origin = np.unique(np_data_origin_all)
            display_list(player_origin,True)
            user_input = input('Which origin? ').title()
            if user_input not in player_origin:
                temphold = np.around(raw_data.groupby("Player Origin")['EURO Value'].sum(),2)
                df_temphold = pd.DataFrame(temphold)
                print(order_values(df_temphold,False))
                display_graph(df_temphold,'Origin','s',True)
                menu()
            else:
                temphold = np.around(np.sum(np_data_EValue_multi[np_data_origin_all == (user_input).title()]),2)
                print('The sum value for the player origin: ' + (user_input).title() + ' is ' + str(temphold))
                menu()
        else:
            player_origin = np.unique(np_data_origin_all)
            display_list(player_origin,True)
            user_input = input('Which origin? ').title()
            if user_input not in player_origin:
                temphold = np.around(u_data.groupby("Player Origin")['EURO Value'].sum(),2)
                df_temphold = pd.DataFrame(temphold)
                print(order_values(df_temphold,False))
                display_graph(df_temphold,'Origin','s',False)
                menu()
            else:
                temphold = np.around(np.sum(np_data_EValue_sin[np_data_origin_latest == (user_input).title()]),2)
                print('The sum value for the player origin: ' + (user_input).title() + ' is ' + str(temphold))
                menu()

#End of Sum
    else:
        print('Invalid option selected ')
        menu()

def other_player_info():
#start of player breakdown
    print('Welcome to player breakdown info ')
    print('')
    display_list(dic_list["player_option_list"],False)
    print('')
    user_input = input('Please select an option in the above list:  ' ).lower()

#PLAYERS WITH MULTIPLE TEAMS
    if user_input == 'player movement' or user_input == '1':
        Player_movement = pd.DataFrame(raw_data.groupby(['Player','Team'])["Team"].count())
        Player_movement_2 = pd.DataFrame(Player_movement.groupby('Player')['Team'].count())
        sortedPM = Player_movement_2.sort_values(by='Team',ascending=False)
        pdPM = pd.DataFrame(sortedPM)
        new_index = []
        length_of_index = len(pdPM.index)
        new_index = [i for i in range(length_of_index)]
        new_data = pdPM.set_index(pd.Index(new_index))
        new_data = new_data['Team'].value_counts().sort_values()
        user_input = input('Please input the number of Players you want to see ')
        try: 
            user_int = int(user_input)
        except ValueError:
            print("Can't input a character. We need a number ")
            user_input = input('Please input the number of Players you want to see ')
            try: 
                user_int = int(user_input)
            except ValueError:
                menu()
        print(pdPM.head(user_int))
        print(f'Above show the no. of rows {user_int}, of players and the number of teams they have played for. These are unique teams')
        print('')
        print('Below shows the combined numbers and the amount of players ')
        print(new_data)
        if input('Do you want to see this in pie chart format? Y/N ').lower() == 'y':
            new_data.plot.pie()
            plt.title('Breakdown showing how many players played for different teams')
            plt.show()
        menu()
            
#PLAYER'S LOWEST AND HIGHEST COST
    elif user_input == 'lowest cost vs highest cost' or user_input == '2':
        player_minc_vs_maxc = raw_data.pivot_table("EURO Value",index='Player',aggfunc=[np.min,np.max])
        df_temphold = pd.DataFrame(player_minc_vs_maxc)
        print(order_values(df_temphold,True))
        menu()

#TOTAL AMOUNT SPENT ON ALL PLAYERS
    elif user_input == 'value per player' or user_input == '3':
        player_value = pd.DataFrame((raw_data.groupby("Player")['EURO Value'].sum()))
        Player_movement = pd.DataFrame(raw_data.groupby(['Player'])["Team"].count())
        temphold = player_value.merge(Player_movement,how='left', on='Player')
        df_temphold = pd.DataFrame(temphold)
        user_input = input('Please input the number of Players you want to see ')
        try: 
            user_int = int(user_input)
        except ValueError:
            print("Can't input a character. We need a number ")
            user_input = input('Please input the number of Players you want to see ')
            try: 
                user_int = int(user_input)
            except ValueError:
                menu()
        print('')
        print('Below is the total amount teams spent on specific players, as well as the number of times the player was available for auction')
        df_temphold.rename(columns={df_temphold.columns[1]: 'Times available in auction'},inplace=True)
        df_temphold = df_temphold.sort_values(by='EURO Value',ascending=False)
        print(df_temphold.head(user_int),False)
        menu()

#end of player breakdown
    else:
        print('Invalid option selected ')
        menu()

def deeper_comparison():
#start of deeper comparison
    clear_console()
    print('This menu is a more detailed breakdown')
    display_list(dic_list['next_list'],False)
    print('')
    user_input = input('Please select an option in the above list: ').lower()

#comparing 2 roles to one and other or all 4 roles
    if user_input == '1' or user_input == 'comparing the 4 roles':
        print('')
        print('We are going to compare the roles')
        role_list = np.unique(np_data_role_latest)
        display_list(role_list,True)
        
        user_input1 = input('Select 1 role from the above list: ').title()
        if user_input1 in role_list:
            role1 = raw_data[raw_data['Role']==user_input1][['EURO Value','Year']]
            role1 = role1.groupby('Year')['EURO Value'].sum()
            role_list = np.delete(role_list, np.argwhere(role_list == user_input1))
            display_list(role_list,False)
            user_input2 = input('Select the 2nd role to compare to the first: ').title()
            if user_input2 in role_list:
                print('')
                role2 = raw_data[raw_data['Role']==user_input2][['EURO Value','Year']]
                role2 = role2.groupby('Year')['EURO Value'].sum()
                print('')
                data = pd.DataFrame(role1.compare(role2, keep_shape=True,keep_equal=True))
                data.rename(columns = {'Year': 'Year', 'self':user_input1,'other':user_input2}, inplace = True)
                columns_new = ['Year', user_input1, user_input2]
                print(data)
                ax = data.plot.line(y=[user_input1,user_input2],markersize=12)
                plt.ylabel('Cost in EURO Value')
                plt.xticks(horizontalalignment="center")
                plt.title(f'Comparing the Roles {user_input1} & {user_input2} over the 10 years')
                ax.yaxis.get_major_formatter().set_scientific(False)
                ax.yaxis.get_major_formatter().set_useOffset(False)
                plt.show()
            else:
                print('Role not in list')
                deeper_comparison()
        else:
            print('')
            if input('Do you want see the 4 roles compared to one and another across all years? Y/N ').lower() == 'y':
                unique_role = np.unique(np_data_role_all)
                
                for i in range(1,5):
                    if i == 1:
                        role = raw_data[raw_data['Role']==unique_role[i-1]][['EURO Value','Year']]
                        role = role.groupby('Year')['EURO Value'].sum()
                    elif i == 2:
                        role2 = raw_data[raw_data['Role']==unique_role[i-1]][['EURO Value','Year']]
                        role2 = role2.groupby('Year')['EURO Value'].sum()
                    elif i == 3:
                        role3 = raw_data[raw_data['Role']==unique_role[i-1]][['EURO Value','Year']]
                        role3 = role3.groupby('Year')['EURO Value'].sum()
                    else:
                        role4 = raw_data[raw_data['Role']==unique_role[i-1]][['EURO Value','Year']]
                        role4 = role4.groupby('Year')['EURO Value'].sum()
                for i in range(1,4):
                    if i == 1:
                        data = pd.DataFrame(role.compare(role2, keep_shape=True,keep_equal=True))
                        data.rename(columns = {'Year': 'Year', 'self':unique_role[i-1],'other':unique_role[i]}, inplace = True)
                    elif i == 2:
                        data2 = pd.DataFrame(role3.compare(role4, keep_shape=True,keep_equal=True))
                        data2.rename(columns = {'Year': 'Year', 'self':unique_role[i],'other':unique_role[i+1]}, inplace = True)
                    else:
                        new_data = pd.concat([data,data2],axis=1,join='inner')
                new_index = []
                length_of_index = len(data.index)
                new_index = [i for i in range(length_of_index)]
                new_data_2 = new_data.set_index(pd.Index(new_index))
                temphold = np.unique(np_data_year_all).astype(int)
                temphold.sort()
                new_data_2['Year'] = temphold
                print('')
                print(new_data_2)
                ax = new_data_2.plot.line(x='Year')
                plt.ylabel('Cost in EURO Value in Millions')
                plt.title('Comparing the 4 Roles over the 10 years')
                ax.yaxis.get_major_formatter().set_scientific(False)
                ax.yaxis.get_major_formatter().set_useOffset(False)
                plt.show()
                print('')
                menu()
            else:
                menu()   

#comparing 2 Teams
    elif user_input == '2' or user_input == 'comparing 2 teams spending':
        print('')
        print('We are going to compare 2 teams spending')
        team_list = np.unique(np_data_team_all)
        display_list(team_list,False)
        
        user_input1 = input('Select 1 team from the above list: ').title()
        if user_input1 in team_list:
            team1 = raw_data[raw_data['Team']==user_input1][['EURO Value','Year']]
            team1 = team1.groupby('Year')['EURO Value'].sum()
            team_list = np.delete(team_list, np.argwhere(team_list == user_input1))
            print('')
            display_list(team_list,False)
            user_input2 = input('Select the 2nd team to compare to the first: ').title()
            if user_input2 in team_list:
                print('')
                team2 = raw_data[raw_data['Team']==user_input2][['EURO Value','Year']]
                team2 = team2.groupby('Year')['EURO Value'].sum()
                print('')
                team1 = check_if_all_year(team1)
                team2 = check_if_all_year(team2)
                team1 = pd.DataFrame(team1)
                team2 = pd.DataFrame(team2)
                try: 
                    data = pd.DataFrame(team1.compare(team2, keep_shape=True,keep_equal=True))
                    data.rename(columns = {'Year': 'Year', 'self':user_input1,'other':user_input2}, inplace = True)
                except ValueError:
                    if team1.equals(team2) == False:
                        default_year_list = np.unique(np_data_year_all)
                        data = pd.DataFrame(index=default_year_list)
                    if '0' in team1.columns:
                        data['t1'] = team1['0']
                    else:
                        data['t1'] = team1.iloc[:,0]
                    if '0' in team2.columns:
                        data['t2'] = team2['0']
                    else:
                        data['t2'] = team2.iloc[:,0]
                    data.rename(columns = {'Year': 'Year', 't1':user_input1,'t2':user_input2}, inplace = True)

                    
                new_index = []
                length_of_index = len(data.index)
                new_index = [i for i in range(length_of_index)]
                new_data = data.set_index(pd.Index(new_index))
                temphold = np.unique(np_data_year_all).astype(int)
                temphold.sort()
                new_data['Year'] = temphold
                columns_new = [user_input1, user_input2, 'Year']
                new_data.set_axis(columns_new, axis='columns', inplace=True)
                new_data[user_input1] = new_data[user_input1].astype(str).apply(lambda x: x.replace('.0', ''))
                new_data[user_input2] = new_data[user_input2].astype(str).apply(lambda x: x.replace('.0', ''))
                new_data[user_input1] = new_data[user_input1].astype(int)
                new_data[user_input2] = new_data[user_input2].astype(int)
                ax = new_data.plot.barh(x='Year')
                plt.xlabel('Cost in EURO Value in Millions')
                plt.title(f'Comparing the teames {user_input1} & {user_input2} over the 10 years')
                print(new_data)
                print('')
                ax.xaxis.get_major_formatter().set_scientific(False)
                ax.xaxis.get_major_formatter().set_useOffset(False)
                plt.show()
                menu()
            else:
                print('Team not in list')
                deeper_comparison()
        else:
            print('Team not in list')
            menu()

#breakdown of player origin
    elif user_input == '3' or user_input == 'comparing player origin':
        origin_india = raw_data[raw_data['Player Origin']=='Indian'][['EURO Value','Year','Role']]
        origin_india = origin_india.groupby(['Year','Role'], as_index=False).agg(sum=('EURO Value', 'sum'))
        origin_oversea = raw_data[raw_data['Player Origin']=='Overseas'][['EURO Value','Year','Role']]
        origin_oversea = origin_oversea.groupby(['Year','Role'], as_index=False).agg(sum=('EURO Value', 'sum'))
        origin_india_w = origin_india.pivot(index='Year', columns='Role', values='sum')
        origin_oversea_w = origin_oversea.pivot(index='Year', columns='Role', values='sum')
        origin_oversea_w = pd.DataFrame(origin_oversea_w)
        origin_india_w = pd.DataFrame(origin_india_w)
        data = pd.concat([origin_india_w, origin_oversea_w],keys=['India','Oversea'])
        data = data.reset_index()
        data = data.sort_values(by=['Year','level_0']).reset_index(drop=True)
        data["Year - Origin"] = data[['Year', 'level_0']].agg('-'.join, axis=1)
        print(data[['Year - Origin', 'All-Rounder',  "Batsman",   "Bowler",  "Wicket Keeper"]])
        ax = data.plot(x='Year - Origin', kind='bar',stacked=True)
        plt.ylabel('Cost in EURO Value in millions')
        plt.title('Breakdown of each role for the year and origin')
        plt.xticks(rotation=40, horizontalalignment="center")
        ax.yaxis.get_major_formatter().set_scientific(False)
        ax.yaxis.get_major_formatter().set_useOffset(False)
        plt.show()
        print(' ')
        menu()

#modelling
    elif user_input == '4' or user_input == "model for 10 year data" or user_input == "model":
        print('')
        user_input = input('Do you want to see the model for 10 year data for a role or player origin? r/o ').lower()
        if user_input == 'r':
            role_option = np.unique(np_data_role_latest)
            display_list(role_option,False)
            user_input = input('Please select one of the above Roles? ').title()
            if user_input in role_option:
                data = raw_data[raw_data['Role']==user_input][['EURO Value','Year']]
                temphold = pd.DataFrame(data)
                temphold = temphold.sort_values(by='Year').reset_index(drop=True)
                temphold['Year'] = temphold['Year'].astype(int)
                time.sleep(2)
                print('')
                ax = sns.lmplot(data=temphold,x='Year',y='EURO Value', x_jitter=0.05)
                plt.title(f'Break down of the Role: {user_input} showing the model value by Year')
                time.sleep(2)
                plt.show()
                time.sleep(2)
                menu()
            else:
                print('Role not in list')
                menu()  
        elif user_input == 'o':
            origin_option = np.unique(np_data_origin_latest)
            display_list(origin_option,False)
            user_input = input('Please select one of the above Origin? ').title()
            if user_input in origin_option:
                data = raw_data[raw_data['Player Origin']==user_input][['EURO Value','Year']]
                temphold = pd.DataFrame(data)
                temphold = temphold.sort_values(by='Year').reset_index(drop=True)
                temphold['Year'] = temphold['Year'].astype(int)
                time.sleep(2)
                print('')
                ax = sns.lmplot(data=temphold,x='Year',y='EURO Value', x_jitter=0.05)
                plt.title(f'Break down of the origin: {user_input} showing the model value by Year')
                time.sleep(2)
                plt.show()
                time.sleep(2)
                menu()
            else:
                print('Origin not in list')
                menu()  


#end of deeper comparison breakdown
    else:
        print('Invalid option selected ')
        menu()    

#menu select function
def menu():
    u_input = input('Return to main menu? Y/N ').lower()
    if u_input == 'y':
        main_menu()
    else: 
        return False 

#Start of program
stop = True

clear_console()
print('Welcome to the Main Menu')
print('')

while stop:
    print('')
    if main_menu() == False:
        stop = False