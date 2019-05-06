# Import all the stuff
from bs4 import BeautifulSoup 
from splinter import Browser
import pandas as pd 
import requests 

# Initialize browser
def init_browser():
     
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/Users/Drew/web_scraping_hw/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


# Create the empty dictionary to hold the stuff we pull down from the web
mars_info = {}

# Scrape NASA Mars - News
def scrape_mars_news():
    try: 

        # initialize the browser
        browser = init_browser()
        # setup the URL and browser.visit it....
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)
        # grab the html
        html = browser.html
        # beautiful soup the html 
        soup = BeautifulSoup(html, 'html.parser')
        # Magically get the latest element that contains news title and news_paragraph
        news_title = soup.find('div', class_='content_title').find('a').text
        news_p = soup.find('div', class_='article_teaser_body').text
        # add the results to the dictionary
        mars_info['news_title'] = news_title
        mars_info['news_paragraph'] = news_p

        return mars_info

    finally:

        browser.quit()

# Grab the images from JPL's site
def scrape_mars_image():

    try:
        
        # initialize the browser
        browser = init_browser()
        # setup the URL and browser.visit it....
        image_url_featured = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(image_url_featured)# Visit Mars Space Images through splinter module
        # grab the html
        html_image = browser.html
         # beautiful soup the html 
        soup = BeautifulSoup(html_image, 'html.parser')
        # Magically get the background-image url from the style tag 
        featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
        # Website Url 
        main_url = 'https://www.jpl.nasa.gov'
        # Concatenate website url with scrapped route
        featured_image_url = main_url + featured_image_url
        # Display full link to featured image
        featured_image_url 
        # add the result to the dictionary
        mars_info['featured_image_url'] = featured_image_url 
        
        return mars_info

    finally:

        browser.quit()


# Mars Weather from Twitter
def scrape_mars_weather():

    try: 

        # initialize the browser
        browser = init_browser()
        # setup the URL and browser.visit it....
        weather_url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(weather_url)
        # grab the html 
        html_weather = browser.html
          # beautiful soup the html 
        soup = BeautifulSoup(html_weather, 'html.parser')
        # Magically get the weather from the tweets
        latest_tweets = soup.find_all('div', class_='js-tweet-text-container')
        # I swear this stuff is magic.  How do computers do this shenanigans?
        # for loopity loop and only grab the stuff where there's Sol and Pressure info 
        for tweet in latest_tweets: 
            weather_tweet = tweet.find('p').text
            if 'Sol' and 'pressure' in weather_tweet:
                print(weather_tweet)
                break
            else: 
                pass
        # add the results to our dictionary that we'll push to mongo later
        mars_info['weather_tweet'] = weather_tweet
        
        return mars_info

    finally:

        browser.quit()

# space-facts which is a great name for a website......
def scrape_mars_facts():

    # Go to Mars facts url 
    facts_url = 'http://space-facts.com/mars/'
    # this one is old school, so we can just pandas this bad boy and grab the table
    mars_facts = pd.read_html(facts_url)
    # make the html table into a pandas DF
    mars_df = mars_facts[0]
    # rename the columns
    mars_df.columns = ['Description','Value']
    # Set the index to the `Description` 
    mars_df.set_index('Description', inplace=True)
    # Save html code
    data = mars_df.to_html()
    # Dictionary entry from Mars | Facts
    mars_info['mars_facts'] = data

    return mars_info


# Mars - the hard one - hemisphere data

def scrape_mars_hemispheres():

    try: 

        # # initialize the browser 
        browser = init_browser()
        # setup the URL and browser.visit it.... 
        hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheres_url)
        # grab the html
        html_hemispheres = browser.html
         # beautiful soup the html 
        soup = BeautifulSoup(html_hemispheres, 'html.parser')
        # let the soup do its magic thing and get all items that contain mars hemispheres information
        items = soup.find_all('div', class_='item')
        # Create empty list for hemisphere urls 
        hemispheres_url_list = []
        # Store the main_ul 
        hemispheres_main_url = 'https://astrogeology.usgs.gov' 
        # Loopity loop
        for i in items: 
            # grab the title
            title = i.find('h3').text
            # grab the link to the full image
            partial_img_url = i.find('a', class_='itemLink product-item')['href']
            # browser.visit the full image website 
            browser.visit(hemispheres_main_url + partial_img_url)
            # grab all the htmls 
            partial_img_html = browser.html
              # magically eautiful soup the html for every individual hemisphere information website 
            soup = BeautifulSoup( partial_img_html, 'html.parser')
            # more soup magic
            img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
            # Append the retreived information
            hemispheres_url_list.append({"title" : title, "img_url" : img_url})

        mars_info['hemispheres_url_list'] = hemispheres_url_list

        return mars_info

            
    finally:

        browser.quit()
