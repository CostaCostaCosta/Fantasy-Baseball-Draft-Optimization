from src.analysis import RotoLeagueAnalysis
import ipdb

def run_app():
    # Create an object of the class and run the process
    analysis = RotoLeagueAnalysis('fg_hitter_2024.csv', 'fg_pitcher_2024.csv', adp_limit=270)
    analysis.preprocess()
    analysis.draft()

if __name__ == "__main__":
    run_app()