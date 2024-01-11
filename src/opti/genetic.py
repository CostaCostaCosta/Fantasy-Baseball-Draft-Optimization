from deap import base, creator, tools, algorithms
import scipy.stats
import random
import ipdb

# Example parameters
num_players = 100
salary_cap = 200
team_size_limit = 10  # Hard limit for the team size
df = [{'A': random.randint(-5, 5), 'B': random.randint(-5, 5), 'Dollars': random.randint(1, 50)} for _ in range(num_players)]

# Fitness function

def make_fitness_function(df, salary_cap):
    def fitness(individual):
        total_cost = sum(individual[i] * df[i]['Dollars'] for i in range(num_players))
        if total_cost > salary_cap:
            return -100,  # Penalize for exceeding salary cap

        total_A = sum(individual[i] * df[i]['A'] for i in range(num_players))
        total_B = sum(individual[i] * df[i]['B'] for i in range(num_players))
        return scipy.stats.cauchy.cdf(total_A) + scipy.stats.cauchy.cdf(total_B),
    
    return fitness

# Feasibility function
def is_feasible(individual):
    num_players_selected = sum(individual)
    return num_players_selected == team_size_limit

# Set up the Genetic Algorithm
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, num_players)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

fitness_function = make_fitness_function(df, salary_cap)
toolbox.register("evaluate", fitness_function)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

# Create initial population and run the GA
population = toolbox.population(n=50)
ngen = 40

for gen in range(ngen):
    # Generate offspring
    offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.2)

    # Check for feasibility and only keep feasible individuals
    feasible_offspring = [ind for ind in offspring if is_feasible(ind)]
    print("Number of feasible solutions: ", len(feasible_offspring))

    # Evaluate the fitness of feasible offspring
    fitnesses = map(toolbox.evaluate, feasible_offspring)
    for ind, fit in zip(feasible_offspring, fitnesses):
        ind.fitness.values = fit
        print("Fitness values: ", ind.fitness.values)

    # Update the population
    population[:] = toolbox.select(population + feasible_offspring, len(population))

# Best solution
if population:
    best_ind = tools.selBest(population, 1)[0]
    print("Best Individual:", best_ind)
    print("Best Fitness:", best_ind.fitness.values[0])
else:
    print("No feasible solution found.")



# # Example parameters (to be defined according to your problem)
# num_players = 100
# salary_cap = 200
# team_size = 5
# df = [{'A': random.randint(-5, 5), 'B': random.randint(-5, 5), 'Dollars': random.randint(5, 50)} for _ in range(num_players)]

# def is_feasible(individual, team_size_limit):
#     """
#     Check if the individual meets the team size limit constraint.
#     """
#     num_players_selected = sum(individual)
#     return num_players_selected <= team_size_limit


# def make_fitness_function(df, salary_cap, team_size):
#     def fitness(individual):
#         team = [df[i] for i in range(len(individual)) if individual[i] == 1]
#         # Count the number of players selected
#         num_players_selected = sum(individual)

#         # Penalize if the team size exceeds the limit or if the cost exceeds the salary cap
#         if num_players_selected != team_size:
#             return -100,  # Penalize for exceeding team size limit
    
#         total_cost = sum(player['Dollars'] for player in team)
#         if total_cost > salary_cap:
#             return -100,  # Penalize if cost exceeds limit
#         total_A = sum(player['A'] for player in team)
#         total_B = sum(player['B'] for player in team)
#         return scipy.stats.cauchy.cdf(total_A) + scipy.stats.cauchy.cdf(total_B),
#     return fitness


# # Set up the Genetic Algorithm
# creator.create("FitnessMax", base.Fitness, weights=(1.0,))
# creator.create("Individual", list, fitness=creator.FitnessMax)

# toolbox = base.Toolbox()
# toolbox.register("attr_bool", random.randint, 0, 1)
# toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, num_players)
# toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# # Using custom fitness function
# fitness_function = make_fitness_function(df, salary_cap)
# toolbox.register("evaluate", fitness_function)

# toolbox.register("mate", tools.cxTwoPoint)
# toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
# toolbox.register("select", tools.selTournament, tournsize=3)

# # Create initial population and run the GA
# population = toolbox.population(n=1000) #50
# ngen = 40
# result, log = algorithms.eaSimple(population, toolbox, cxpb=0.5, mutpb=0.2, ngen=ngen, verbose=True)

# # Best solution
# best_ind = tools.selBest(population, 1)[0]
# print("Best Individual:", best_ind)
# print("Best Fitness:", best_ind.fitness.values[0])
