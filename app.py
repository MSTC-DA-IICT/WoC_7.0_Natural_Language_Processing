# app.py

from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import joblib
import string
from scrap import Reviews
from nltk.corpus import stopwords
import logging

logging.basicConfig(level=logging.DEBUG)    
app = Flask(__name__)

def convertmyTxt(rv): 
    
    np = [c for c in rv if c not in string.punctuation] 
    
    np = ''.join(np) 
    
    return [w for w in np.split() if w.lower() not in stopwords.words('english')] 

logisticRegression = joblib.load(".\\models\\logisticRegression.pkl")
randomForest = joblib.load(".\\models\\randomForest.pkl")
SVC = joblib.load(".\\models\\SVC.pkl")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        logging.debug(f"Received URL: {url}")
        asin = extract_asin(url)
        print(asin)
        if asin:
            logging.debug(f"Extracted ASIN: {asin}")
            reviews = scrape_reviews(asin)
            if reviews:
                classified_reviews = classify_reviews(reviews)
                return render_template('reviews.html', reviews=classified_reviews)
            else:
                logging.error("Failed to scrape reviews.")
                return 'Error: Failed to scrape reviews'
        else:
            logging.error("Invalid Amazon URL.")
            return 'Invalid Amazon URL'
    return render_template('index.html')


def extract_asin(url):

    parsed_url = urlparse(url)
    
    print(parsed_url)

    if parsed_url.netloc == 'www.amazon.com':

        # query_params = parse_qs(parsed_url.query)
        # print(query_params)
        # if 'asin' in query_params:
        #     return query_params['asin'][2]

        path_parts = parsed_url.path.split('/')
        
        # print(path_parts)
        
        return path_parts[3]
    
    elif parsed_url.netloc == 'www.amazon.in':
        
        path_parts = parsed_url.path.split('/')
        
        # print(path_parts)
        
        return path_parts[3]

    return None

def scrape_reviews(asin):

    amz = Reviews(asin)
    
    print(asin)
    
    reviews = amz.fetch_reviews()

    print(reviews)

    for review in reviews:
        
        # Remove newlines and any trailing "Read more"
        
        review['text'] = review['text'].replace("\n", " ").replace("Read more", "").strip()

    return(reviews)

def classify_reviews(reviews):

    classified_reviews = []
    
    for review in reviews:
    
        text = review['text']
    
    
    
        predicted_class = logisticRegression.predict([text])[0]
        
        if predicted_class == 'CG':
            # If predicted class is 'CG', mark the review as critical
            review['critical'] = True
        else:
            review['critical'] = False
        
        print(review)
        
        classified_reviews.append(review)
    
    return classified_reviews

if __name__ == '__main__':
    app.run(debug=True)