import numpy as np
import pandas as pd
import scipy.stats
import pulp
import ipdb


def hitter_constraints(problem, df, player_in_lineup, NUM_PLAYERS):
    """
    Set the hitter constraints for the linear programming problem.
    """
    print("NUM_PLAYERS length:", len(NUM_PLAYERS))
    print("player_in_lineup length:", len(player_in_lineup))
   
    # Constraint: Any player with 'Cost' > 0 must be in the lineup
    for i in NUM_PLAYERS:
        if df.iloc[i]['Cost'] > 0:
            problem += player_in_lineup[i] == 1

    # Constraint: Teams must have X players drafted (4 flyers + catcher)
    problem += pulp.lpSum(player_in_lineup) == 8

    # Positional constraints
    positions = ['C', '1B', '2B', '3B', 'SS', 'OF']
    for pos in positions:
        pos_players = df['PP'].str.contains(pos)
        problem += pulp.lpSum(player_in_lineup[i] * pos_players[i] for i in NUM_PLAYERS) >= (0 if pos == 'C' else 1)

    # Limit to one DH
    dh_players = df['PP'].str.contains('DH')
    problem += pulp.lpSum(player_in_lineup[i] * dh_players[i] for i in NUM_PLAYERS) <= 1

    return problem


def optimize_hitter_lineup(df, salary_cap):
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
    
    NUM_PLAYERS = range(len(player_costs))
    # Initialize the linear programming problem
    problem = pulp.LpProblem("Optimal_Lineup", pulp.LpMaximize)

    # Create variable to represent each player
    # Create a binary variable for each player to represent whether they are in the lineup or not
    player_in_lineup = pulp.LpVariable.dicts("Players", NUM_PLAYERS, 0, 1, cat="Binary")

    # Create objective: maximize sum of player points
    problem += pulp.lpSum(player_in_lineup[i] * sum((player_stats[stat][i]) for stat in player_stats) for i in NUM_PLAYERS)
    
    # Constraint: Sum of player dollars must be less than or equal to the salary cap
    problem += sum(player_in_lineup[i] * df.iloc[i]['Dollars']for i in NUM_PLAYERS) <= salary_cap

    # Apply hitter constraints
    hitter_constraints(problem, df, player_in_lineup, NUM_PLAYERS)

    # Solve the problem and output results
    points, cost = 0, 0
    predicted = []

    if problem.solve(pulp.PULP_CBC_CMD(msg=False)) == 1:
        print("Linear Optimal Lineup")
        for pos in NUM_PLAYERS:
            if player_in_lineup[pos].value() == 1:
                predicted.append(df['PlayerName'][pos])
                cost += player_costs[pos]
                points += player_points[pos]
                # print(f'{df["PlayerName"][pos]:25s}, Position = {df["POS"][pos]:2s},Price = {player_costs[pos]:5.2f}, Points = {player_points[pos]:3.2f}')
        # print(f'\Linear Team Cost: {int(cost):5d}\nLinear Team Points: {points:5.2f}')
    else:
        print('Error finding solution')

    # round points to 4 decimal places
    points = round(points, 4)

    return predicted, cost, points


def optimize_hitter_value(df, salary_cap, hitter_name, min_points):
    """
    Function to optimize the value of a baseball hitter using linear programming.

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
    
    # Create a copy of the DataFrame to avoid modifying the original data
    df_copy = df.copy()
    # Set the cost ('Dollars') of the specified hitter to 0 in the copy
    df_copy.loc[df_copy['PlayerName'] == hitter_name, 'Dollars'] = 0

    # Range object for iterating over DataFrame indices
    num_players = range(len(df_copy))

    # Initialize the linear programming problem for maximizing player value 
    # s.t. they are in a lineup that outscores the current optimal point value 
    problem = pulp.LpProblem("Maximize_Player_Value", pulp.LpMaximize)
    # Introduce a target cost variable to be optimized
    target_cost = pulp.LpVariable("TC")
    # The objective function is to maximize this target cost
    problem += target_cost

    # Create a binary variable for each player to indicate if they are in the lineup (1) or not (0)
    player_in_lineup = pulp.LpVariable.dicts("Players", num_players, 0, 1, cat="Binary")

    # Constraint: Sum of player dollars must be less than or equal to the salary cap minus target cost
    problem += sum(player_in_lineup[i] * df_copy.iloc[i]['Dollars']for i in num_players) + target_cost <= salary_cap

    # Constraint to ensure the specified hitter is in the lineup
    target = df_copy['PlayerName'] == hitter_name
    problem += pulp.lpSum(player_in_lineup[i] * target[i] for i in num_players) == 1

    # Constraint to ensure total points of players in the lineup are at least the minimum required
    problem += pulp.lpSum(player_in_lineup[i] * df_copy.iloc[i]['PTS'] for i in num_players) >= min_points

    # Additional constraints (salary cap, positions, etc.) are handled in the 'hitter_constraints' function
    hitter_constraints(problem, df_copy, player_in_lineup, num_players)

    # Initialize variables to store total cost and points of the optimized lineup
    total_cost, total_points = 0, 0
    predicted_lineup = []

    # Solve the optimization problem
    if problem.solve(pulp.PULP_CBC_CMD(msg=False)) == pulp.LpStatusOptimal:
        print("Hypothetical Lineup")
        print(hitter_name, target_cost.value())
        for pos in num_players:
            if player_in_lineup[pos].value() == 1:
                # Add player to the predicted lineup and accumulate their cost and points
                predicted_lineup.append(df_copy['PlayerName'][pos])
                total_cost += df_copy['Dollars'][pos]
                total_points += df_copy['PTS'][pos]
                print(f'{df_copy["PlayerName"][pos]:25s}, Position = {df_copy["POS"][pos]:2s}, Price = {df_copy["Dollars"][pos]:5.2f}, Points = {df_copy["PTS"][pos]:3.2f}')
    else:
        # If the problem is not solvable, print the status
        status = pulp.LpStatus[problem.status]
        print('Error finding solution:', status)

    # Return the optimized lineup, total cost, total points, and the optimized value of the target cost
    return predicted_lineup, total_cost, total_points, target_cost.value()