import pandas as pd
import src.optimizer as optimizer
import ipdb

def get_player(df, player_name):
    """
    Retrieve a player's data from the dataframe.
    """
    return df.loc[df['PlayerName'] == player_name]


def add_players(df, player_names, team):
    """
    Add players to a team.
    """
    players = [get_player(df, name) for name in player_names]
    team = pd.concat([team] + players, ignore_index=True)
    return team


def drop_player(player_name, team):
    """
    Remove a player from a team.
    """
    return team[team['PlayerName'] != player_name]


def add_cost(df, player_name, cost):
    """
    Update the cost for a player in the dataframe and set their dollars to be that cost
    """
    df.loc[df['PlayerName'] == player_name, 'Cost'] = cost
    df.loc[df['PlayerName'] == player_name, 'Dollars'] = cost


def live_draft(picks, salary_cap, df_hitter):
    my_team = pd.DataFrame()

    # determine available hitters
    available_hitters = df_hitter.query('Cost == 0 and Dollars >= 1').copy()
    available_hitters['Dollars'] = available_hitters['Dollars'].clip(lower=1)
    
    for _ in range(picks):
        # Combine with my team for optimization
        opti_hitter = pd.concat([my_team, available_hitters])
        opti_hitter.reset_index(inplace=True)

        # Optimization step 
        predicted_lineup, cost_h, points_h = optimizer.optimize_hitter_lineup(opti_hitter, salary_cap)

        # Get nominated player's max value and lineup
        nom_player_name = input("Please enter nominated player name: ")
        predicted_lineup2, cost_h2, points_h2, target_cost = optimizer.optimize_hitter_value(
            opti_hitter, salary_cap, nom_player_name, points_h
        )
        print(get_player(df_hitter, nom_player_name))

        # Update player cost and check if drafted
        auction_sold = int(input("Enter sold price: "))
        add_cost(df_hitter, nom_player_name, auction_sold)

        if input("Did you draft this player? y or n: ").lower() == 'y':
            # Add drafted player to the team 
            my_team = add_players(df_hitter, [nom_player_name], my_team)
        
        # remove nominated player from available hitters
        player_index = available_hitters[available_hitters['PlayerName'] == nom_player_name].index
        available_hitters = available_hitters.drop(player_index)
        available_hitters = available_hitters.reset_index(drop=True)
    
    return my_team
