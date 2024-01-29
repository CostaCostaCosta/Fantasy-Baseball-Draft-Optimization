#Roto League Analysis 
import pandas as pd
import io
import os
import ipdb
import src.draft as draft
import src.opti.genetic as genetic

class RotoLeagueAnalysis:
    """
    This class is used for analyzing RotoLeague data. 
    It includes various methods to process hitter and pitcher data.
    """
    def __init__(self, salary_cap, draft_picks, hitter_file_name, pitcher_file_name, adp_limit=300):
      """
      Initialize the class with hitter file, pitcher file and adp limit.
      """
      self.salary_cap = salary_cap
      self.draft_picks = draft_picks
      self.hitter_file_name = hitter_file_name
      self.pitcher_file_name = pitcher_file_name
      self.adp_limit = adp_limit
      self.df_hitter = None
      self.df_pitcher = None
    
    def load_files(self):
        """
        Loads CSV or PKL files containing hitter and pitcher data into pandas dataframes.
        """
        self.df_hitter = self.load_file(self.hitter_file_name)
        self.df_pitcher = self.load_file(self.pitcher_file_name)

    def load_file(self, file_name):
        """
        Loads a file (either CSV or PKL) into a pandas dataframe.
        """
        # file_path = os.path.join('../data', file_name)
        file_path = os.path.join('data', file_name)
        file_extension = os.path.splitext(file_path)[1].lower()

        if file_extension == '.csv':
            return pd.read_csv(file_path, dtype=str)
        elif file_extension == '.pkl':
            return pd.read_pickle(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")

    
    def process_hitter_data(self):
        """
        Processes hitter data by renaming columns, converting string values to float, filtering data based on ADP limit,
        and assigning positions to players in a specific order. Also adds a new column "Cost" if it does not already exist.
        """
        self.df_hitter.rename(columns={self.df_hitter.columns[0]: "PlayerName" },inplace=True)
        hit_columns = self.df_hitter.columns.drop(["PlayerId"])[3:]
        
        for col in hit_columns:
            self.df_hitter[col] = self.df_hitter[col].replace( '[\$,)]','', regex=True ).replace( '[(]','-', regex=True ).astype(float)
        self.df_hitter = self.df_hitter.loc[(self.df_hitter['ADP']<self.adp_limit)]
    
        self.df_hitter['PP'] = self.df_hitter['POS']
    
        positionOrder = ['C','SS','2B','3B','OF','1B','SP','DH']
        for pos in positionOrder:
            self.df_hitter.loc[self.df_hitter['PP'].str.contains(pos), 'PP'] = pos

        # limit the input values to four decimal places for limited precision
        self.df_hitter = self.df_hitter.round(4)

        # adjust position bonus (aPos) relative to the mean for everyone but catchers
        apos_mean = self.df_hitter.loc[self.df_hitter['PP'] != 'C', 'aPOS'].mean()
        self.df_hitter.loc[self.df_hitter['PP'] != 'C', 'aPOS'] = apos_mean

        # Set a 1 dollar floor for 'Dollars'
        self.df_hitter['Dollars'] = self.df_hitter['Dollars'].clip(lower=1)

        # Add Cost column if it does not exist, or fill null valu es with 0 if it does
        if 'Cost' not in self.df_hitter.columns:
            self.df_hitter['Cost'] = 0
        else:
            self.df_hitter['Cost'].fillna(0, inplace=True)
    
        # Reset the index for df_hitter
        self.df_hitter = self.df_hitter.reset_index(drop=True)

          
    def process_pitcher_data(self):
        """
        This method is used to process pitcher data.
        """
        self.df_pitcher.rename(columns={self.df_pitcher.columns[0]: "PlayerName" },inplace=True)
        pitch_columns = self.df_pitcher.columns.drop(["PlayerId"])[3:]
        for col in pitch_columns:
            self.df_pitcher[col] = self.df_pitcher[col].replace( '[\$,)]','', regex=True ).replace( '[(]','-', regex=True ).astype(float)
        self.df_pitcher = self.df_pitcher.loc[self.df_pitcher['ADP']<self.adp_limit]
        self.df_pitcher['PP'] = self.df_pitcher['POS']
        positionOrder2 = ['SP','RP','DH']
        for pos in positionOrder2:
            self.df_pitcher.loc[self.df_pitcher['PP'].str.contains(pos), 'PP'] = pos

        if 'Cost' not in self.df_pitcher.columns:
            self.df_pitcher['Cost'] = None

        # Reset the index for df_pitcher
        self.df_pitcher = self.df_pitcher.reset_index(drop=True)
    

    def preprocess(self):
        """
        This method runs the whole process of uploading and processing data.
        """
        self.load_files()
        self.process_hitter_data()
        self.process_pitcher_data()


    def draft(self):
        """
        This method runs the draft process using the processed data.
        """
        my_team = draft.live_draft(self.draft_picks, self.salary_cap, self.df_hitter)
        return my_team
    
    
    def genetic(self):
        best_ind, best_fitness = genetic.genetic_optimizer(self.df_hitter.copy(), self.salary_cap)
        best_lineup = self.df_hitter.loc[best_ind]
        # Print "Genetic Best Lineup"
        print(f"Genetic Best Lineup:\n{best_lineup}")
        # Print "Genetic Lineup Cost"
        print(f"Genetic Lineup Cost: {best_lineup['Dollars'].sum():.2f}")
        stat_totals = best_lineup[best_lineup.columns[best_lineup.columns.str.startswith('m')]].sum()
        total_sum = round(stat_totals.sum(), 2)
        print(f"{stat_totals.round(2)}, Linear Sum: {total_sum}")
        print(f"Fitness Score: {best_fitness.round(3)}")
        return best_lineup, best_fitness, stat_totals, total_sum