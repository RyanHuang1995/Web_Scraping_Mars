from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import datetime as dt

#Activate Chrome
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_all():

    info = scrape_info()
    Hemisphere_image = scrape_hemisphere()
    Cerberus_image = Hemisphere_image["Cerberus_image"]
    Schiaparelli_image = Hemisphere_image["Schiaparelli_image"]
    Syrtis_Major_image = Hemisphere_image["Syrtis_Major_image"]
    Valles_Marineris_image = Hemisphere_image["Valles_Marineris_image"]


    data = {
        "Title" : info["Title"],
        "Paragraph" : info["Paragraph"],
        "Image_url" : scrape_image(),
        "weather" : scrape_wheather(),
        "Fact" :scrape_fact(),
        "Cerberus_image" : Cerberus_image,
        "Schiaparelli_image" : Schiaparelli_image,
        "Syrtis_Major_image" : Syrtis_Major_image,
        "Valles_Marineris_image" : Valles_Marineris_image
        
    }

    return data
#Function to scrape for info of Mars
def scrape_info():

    browser = init_browser()

    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    html = browser.html
    soup = bs(html, "lxml")

    #Scraping the latest NEWS title and paragraph
    result = soup.find("li",class_ = "slide")
    title = result.find("div", class_="content_title").get_text()
    paragraph = result.find("div", class_="article_teaser_body").get_text()

    info = {
        "Title" : title,
        "Paragraph":paragraph
    }

    return info

def scrape_image():

    browser = init_browser()
    
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    html = browser.html
    #Find the featured_image_url
    mars_feature = browser.find_by_id("full_image")
    mars_feature.click()
    #Find the more info button and click it
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()
    #Scraping the image from new website
    html = browser.html
    soup = bs(html,"lxml")
    result = soup.find("figure",class_ = "lede")
    img_url = result.a.img["src"]
    feature_img_url = f"https://www.jpl.nasa.gov{img_url}"

    return feature_img_url

def scrape_wheather():
    browser = init_browser()
    #Visit Mars Twitter website
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    html = browser.html
    soup = bs(html,"lxml")
    #Scraping the latest twi
    latest_twi = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").get_text()

    weather = latest_twi
    return weather


def scrape_fact():

    browser = init_browser()
    #Visit Mars Facts website
    url = "https://space-facts.com/mars/"
    browser.visit(url)
    mars_fact = pd.read_html(url)
    mars_fact = pd.DataFrame(mars_fact[0])
    mars_fact.columns = ["Mars Feature","Scales"]

    return mars_fact.to_html(classes="table table-striped")


def scrape_hemisphere():

    browser = init_browser()

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    html = browser.html
    hemisphere_Cerberus = browser.find_by_text("Cerberus Hemisphere Enhanced")
    hemisphere_Cerberus.click()
    html = browser.html
    soup = bs(html,"lxml")
    hemisphere_image = soup.find("a", target = "_blank")
    print("The First image link")
    print("-------------")
    Cerberus_image = hemisphere_image["href"]

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    html = browser.html
    hemisphere_Schiaparelli = browser.find_by_text("Schiaparelli Hemisphere Enhanced")
    hemisphere_Schiaparelli.click()
    html = browser.html
    soup = bs(html,"lxml")
    hemisphere_image = soup.find("a", target = "_blank")
    print("The Second image link")
    print("-------------")
    Schiaparelli_image = hemisphere_image["href"]

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    html = browser.html
    hemisphere_Syrtis_Major = browser.find_by_text("Syrtis Major Hemisphere Enhanced")
    hemisphere_Syrtis_Major.click()
    html = browser.html
    soup = bs(html,"lxml")
    hemisphere_image = soup.find("a", target = "_blank")
    print("The Third image link")
    print("-------------")
    Syrtis_Major_image = hemisphere_image["href"]

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    html = browser.html
    hemisphere_Valles_Marineris = browser.find_by_text("Valles Marineris Hemisphere Enhanced")
    hemisphere_Valles_Marineris.click()
    html = browser.html
    soup = bs(html,"lxml")
    hemisphere_image = soup.find("a", target = "_blank")
    print("The Fourth image link")
    print("-------------")
    Valles_Marineris_image = hemisphere_image["href"]

    Hemispheres_image = {
        "Cerberus_image":Cerberus_image,
        "Schiaparelli_image" : Schiaparelli_image,
        "Syrtis_Major_image" : Syrtis_Major_image,
        "Valles_Marineris_image" : Valles_Marineris_image
    }

    return Hemispheres_image
