import requests
from bs4 import BeautifulSoup

class Reviews:
    def __init__(self, asin):
        self.asin = asin
        self.url = f"https://www.amazon.com/dp/{self.asin}/?th=1"

    def fetch_reviews(self):
        try:
            # Send a GET request to the target URL
            response = requests.get(self.url)

            # Check if the response status code is not 200 (OK)
            if response.status_code != 200:
                print(f"An error occurred with status {response.status_code}")
                return []

            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract review texts
            review_texts = soup.find_all("span", class_="review-text")
            review_texts_list = [text.get_text(separator="\n").strip() for text in review_texts]

            # Create a dictionary to store the review details
            reviews = []
            for text in review_texts_list:
                reviews.append({"text": text})

            return reviews

        except Exception as e:
            print(f"Error fetching reviews: {e}")
            return []


# if __name__ == '__main__':
#     asin = 'B0CZVTR63Y'  
#     scraper = Reviews(asin)
#     reviews = scraper.fetch_reviews()
#     print(reviews)