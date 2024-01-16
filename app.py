# %load_ext cudf.pandas
import pandas as pd
import datetime
import ipdb

from src.analysis import RotoLeagueAnalysis
def run_app():
    # Create an object of the class and run the process
    analysis = RotoLeagueAnalysis(salary_cap=200, 
                                hitter_file_name='fg_hitter_2024.csv', 
                                pitcher_file_name='fg_pitcher_2024.csv',
                                adp_limit=250) #270
    analysis.preprocess()

    # create a dataframe that contains the output of the genetic algorithm
    genetic_df = pd.DataFrame()
    
    # iterate over the range
    for i in range(50):
        best_lineup, best_fitness, stat_totals, total_sum = analysis.genetic()
        best_names = best_lineup['PlayerName'].values.tobytes()
        # create a dictionary for the current run
        current_run_data = {
            'best_lineup': best_names,
            'best_fitness': best_fitness,
            'stat_totals': stat_totals,
            'total_sum': total_sum
        }
        current_run_df = pd.DataFrame(current_run_data, index=[0])
        # use concat instead of append to add the current run data to df_genetic
        genetic_df = pd.concat([genetic_df, current_run_df])
    
    unique_filename = "df_genetic_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".csv"
    genetic_df.to_csv(unique_filename, index=False)


    # analysis.draft()

if __name__ == "__main__":
    run_app()