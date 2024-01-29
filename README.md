Fantasy Baseball Optimization Project
Overview

This project is dedicated to exploring optimization problems in the context of fantasy baseball. It focuses on two primary modes of analysis: a live draft mode and a genetic algorithm exploration. These approaches provide insights and strategies for building competitive fantasy baseball teams within the constraints of a given league.
Live Draft Mode (Linear Optimization)

The live draft mode employs a linear optimization problem tailored to league-specific constraints. This mode's base objective function can be expressed mathematically as:

Objective Function=∑i=1nziObjective Function=∑i=1n​zi​

where zizi​ represents the z-score for each statistical category in the league (e.g., batting average, home runs, earned run average, etc.). The z-score is a measure of how many standard deviations an element is from the mean, providing a standardized value for comparison across different statistics.
Constraints

The constraints in the live draft mode are specific to the league settings, such as salary caps, roster spots, and positional requirements. These constraints ensure that the optimization process yields feasible and league-compliant team compositions.
Genetic Algorithm Exploration (Non-linear Optimization)

The genetic algorithm exploration introduces a non-linear approach to the optimization problem. This method leverages the Cauchy cumulative distribution function (CDF) for each individual stat, providing a more nuanced evaluation of team compositions, especially for teams that are heavily weighted in one or more categories. The use of Cauchy CDF can be expressed as:

f(x;x0,γ)=1πγ[1+(x−x0γ)2]f(x;x0​,γ)=πγ[1+(γx−x0​​)2]1​

where x0x0​ is the location parameter and γγ is the scale parameter of the distribution.
Challenges of Applying a Genetic Algorithm

The application of a genetic algorithm in this context presents several challenges:

    Complexity: The genetic algorithm's non-linear nature introduces complexity in handling and interpreting the results, especially when balancing across multiple statistical categories.

    Computational Intensity: Genetic algorithms can be computationally intensive, requiring significant resources for computation, especially for large datasets and numerous iterations.

    Solution Diversity: Ensuring diversity in the solutions while maintaining competitiveness within the league's framework can be challenging.

    Parameter Tuning: The genetic algorithm requires careful tuning of parameters like mutation rates, crossover probabilities, and population size to effectively explore the solution space.

    Handling Outliers: Effectively managing statistical outliers in player performances, which can disproportionately influence the optimization process, is a critical aspect of the algorithm.

Install Required Packages:
With the virtual environment activated, install the required packages using:
pip install -r requirements.txt

Running the Application

With the environment set up, you're ready to run the application. The project can be executed in two modes: Live Draft Mode and Genetic Algorithm Exploration.
Running Live Draft Mode

Use the following command to run the project in Live Draft Mode:
python app.py --salary_cap 200 --hitter_file fg_hitter_2024.csv --pitcher_file fg_pitcher_2024.csv --adp_limit 250 --mode draft

To run the project in Genetic Algorithm Exploration mode, use:
python app.py --salary_cap 200 --hitter_file fg_hitter_2024.csv --pitcher_file fg_pitcher_2024.csv --adp_limit 250 --mode genetic


Conclusion

This project provides a comprehensive and mathematical approach to fantasy baseball team optimization. The live draft mode offers a linear optimization solution with practical constraints, while the genetic algorithm mode explores non-linear dynamics for a more in-depth analysis. The complexity and computational challenges of these methods underscore the sophisticated nature of fantasy sports analysis and the potential for innovative strategies in team management.
