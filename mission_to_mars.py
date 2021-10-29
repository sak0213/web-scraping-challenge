def updatePage():
    from bs4 import BeautifulSoup as bs
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
    # time.sleep(0.025)

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
    df = df.set_index("Mars - Earth Comparison")
    df

    ######## Find  #############
    url = "https://marshemispheres.com/"
    browser.visit(url)
    # time.sleep(.025)
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

    news_dict = []
    for i in range(len(headline)):
        news_dict.append({
            "headline": headline[i],
            "description": description[i]
        })

    hemisphere_dict = []
    for i in range(len(picture_description)):
        hemisphere_dict.append({"title":picture_description[i], "img_url":image_link[i]})
    print(hemisphere_dict)

    mars_dictionary = {
        "news": news_dict,
        "featured_photo" : f'https://spaceimages-mars.com/{photo_link}',
        "data": df.to_dict(),
        "hemispheres": hemisphere_dict
    }

    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    db = client.Mars_Data
    Scrape_Results = db.Scrape_Results
    db.Scrape_Results.drop()
    Scrape_Results.insert_one(mars_dictionary)

