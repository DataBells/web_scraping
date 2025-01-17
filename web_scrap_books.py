# Import libraries for network requests, scrap data from web pages and CSV to export data 
import requests 
from bs4 import BeautifulSoup
import csv

# Defining Scraper Class
class Scraper:
    def __init__(self, url, selectors, output_file="your_books.csv"):
        self.url = url
        self.selectors = selectors
        self.data = {}
        self.output_file = output_file

# Fetch the URL
    def fetch_page(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        print("Fetching page...")
        response = requests.get(self.url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch data. HTTP Status Code: {response.status_code}")
            return None
        return response.text

# Parsing URL to extract data based on selectors
    def parse_data(self, page_content):
        soup = BeautifulSoup(page_content, 'lxml')
        # Extract data for each selector
        for key, selector in self.selectors.items():
            elements = soup.select(selector)
            self.data[key] = [element.getText().strip() for element in elements]

#  Export Data to CSV
    def save_to_csv(self):
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

# Display the scraped data in readable format 
    def display_data(self):
        if not self.data:
            print("No data to display. Please check the selectors.")
            return
        
        print(f"Scraped Data from {self.url}:")
        for key, values in self.data.items():
            print(f"\n{key.capitalize()}:")
            for i, value in enumerate(values, start=1):
                print(f"{i}. {value}")
               
# Main Method
    def scrape(self):
        page_content = self.fetch_page()
        if page_content:
            self.parse_data(page_content)
            self.display_data()
            self.save_to_csv()

# Entry Point Script 
if __name__ == "__main__":
# Selected URL for web scraping (scraping top 100 medication and its's other details)
    url = "https://www.goodreads.com/list/show/9440.100_Best_Books_of_All_Time_The_World_Library_List"
# Define CSS selectors for the data you want to scrape (you can find css selectors from website by clicking inspect element)
    selectors = {
        "Title": ".bookTitle",
        "Author": ".authorName",
        "Rating": ".minirating",
    }
    scraper = Scraper(url, selectors)
    scraper.scrape()
        