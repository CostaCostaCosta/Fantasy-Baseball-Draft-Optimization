from deap import base, creator, tools, algorithms
import random

# Example parameters (to be defined according to your problem)
num_players = 100
cost_limit = 300
players_data = [{'A': random.randint(1, 20), 'B': random.randint(1, 20), 'C': random.randint(50, 150)} for _ in range(num_players)]

# Define the fitness function
def fitness(individual):
    team = [players_data[i] for i in range(len(individual)) if individual[i] == 1]
    total_cost = sum(player['C'] for player in team)
    if total_cost > cost_limit:
        return -1,  # Returning a large negative value if the team exceeds the cost limit
    total_A = sum(player['A'] for player in team)
    total_B = sum(player['B'] for player in team)
    return cauchy_cdf(total_A) + cauchy_cdf(total_B),

# Set up the Genetic Algorithm
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, num_players)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", fitness)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

# Create initial population and run the GA
population = toolbox.population(n=50)
ngen = 40
result, log = algorithms.eaSimple(population, toolbox, cxpb=0.5, mutpb=0.2, ngen=ngen, verbose=True)

# Best solution
best_ind = tools.selBest(population, 1)[0]
print("Best Individual:", best_ind)
print("Best Fitness:", best_ind.fitness.values[0])

