import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime
import os
import argparse  # Import argparse to handle command-line arguments

# --- Configuration (Defaults) ---
DEFAULT_TICKER = 'NQ=F'
DEFAULT_N_YEARS = 10

def fetch_data(ticker, start, end):
    """
    Fetches historical data from Yahoo Finance.
    """
    print(f"Fetching data for {ticker} from {start} to {end}...")
    try:
        data = yf.download(ticker, start=start, end=end, auto_adjust=True)
        if data.empty:
            print(f"No data found for {ticker} in the specified range. Please check the ticker symbol.")
            return None
        return data
    except Exception as e:
        print(f"An error occurred while fetching data: {e}")
        return None

def calculate_seasonality(data):
    """
    Calculates the average daily return for each date of the year and
    the cumulative return curve.
    """
    # Calculate daily returns
    data['Daily Return'] = data['Close'].pct_change()

    # Drop the first row which will have a NaN value and create an explicit copy
    data = data.dropna().copy()

    # Extract month and day from the index to group by date
    data['Month'] = data.index.month
    data['Day'] = data.index.day

    # Calculate the average daily return for each unique date (month-day)
    average_daily_returns = data.groupby(['Month', 'Day'])['Daily Return'].mean()

    # Create a new DataFrame for the seasonality index
    seasonality_df = pd.DataFrame(average_daily_returns)
    seasonality_df.index = [f"{m:02d}-{d:02d}" for m, d in seasonality_df.index]

    # Calculate the cumulative sum of the average daily returns
    seasonality_df['Cumulative Return'] = (1 + seasonality_df['Daily Return']).cumprod() - 1

    return seasonality_df

def plot_seasonality(seasonality_df, ticker, save_path=None):
    """
    Plots the seasonality chart and optionally saves it to a file.
    """
    plt.style.use('seaborn-v0_8-darkgrid')
    plt.figure(figsize=(12, 7))

    # Plotting the cumulative returns
    plt.plot(seasonality_df['Cumulative Return'], color='#007acc', linewidth=2)

    # Adding a horizontal line at y=0 for reference
    plt.axhline(0, color='grey', linestyle='--', linewidth=1)

    # Adding title and labels
    plt.title(f'Market Seasonality Chart ({ticker})', fontsize=16, fontweight='bold')
    plt.xlabel('Date of Year', fontsize=12)
    plt.ylabel('Cumulative Average Return', fontsize=12)

    # Customizing x-axis ticks to show month labels
    month_starts = [i for i, date_str in enumerate(seasonality_df.index) if date_str.endswith('-01')]
    month_labels = [datetime.strptime(date_str, '%m-%d').strftime('%b') for date_str in seasonality_df.index if date_str.endswith('-01')]
    plt.xticks(month_starts, month_labels, rotation=45)

    plt.grid(True)
    plt.tight_layout()

    # Add the signature text
    plt.figtext(0.99, 0.01, 'chart created by Handiko', horizontalalignment='right', fontsize=10, color='black', fontweight='bold')

    # Save the plot if a save path is provided
    if save_path:
        try:
            plt.savefig(save_path)
            print(f"Plot saved successfully to {os.path.abspath(save_path)}")
        except Exception as e:
            print(f"An error occurred while saving the plot: {e}")

    print("Displaying the seasonality chart.")
    plt.show()

# --- Modified Main Function ---
def main(ticker=DEFAULT_TICKER, n_years=DEFAULT_N_YEARS):
    """
    Main function to run the seasonality analysis with dynamic inputs.
    """
    # Calculate dates based on input parameters
    end_date = pd.to_datetime('today')
    start_date = end_date - pd.DateOffset(years=n_years)
    save_path = f'./{ticker}_seasonality_chart.png'

    # Fetch data
    data = fetch_data(ticker, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))

    if data is not None:
        seasonality_data = calculate_seasonality(data)
        plot_seasonality(seasonality_data, ticker, save_path)

if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Generate a market seasonality chart.")
    parser.add_argument('--ticker', type=str, default=DEFAULT_TICKER, help='Ticker symbol (default: ^JKSE)')
    parser.add_argument('--years', type=int, default=DEFAULT_N_YEARS, help='Number of years of historical data (default: 10)')

    args = parser.parse_args()

    # Run main with parsed arguments
    main(ticker=args.ticker, n_years=args.years)