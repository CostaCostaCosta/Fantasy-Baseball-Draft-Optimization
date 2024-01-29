from deap import base, creator, tools, algorithms
import scipy.stats
import random
import ipdb

import src.opti.optimizer as linear_optimizer 


# Make Fitness Function
def make_fitness_function(df, salary_cap):
    def fitness_function(individual):
        selected_df = df.iloc[individual]
        
        # Hitting stats are represented by columns in df that start with "m"
        target_columns = [col for col in selected_df.columns if col.startswith('m')]
        
        total_stats = sum(scipy.stats.cauchy.cdf(sum(selected_df[stat])) for stat in target_columns)
        total_salary = sum(selected_df['Dollars'])  # assuming 'Dollars' is the column in df that contains the salaries

        # calculate penalty for exceeding salary cap
        if total_salary > salary_cap:
            penalty = (total_salary - salary_cap) * 0.1  # adjust the penalty rate as needed
        else:
            penalty = 0

        # calculate penalty for repeating players in individual
        if len(individual) != len(set(individual)):
            penalty += 10

        return total_stats - penalty,

    return fitness_function


def controlled_mutation(individual, df, num_players_to_mutate, salary_cap):
    mutated_individual = list(individual)  # Ensure it's mutable
    
    # Randomly select 'num_players_to_mutate' players from the individual
    players_to_mutate = random.sample(mutated_individual, num_players_to_mutate)

    # Calculate the total salary after removing selected players
    total_salary_removed = df.loc[players_to_mutate, 'Dollars'].sum()
    remaining_salary_cap = salary_cap - (df.loc[mutated_individual, 'Dollars'].sum() - total_salary_removed)

    # Randomly select new players to fit within the remaining salary cap
    new_players = []
    for i in range(num_players_to_mutate):
        # set potential_replacements based on salary
        potential_replacements = df[df['Dollars'] <= remaining_salary_cap-(num_players_to_mutate+i)].index.tolist()
        # Ensure the replacements are different from current players and each other
        potential_replacements = [player for player in potential_replacements if player not in mutated_individual]

        # when we reach the final player, we should only consider the top 10 players who have a salary less than the remaining salary cap 
        if i == num_players_to_mutate - 1:
            # Select 10 highest paid remaining players in potential replacements
            top_10_paid_players = df.loc[potential_replacements].nlargest(10, 'Dollars').index.tolist()
            potential_replacements = top_10_paid_players

        if potential_replacements:
            chosen_player = random.choice(potential_replacements)
            new_players.append(chosen_player)
            potential_replacements.remove(chosen_player)
            # Update the remaining salary cap
            remaining_salary_cap -= df.loc[chosen_player, 'Dollars']

    # Replace the selected players in the individual
    for idx, player in enumerate(players_to_mutate):
        if idx < len(new_players):
            mutated_individual[mutated_individual.index(player)] = new_players[idx]

    # print(df.loc[mutated_individual])
    return creator.Individual(mutated_individual)


def generate_initial_population(df, population_size, salary_cap):
    population = []
    # Generate feasible individual using the linear optimizer
    feasible_individual_names = linear_optimizer.optimize_hitter_lineup(df, salary_cap)[0]

    # find index of feasible_individual_names in df and set feasible_individual to a list of these values
    feasible_individual = creator.Individual(df[df['PlayerName'].isin(feasible_individual_names)].index.tolist())
    population.append(feasible_individual)

    for _ in range(population_size):
        # select number of players to mutate randomly, with a max of the length of feasible_individual 
        num_players_to_mutate = min(len(feasible_individual), random.randint(1, len(feasible_individual)))

        # Apply sequential controlled mutation
        mutated_individual = controlled_mutation(feasible_individual, df, num_players_to_mutate, salary_cap)
        population.append(mutated_individual)
        
        # Check if the fitness of the mutated individual is comparable to the fitness of the feasible individual
        if mutated_individual.fitness.values >= feasible_individual.fitness.values:
            # If the fitness is comparable, update the feasible individual to be the mutated individual
            feasible_individual = mutated_individual
    
    return population


def genetic_optimizer(df, salary_cap, initial_population_size=1000, ngen=100):
    if "FitnessMax" not in dir(creator):
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    if "Individual" not in dir(creator):
        creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    toolbox.register("attr_bool", random.randint, 0, len(df)-1)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, 10)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    fitness_function = make_fitness_function(df, salary_cap)
    # repair_function = make_linear_optimization_repair(df, salary_cap)

    toolbox.register("evaluate", fitness_function)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)

    # Create initial population
    population = generate_initial_population(df, initial_population_size, salary_cap)

    # Run the GA
    for gen in range(ngen):
        offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.2)

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # Select the next generation population
        population[:] = toolbox.select(population + offspring, len(population))

    # Select the best solution
    best_ind = tools.selBest(population, 1)[0]
    best_fitness = best_ind.fitness.values[0]

    return best_ind, best_fitness