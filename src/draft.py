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
    Update the cost for a player in the dataframe.
    """
    df.loc[df['PlayerName'] == player_name, 'Cost'] = cost

def live_draft(picks, df_hitter):
    my_team = pd.DataFrame()
    drafted_players = []

    for _ in range(picks):
        # Filter available hitters more efficiently
        available_hitters = df_hitter.query('Cost == 0 and Dollars >= 1')
        available_hitters['Dollars'] = available_hitters['Cost'].clip(lower=1)

        # Combine with my team for optimization
        opti_hitter = pd.concat([available_hitters, my_team])

        # Optimization step 
        predicted_lineup, cost_h, points_h = optimizer.optimize_hitter_lineup(opti_hitter)

        # Get nominated player's max value and lineup
        nom_player_name = input("Please enter nominated player name: ")
        predicted_lineup2, cost_h2, points_h2, target_cost = optimizer.optimize_hitter_value(
            opti_hitter, nom_player_name, points_h
        )
        print(get_player(df_hitter, nom_player_name))

        # Update player cost and check if drafted
        auction_sold = int(input("Enter sold price: "))
        add_cost(df_hitter, nom_player_name, auction_sold)
        if input("Did you draft this player? y or n: ").lower() == 'y':
            drafted_players.append(nom_player_name)

    # Add all drafted players to the team at once
    my_team = add_players(df_hitter, drafted_players, my_team)
    return my_team


# def live_draft(picks, df_hitter):
#     """
#     Simulate a live draft for a given number of picks.
#     """
#     my_team = pd.DataFrame()

#     for _ in range(picks):
#         # Get available hitters
#         available_hitters = df_hitter[df_hitter['Cost'] == 0].copy()

#         # Adjust minimum price to 1 and set dollars for players with cost
#         available_hitters['Dollars'] = available_hitters.apply(
#             lambda row: row['Cost'] if row['Cost'] > 0 else max(row['Dollars'], 1), axis=1)

#         # Combine available hitters and my team
#         opti_hitter = pd.concat([available_hitters, my_team]).copy()

#         # Optimize hitter lineup
#         predicted_lineup, cost_h, points_h = optimizer.optimize_hitter_lineup(opti_hitter)

#         # Get nominated player name
#         nom_player_name = input("Please enter nominated player name: ")

#         # # Check if player name is valid
#         # if nom_player_name not in df_hitter['PlayerName']:
#         #     print("Invalid player name. Please try again.")
#         #     continue

#         # Determine optimal cost
#         predicted_lineup2, cost_h2, points_h2, target_cost = optimizer.optimize_hitter_value(
#             opti_hitter, nom_player_name, points_h)

#         print(get_player(df_hitter, nom_player_name))

#         # Get auction sold price
#         while True:
#             try:
#                 auction_sold = int(input("Enter sold price: "))
#                 break
#             except ValueError:
#                 print("Invalid input. Please enter a number.")

#         # Update player cost
#         add_cost(df_hitter, nom_player_name, auction_sold)

#         # Check if player was drafted
#         you_drafted = input("Did you draft this player? y or n: ").lower()
#         if you_drafted == 'y':
#             my_team = add_players(df_hitter, [nom_player_name], my_team)

#     return my_team

# def live_draft(picks, df_hitter):
#     """
#     Simulate a live draft for a given number of picks.
#     """
#     my_team = pd.DataFrame()
#     is_hitter = True

#     for _ in range(picks):
#         available_hitters = df_hitter[df_hitter['Cost'] == 0].copy()

#         # Adjust minimum price to 1
#         available_hitters.loc[available_hitters['Dollars'] < 1, 'Dollars'] = 1

#         # Players with a cost have their dollars set to their cost
#         available_hitters.loc[available_hitters['Cost'] > 0, 'Dollars'] = available_hitters['Cost']

#         opti_hitter = pd.concat([available_hitters, my_team]).copy()
        
#         if is_hitter:
#             predicted_lineup, cost_h, points_h = optimizer.optimize_hitter_lineup(opti_hitter)

#         # Input nominated player
#         nom_player_name = input("Please enter nominated player name: ")

#         # Determine optimal cost
#         predicted_lineup2, cost_h2, points_h2, target_cost = optimizer.optimize_hitter_value(
#             opti_hitter, nom_player_name, points_h
#         )
#         print(get_player(df_hitter, nom_player_name))

#         # Update player cost
#         auction_sold = int(input("Enter sold price: "))
#         add_cost(df_hitter, nom_player_name, auction_sold)

#         # Did you draft this player?
#         you_drafted = input("Did you draft this player? y or n: ")
#         if you_drafted.lower() == 'y':
#             my_team = add_players(df_hitter, [nom_player_name], my_team)

#     return my_team
