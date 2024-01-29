import argparse
import pandas as pd
import datetime
from src.analysis import RotoLeagueAnalysis

def run_app(args):
    # Create an object of the class
    analysis = RotoLeagueAnalysis(salary_cap=args.salary_cap, 
                                  draft_picks=10,
                                  hitter_file_name=args.hitter_file, 
                                  pitcher_file_name=args.pitcher_file,
                                  adp_limit=args.adp_limit)

    analysis.preprocess()

    # Non-linear GENETIC ALGORITHM EXPLORATION
    if args.mode == 'genetic':
        # Create a dataframe for the genetic algorithm output
        genetic_df = pd.DataFrame()

        # Iterate over the range for genetic algorithm
        for i in range(3):
            print(f"Running Genetic Iteration {i+1}")
            best_lineup, best_fitness, stat_totals, total_sum = analysis.genetic()
            best_names = ', '.join(best_lineup['PlayerName'].values)

            current_run_data = {
                'best_lineup': best_names,
                'best_fitness': best_fitness.round(4),
                'stat_totals': stat_totals,
                'total_sum': total_sum
            }
            current_run_df = pd.DataFrame(current_run_data, index=[0])
            genetic_df = pd.concat([genetic_df, current_run_df])

        unique_filename = "genetic_output/df_genetic_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".csv"
        genetic_df.to_csv(unique_filename, index=False)

    # Linear Optimization live draft 
    elif args.mode == 'draft':
        # Run the draft process
        analysis.draft()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Roto League Analysis")
    parser.add_argument("--salary_cap", type=int, required=True, help="Salary cap for the league")
    parser.add_argument("--hitter_file", type=str, required=True, help="File name for hitter data")
    parser.add_argument("--pitcher_file", type=str, required=True, help="File name for pitcher data")
    parser.add_argument("--adp_limit", type=int, default=250, help="ADP limit for the players")
    parser.add_argument("--draft_picks", type=int, default=10, help="Number of Draft Picks for simulated draft")
    parser.add_argument("--mode", type=str, choices=['genetic', 'draft'], required=True, help="Mode of operation: 'genetic' or 'draft'")

    args = parser.parse_args()
    run_app(args)
