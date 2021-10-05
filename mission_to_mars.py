def updatePage():
    from bs4 import BeautifulSoup as bs
    import requests
    from splinter import Browser
    from webdriver_manager.chrome import ChromeDriverManager
    import pandas as pd
    import time
    import pymongo

    ##### FInd News Articles ###
    url = "https://redplanetscience.com/"
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    browser.visit(url)

    html = browser.html
    soup = bs(html, "html.parser")

    soup_list = soup.find_all("div", class_="list_text")

    headline = []
    description = []

    for i in soup_list:
        headlines = i.find("div", "content_title").text
        descriptions = i.find("div", "article_teaser_body").text
        headline.append(headlines)
        description.append(descriptions)

    ##### FInd Featured Photo ###
    url = "https://spaceimages-mars.com/"

    browser.visit(url)
    time.sleep(0.025)

    html = browser.html
    soup = bs(html, "html.parser")
    browser.links.find_by_partial_text('FULL IMAGE').click()

    html = browser.html
    soup = bs(html, "html.parser")

    soup1 = soup.find("div", class_="floating_text_area")
    photo_link = soup1.select_one("a",target_="_blank", class_="showimg fancybox-thumbs")["href"]

    ######## Find Mars Data #############
    url = "https://galaxyfacts-mars.com/"
    tables = pd.read_html(url)
    tables

    df = tables[0]
    new_header = df.iloc[0]
    df = df[1:]
    df.columns = new_header
    df = df[["Mars - Earth Comparison","Mars","Earth"]]
    df

    ######## Find  #############
    url = "https://marshemispheres.com/"
    browser.visit(url)
    time.sleep(.025)
    html = browser.html
    soup = bs(html, "html.parser")
    soupp = soup.find('div', class_='collapsible results')
    items = soupp.find_all("div", class_="item")

    scrape_link = []
    picture_description = []
    #image links
    for i in items:
        desc_container = i.find("a", class_="itemLink product-item")['href']
        scrape_link.append(desc_container)
        picture_description.append(i.find("h3").text)

    image_link = []
    for i in scrape_link:
        scrapable_url = f'{url}{i}'
        browser.visit(scrapable_url)
        html = browser.html
        soup = bs(html, "html.parser")
        downloads = soup.find('div', class_='downloads')
        image_url = downloads.find("a")["href"]
        image_link.append(f'{url}{image_url}')
    browser.quit()    

    mars_dictionary = {
        "news": {
            "headline": headline,
            "description": description
        },
        "featured_photo" : photo_link,
        "data": df.to_dict(),
        "hemispheres": {
            "name": picture_description,
            "image_link":image_link
        }
    }

    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    db = client.Mars_Data
    Scrape_Results = db.Scrape_Results
    Scrape_Results.insert_one(mars_dictionary)

