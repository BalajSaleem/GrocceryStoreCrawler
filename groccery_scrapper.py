# from urllib.request import urlopen as uReq
# from bs4 import BeautifulSoup as soup
#
# metro_url = 'https://metro-online.pk/category/frozen-food/frozen-ready-to-cook'
# user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
# headers = {'User-Agent':user_agent}
# uClient = uReq(metro_url)
# uClient.add_header=headers
# metro_html = uClient.read()
# uClient.close()
# page_soup = soup(metro_html, 'html.parser')
# print(page_soup.h1)
#
#


# import urllib.request
# from bs4 import BeautifulSoup as soup
# user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
#
# url = "https://metro-online.pk/category/frozen-food/frozen-ready-to-cook"
# headers={'User-Agent':user_agent,}
#
# request = urllib.request.Request(url,None,headers) #The assembled request
# response = urllib.request.urlopen(request)
# data = response.read() # The data u need
# response.close()
# page_soup = soup(data, 'html.parser')
# items = page_soup.findAll("div",{"class":"productdivinner"})
# print(items)

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class crawler:
    url = ""
    driver = webdriver.Chrome("chromedriver.exe")

    def __init__(self, url="https://metro-online.pk/"):
        print('crawler made')
        self.url = url
        self.driver.get(url)
        self.driver.maximize_window()


    def scroll_down(self):
        """A method for scrolling the page."""

        # Get scroll height.
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:

            # Scroll down to the bottom.
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load the page.
            time.sleep(2)

            # Calculate new scroll height and compare with last scroll height.
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break

            last_height = new_height

    def scrape(self):

        try:
            element = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "productdivinner"))
            )
            self.scroll_down()
            items = self.driver.find_elements_by_class_name("productdivinner")

        finally:
            print('ok done')

        print(len(items))
        for item in items:
            name = item.find_element_by_class_name("productname").text
            price = item.find_element_by_class_name("productprice").text
            imgUrl = item.find_element_by_class_name("productimg").find_element_by_tag_name("img").get_attribute("src")
            if name and price:
                print('PRODUCT: ' + name + '\t\t PRICE: ' + price + '\t\tIMG URL: ' + imgUrl)

        self.driver.quit()

    def crawl(self):
        item = ''
        try:
            element = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "submenuinner"))
            )
            self.scroll_down()
            items = self.driver.find_elements_by_class_name("submenuinner")
            # item = self.driver.find_element_by_link_text("Fresh Food")
            # item = item.find_element_by_xpath("..")
            #print('top text: ' + item.text)
            #subitems = item.find_elements_by_tag_name("ul")
            #print('subitems len:' + str(len(subitems)))
        finally:
            print('ok done with crawling')

        for item in items:
            name = item.find_element_by_xpath("..").find_element_by_xpath("..").find_element_by_tag_name('span').text
            subitems = item.find_elements_by_tag_name("ul")
            print('ITEM NAME: ' + name + ' ; TOTAL SUBITEMS:' + str(len(subitems)))
            for subitem in subitems:
                subitem_name = subitem.find_element_by_xpath("..").find_element_by_tag_name('h6').find_element_by_tag_name('a').get_attribute('text')
                links = subitem.find_elements_by_tag_name('li')
                print('SUBITEM NAME:' + subitem_name + ' ; TOTAL LINKS:' + str(len(links)))
                print('')
                for link in links:
                    a = link.find_element_by_tag_name('a')
                    print('LINK NAME: ' + a.get_attribute("text") + '; LINK: ' + a.get_attribute("href"))
                    # a.click()
                    #self.scrape()





#TODO
#if 0 elements in the subitems list, click on the link


metroCrawler = crawler()
metroCrawler.crawl()
#metroCrawler.crawl()
