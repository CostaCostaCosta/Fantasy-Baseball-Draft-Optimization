import numpy as np
import pandas as pd
import scipy.stats
import io
import pulp
import ipdb

def hitter_constraints(problem, df, player_in_lineup, SALARY_CAP, NUM_PLAYERS):
    """
    Set the hitter constraints for the linear programming problem.
    """
    print("NUM_PLAYERS length:", len(NUM_PLAYERS))
    print("player_in_lineup length:", len(player_in_lineup))

    # Constraint: Sum of player costs must be less than or equal to the salary cap
    problem += sum(player_in_lineup[i] * df.iloc[i]['Dollars']for i in NUM_PLAYERS) <= SALARY_CAP

    # Constraint: 
    rostered_hitters = df['Cost'] > 0
    problem += pulp.lpSum(player_in_lineup[i] * rostered_hitters.iloc[i] for i in NUM_PLAYERS) == sum(rostered_hitters)
    
    # Constraint: Teams must have X players drafted (4 flyers + catcher)
    problem += pulp.lpSum(player_in_lineup) == 8

    # Positional constraints
    positions = ['C', '1B', '2B', '3B', 'SS', 'OF']
    for pos in positions:
        pos_players = df['PP'].str.contains(pos)
        problem += pulp.lpSum(player_in_lineup[i] * pos_players[i] for i in NUM_PLAYERS) >= (0 if pos == 'C' else 1)

    return problem


def optimize_hitter_lineup(df):
    """
    Function to optimize the selection of players for a fantasy baseball game using linear programming.
    
    # Initialize linear programming problem
    Parameters:
    df (DataFrame): DataFrame containing player stats and costs.

    Returns:
    predicted (list): List of selected player names.
    cost (float): Total cost of selected players.
    points (float): Total points of selected players.
    """
    
    # Extract cost and points for each player from dataframe
    player_costs = df['Dollars'].values  # using projected prices
    player_points = df['PTS'].values

    # Extract hitting stats for each player from dataframe
    # Hitting stats are represented by columns in df that start with "m"
    hitting_columns = [col for col in df.columns if col.startswith('m')]
    player_stats = {stat: df[stat].values for stat in hitting_columns}
    
    # Define the salary cap and the range for number of players
    SALARY_CAP = 270 * 0.8 - 10
    NUM_PLAYERS = range(len(player_costs))
    # Initialize the linear programming problem
    problem = pulp.LpProblem("Optimal_Lineup", pulp.LpMaximize)

    # Create variable to represent each player
    # Create a binary variable for each player to represent whether they are in the lineup or not
    player_in_lineup = pulp.LpVariable.dicts("Players", NUM_PLAYERS, 0, 1, cat="Binary")

    # Create objective: maximize sum of player points
    problem += pulp.lpSum(player_in_lineup[i] * sum(scipy.stats.cauchy.cdf(player_stats[stat][i]) for stat in player_stats) for i in NUM_PLAYERS)

    # Apply hitter constraints
    hitter_constraints(problem, df, player_in_lineup, SALARY_CAP, NUM_PLAYERS)

    # Solve the problem and output results
    points, cost = 0, 0
    predicted = []

    if problem.solve() == 1:
        print("Current Optimal Lineup")
        for pos in NUM_PLAYERS:
            if player_in_lineup[pos].value() == 1:
                predicted.append(df['PlayerName'][pos])
                cost += player_costs[pos]
                points += player_points[pos]
                print(f'{df["PlayerName"][pos]:25s}, Position = {df["POS"][pos]:2s},Price = {player_costs[pos]:5.2f}, Points = {player_points[pos]:3.2f}')
        print(f'\nTotal Team Cost: {int(cost):5d}\nTotal Team Points: {points:5.2f}')
    else:
        print('Error finding solution')

    return predicted, cost, points


def optimize_hitter_value(df, hitter_name, min_points):
    """
    Function to find the max value of a baseball hitter using linear programming.

    Parameters:
    df (pandas.DataFrame): DataFrame of players with columns 'PlayerName', 'Dollars', 'PTS', and 'POS'.
    hitter_name (str): The name of the hitter to optimize.
    min_points (float): The minimum points that the hitter should have.

    Returns:
    list: List of players in the optimized lineup.
    float: Total cost of the optimized lineup.
    float: Total points of the optimized lineup.
    float: The optimized value of the target cost.
    """
    # Copy the dataframe to avoid changing the original dataframe
    df_copy = df.copy()
    # Set the cost of the target hitter to 0
    df_copy.loc[df_copy['PlayerName'] == hitter_name, 'Dollars'] = 0

    # Define the salary cap and the number of players
    salary_cap = 193
    num_players = range(len(df_copy))

    # Define the problem
    problem = pulp.LpProblem("Maximize_Player_Value", pulp.LpMaximize)

    # Create a binary variable to state that a player is in the lineup or not
    player_in_lineup = pulp.LpVariable.dicts("Players", num_players, 0, 1, cat="Binary")

    # Create a variable for the target cost
    target_cost = pulp.LpVariable("TC")

    # The objective function is to maximize the target cost
    problem += target_cost

    # Constraint: The target player must be in the lineup
    target = df_copy['PlayerName'] == hitter_name
    problem += pulp.lpSum(player_in_lineup[i] * target[i] for i in num_players) == 1

    # Constraint: The total points of the players in the lineup must be greater than or equal to the minimum points
    problem += pulp.lpSum(player_in_lineup[i] * df_copy.iloc[i]['PTS'] for i in num_players) >= min_points

    # Apply hitter_constraints
    hitter_constraints(problem, df_copy, player_in_lineup, salary_cap, num_players)

    # Initialize the total cost and points
    total_cost, total_points = 0, 0
    # Initialize the lineup
    predicted_lineup = []

    # If the problem has an optimal solution
    if problem.solve() == pulp.LpStatusOptimal:
        print("Hypothetical Lineup")
        print(hitter_name, target_cost.value())
        # Loop through the players
        for pos in num_players:
            # If the player is in the lineup
            if player_in_lineup[pos].value() == 1:
                # Add the player to the lineup
                predicted_lineup.append(df_copy['PlayerName'][pos])
                # Add the cost and points of the player to the total cost and points
                total_cost += df_copy['Dollars'][pos]
                total_points += df_copy['PTS'][pos]
                print(f'{df_copy["PlayerName"][pos]:25s}, Position = {df_copy["POS"][pos]:2s}, Price = {df_copy["Dollars"][pos]:5.f}, Points = {df_copy["PTS"][pos]:3.2f}')
    else:
        print('Error finding solution')

    # Return the lineup, total cost, total points, and the value of the target cost
    return predicted_lineup, total_cost, total_points, target_cost.value()
