# Import libraries for Network Requests, scrap information from web pages and CSV
import requests 
from bs4 import BeautifulSoup
import csv

class Scraper:
    def __init__(self, url, selectors, output_file="imdb_data.csv"):
        """
        :param url: Target URL of the IMDb list.
        :param selectors: Dictionary of CSS selectors for the data to be extracted.
        :param output_file: Name of the output CSV file.
        """
        self.url = url
        self.selectors = selectors
        self.data = {}
        self.output_file = output_file

    def fetch_page(self):
        """
        Fetch the webpage and return the response if successful.
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        print("Fetching page...")
        response = requests.get(self.url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch data. HTTP Status Code: {response.status_code}")
            return None
        return response.text

    def parse_data(self, page_content):
        """
        Parse the page content to extract data based on provided CSS selectors.
        """
        soup = BeautifulSoup(page_content, 'lxml')

        # Extract data for each selector
        for key, selector in self.selectors.items():
            elements = soup.select(selector)
            self.data[key] = [element.getText().strip() for element in elements]

    def save_to_csv(self):
        """
        Save the scraped data to a CSV file.
        """
        if not self.data:
            print("No data to save. Please check the selectors.")
            return

        # Transpose the data to rows for CSV writing
        rows = list(zip(*self.data.values()))

        print(f"Saving data to {self.output_file}...")
        with open(self.output_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            # Write headers (keys of the selectors dictionary)
            writer.writerow(self.data.keys())
            # Write rows
            writer.writerows(rows)
        print(f"Data saved to {self.output_file} successfully!")

    def display_data(self):
        """
        Display the scraped data in a readable format.
        """
        if not self.data:
            print("No data to display. Please check the selectors.")
            return

        print(f"Scraped Data from {self.url}:")
        for key, values in self.data.items():
            print(f"\n{key.capitalize()}:")
            for i, value in enumerate(values, start=1):
                print(f"{i}. {value}")

    def scrape(self):
        """
        Main method to scrape the website and save data to a CSV file.
        """
        page_content = self.fetch_page()
        if page_content:
            self.parse_data(page_content)
            self.display_data()
            self.save_to_csv()


if __name__ == "__main__":
    # URL of the IMDb list
    # url = "https://www.imdb.com/list/ls063771441/"
    url = "https://rxtechexam.com/top-100-drugs/?srsltid=AfmBOorHLkaSwyn24e37AOV8x-F96urB7UOa_QfSSv2qy2f_Mgb6pF-K"

    # Define CSS selectors for the data you want to scrape
    selectors = {
        # "titles": ".ipc-title__text",                    # Movie title selector
        # "ratings": ".ipc-rating-star--rating",           # Movie rating selector
        # "votes": ".ipc-rating-star--voteCount",          # Vote count selector
        "Generic Name": ".column-1",
        "Brand Name": ".column-2",
        "Indication Name": ".column-3",
        "Medication Name": ".column-4",
        "DEA Name": ".column-5",
        # "author": ".authorOrTitle",
    }

    scraper = Scraper(url, selectors)
    scraper.scrape()
