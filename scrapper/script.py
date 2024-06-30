from taskmanager.coinmarketcap import CoinMarketCap
from bs4 import BeautifulSoup
import requests

def main():
    # Get the name of the coin from the user
    coin_name = input("Enter the name of the coin: ")

    # Initialize CoinMarketCap object
    coin_market_cap = CoinMarketCap(coin_name)

    # Make a request to fetch the HTML content of the coin's webpage
    html_content = coin_market_cap.make_request()

    # Extract data from the HTML content
    coin_data = coin_market_cap.extract_data(html_content)

    # Process the extracted data as needed
    print(coin_data)

if __name__ == "__main__":
    main()
