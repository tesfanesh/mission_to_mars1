# dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests 

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

mars_info = {}

def mars_news():
    
    try:
        browser = init_browser()
        url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        news_title = soup.find('div', class_='content_title').text
        news_p = soup.find('div', class_='article_teaser_body').text

        mars_info['news_title'] = news_title
        mars_info['news_paragraph'] = news_p
        return mars_info

    finally:
        browser.quit()


def jpl_mars_space():

    try:
        browser = init_browser()
        url_1 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(url_1)
        html_1 = browser.html
        soup = BeautifulSoup(html_1, 'html.parser')
        img_url = soup.find('div', class_='img').find('img')['src']
        featured_image_url = 'https://www.jpl.nasa.gov' + img_url
    
        mars_info['featured_image_url'] = featured_image_url
        return mars_info

    finally:
        browser.quit()

    

    

def mars_weather():

    try:
        browser = init_browser()
        url_tweet = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(url_tweet)
        html_tweet = browser.html
        soup = BeautifulSoup(html_tweet, 'html.parser')
        latest_tweets = soup.find_all('div', class_='js-tweet-text-container')

        for tweet in latest_tweets: 
            mars_weather = tweet.find('p').text
            if 'twitter' in mars_weather:
                pass
            else: 
                mars_info['weather_tweet'] = mars_weather
        
        
        mars_info['weather_tweet'] = mars_weather

        return mars_info
    finally:
         
        browser.quit()

def mars_hemi():
    try:

        browser = init_browser()
        url_mars_hemi = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url_mars_hemi)
        links = browser.find_by_css("a.product-item img")
        hemisphere_image_urls = []
        for i in range(len(links)):
            browser.find_by_css("a.product-item img")[i].click()
            title = browser.find_by_css("h2").text
            sample = browser.find_link_by_text('Sample').first
            img_url = sample['href']
            hemisphere_image_urls.append({"title": title, "img_url": img_url})
            browser.back()

        mars_info['hemisphere_image_urls'] = hemisphere_image_urls
        return mars_info

    finally:
        browser.quit()
   


def mars_df():
    try:
        browser = init_browser()

        url = "https://space-facts.com/mars/"
        tables = pd.read_html(url)
        mars_facts_df = tables[1]
        mars_facts_df.columns = ['', 'Value']
        mars_facts_df = mars_facts_df.set_index('')
        html_table = mars_facts_df.to_html()

        mars_info['html_table'] = html_table
        return mars_info

    finally:
        browser.quit()

    


