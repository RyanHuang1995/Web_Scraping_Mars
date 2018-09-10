# -*- coding: utf-8 -*-
"""
Created on Fri Sep  7 17:35:52 2018

@author: vikra
"""

from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import datetime as dt

#Activate Chrome
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

def scrape_all():

    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)

    # Run all scraping functions and store in dictionary.
    data = {
        "news_title": mars_title(browser),
        "news_paragraph": mars_paragraph(browser),
        "featured_image": scrape_image(browser),
        "hemispheres": Hemispheres(browser),
        "weather": weather(browser),
        "facts": facts(browser),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_title(browser):
    #Scraping data from target website
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    html = browser.html
    soup = bs(html, "lxml")
    #Scraping the latest NEWS title and paragraph
    result = soup.find("li",class_ = "slide")
    title = result.fin("div",class_="content_title").get_text()
    
    return title


def mars_paragraph(browser):
    #Scraping data from target website
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    html = browser.html
    soup = bs(html, "lxml")
    #Scraping the latest NEWS title and paragraph
    result = soup.find("li",class_ = "slide")
    paragraph = result.fin("div",class_="article_teaser_body").get_text()
    
    return paragraph
    
def scrape_image(browser):
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    html = browser.html
    #Find the featured_image_url
    mars_feature = browser.find_by_id("full_image")
    mars_feature.click()
    #Find the more info button and click it
    more_info_elem = browser.find_by_text('more info     ')
    more_info_elem.click()
    #Scraping the image from new website
    html = browser.html
    soup = bs(html,"lxml")
    result = soup.find("figure",class_ = "lede")
    img_url = result.a.img["src"]
    feature_img_url = f"https://www.jpl.nasa.gov{img_url}"

    return feature_img_url

def weather(browser):
    #Visit Mars Twitter website
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    html = browser.html
    soup = bs(html,"lxml")
    #Scraping the latest twi
    latest_twi = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").get_text()
    
    return latest_twi

def facts(browser):
    #Visit Mars Facts website
    url = "https://space-facts.com/mars/"
    mars_fact = pd.read_html(url)
    mars_fact = pd.DataFrame(mars_fact[0])
    mars_fact.columns = ["Mars Feature","Scales"]
    
    return mars_fact


def Hemispheres(browser):
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

    return Cerberus_image, Schiaparelli_image, Syrtis_Major_image,Valles_Marineris_image


if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())