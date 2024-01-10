from scipy.optimize import minimize
import numpy as np

def cauchy_cdf(x):
    return 1/np.pi * np.arctan(x) + 0.5

def objective_function(x, players_data):
    total_A = sum(x[i] * players_data[i]['A'] for i in range(len(players_data)))
    total_B = sum(x[i] * players_data[i]['B'] for i in range(len(players_data)))
    return -(cauchy_cdf(total_A) + cauchy_cdf(total_B))  # Negative sign for maximization

def cost_constraint(x, players_data, cost_limit):
    total_cost = sum(x[i] * players_data[i]['C'] for i in range(len(players_data)))
    return cost_limit - total_cost

# Example players data
players_data = [
    {'A': 10, 'B': 5, 'C': 100},
    {'A': 15, 'B': 10, 'C': 150},
    # Add more players as needed
]

# Number of players
num_players = len(players_data)

# Initial guess (none selected)
x0 = np.zeros(num_players)

# Constraint dictionary
constr = {'type': 'ineq', 'fun': cost_constraint, 'args': (players_data, 300)}  # Example cost limit 300

# Bounds for each player (0 or 1)
bounds = [(0, 1) for _ in range(num_players)]

# Solve the problem
result = minimize(objective_function, x0, args=(players_data), bounds=bounds, constraints=constr, options={'disp': True})

# Selected players
selected_players = np.round(result.x)  # Rounding to get integer values
selected_players

