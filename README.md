
# Fantasy Baseball Optimization Project

## Overview

Welcome to the Fantasy Baseball Optimization Project, an adventurous exploration into the realm of fantasy baseball through the lens of optimization problems. This project uniquely blends two analytical approaches: **Live Draft Mode** and **Genetic Algorithm Exploration**, each offering distinct insights and strategies for assembling top-tier fantasy baseball teams.

---

## Live Draft Mode (Linear Optimization)

### 📊 Base Objective Function
In the Live Draft Mode, we address the optimization problem using linear strategies, perfectly tailored to fit the unique constraints of your fantasy league. Our simple base objective function is:

```math
Objective Function = max ∑_{i=1}^{n} z_i
```

Here, `z_i` represents the z-score for each statistical category, transforming diverse stats into a universal measure of performance. It's all about finding the perfect balance in your fantasy team's statistical portfolio.

### ⚖️ Constraints
This mode operates within the league-specific constraints, ensuring your team composition is both feasible and compliant with the league's structure:
- Salary Caps
- Roster Spots
- Positional Requirements

---

## Genetic Algorithm Exploration (Non-linear Optimization)

Dive into the complexity of non-linear optimization with our Genetic Algorithm Exploration. This approach adds a new dimension to your team-building strategy.

### 🌀 The Cauchy CDF Twist
Each stat is scaled by Cauchy Cumulative Distribution Function (CDF), offering a more balanced perspective for roster construction. 

```math
f(x; x_0, γ) = \frac{1}{\pi γ [1 + (\frac{x - x_0}{γ})^2]}
```

`x_0` and `γ` represent the location and scale parameters. 

### 🧠 Challenges in Genetic Algorithm
- **Complexity**: Navigating through the non-linear nature of the algorithm.
- **Computational Intensity**: Demanding substantial computing resources for robust analysis.
- **Solution Diversity**: Balancing diversity with competitiveness.
- **Parameter Tuning**: Precise adjustments of mutation rates, crossover probabilities, and population size.
- **Handling Outliers**: Strategically managing statistical extremes that can skew analysis.

---

## Installation & Running the Application

### 🛠️ Install Required Packages
Activate your virtual environment and install the necessary packages:
```bash
pip install -r requirements.txt
```

### 🚀 Running the Application
You can execute the project in two modes:

#### Live Draft Mode
Run the project in Live Draft Mode using the command:
```bash
python app.py --salary_cap 200 --hitter_file fg_hitter_2024.csv --pitcher_file fg_pitcher_2024.csv --adp_limit 250 --mode draft
```

#### Genetic Algorithm Exploration
For the Genetic Algorithm Exploration mode, use:
```bash
python app.py --salary_cap 200 --hitter_file fg_hitter_2024.csv --pitcher_file fg_pitcher_2024.csv --adp_limit 250 --mode genetic
```

---

## Conclusion

The Fantasy Baseball Optimization Project merges the thrill of fantasy baseball with the rigor of mathematical optimization. Whether you're strategizing through linear optimization in the Live Draft Mode or exploring the complex dynamics of the Genetic Algorithm, this project offers an enriching and analytical path to mastering fantasy baseball team management. Join us in pushing the boundaries of fantasy sports analysis!
