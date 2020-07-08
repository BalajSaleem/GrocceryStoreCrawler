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
import csv
import threading

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Crawler:
    url = ""

    driver = webdriver

    def __init__(self, url="https://metro-online.pk/"):
        self.driver = webdriver.Chrome("chromedriver.exe")
        print('crawler made')
        self.url = url
        self.driver.get(url)
        #self.driver.maximize_window()

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

    def scrape(self, url='', p_cat=''):
        if url:
            self.driver.get(url)
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "productdivinner"))
            )
            self.scroll_down()
            items = self.driver.find_elements_by_class_name("productdivinner")

        except:
            print('ok done')
            return
        product_list = []
        print(len(items))
        for item in items:
            name = item.find_element_by_class_name("productname").text
            price = item.find_element_by_class_name("productprice").text
            imgUrl = item.find_element_by_class_name("productimg").find_element_by_tag_name("img").get_attribute("src")
            if name and price:
                print('PRODUCT: ' + name + '\t\t PRICE: ' + price + '\t\tIMG URL: ' + imgUrl)
                product_list.append({"p_cat": p_cat, "p_name": name, "p_price": price, "p_img": imgUrl})
                #product_list.append({"p_name": name})

        # self.driver.quit()
        return product_list

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
            # print('top text: ' + item.text)
            # subitems = item.find_elements_by_tag_name("ul")
            # print('subitems len:' + str(len(subitems)))
        finally:
            print('ok done with crawling')
        generatedUrls = []

        for item in items:
            name = item.find_element_by_xpath("..").find_element_by_xpath("..").find_element_by_tag_name('span').text
            subitems = item.find_elements_by_tag_name("ul")
            print('ITEM NAME: ' + name + ' ; TOTAL SUBITEMS:' + str(len(subitems)))
            for subitem in subitems:
                subitem_name = subitem.find_element_by_xpath("..").find_element_by_tag_name(
                    'h6').find_element_by_tag_name('a').get_attribute('text')
                links = subitem.find_elements_by_tag_name('li')
                print('SUBITEM NAME:' + subitem_name + ' ; TOTAL LINKS:' + str(len(links)))
                # print('')
                for link in links:
                    a = link.find_element_by_tag_name('a')
                    link_name = a.get_attribute("text")
                    link_url = a.get_attribute("href")
                    # print('LINK NAME: ' + link_name + '; LINK: ' + link_url)
                    generatedUrls.append({'linkName': link_name, 'linkUrl': link_url})

        return generatedUrls

    def close(self):
        self.driver.close()


def get_metro_data(sub_array, thread_no):
    print('Thread ' + str(thread_no) + ' Started')
    time.sleep(1)
    sub_crawler = Crawler()
    for link in sub_array:
        print("THREAD: " + str(thread_no) + ' | ' + link["linkName"] + ' | ' + link["linkUrl"])
        collective_list[thread_no].append(sub_crawler.scrape(link["linkUrl"], link['linkName']))


def split_link_array(total_splits, all_links):
    print('splitting the link array')
    array_len = len(all_links)  # 10
    split_len = array_len // total_splits  # 3
    for i in range(total_splits + 1):
        print('==============SPLIT ' + str(i) + ' ==============')
        split = all_links[split_len * i: split_len * (i + 1)]
        print_links(split)
        print('============================')
        # get_metro_data(split)
        # create the threads
        t = threading.Thread(target=get_metro_data, args=(split, i))
        time.sleep(1)
        thread_list.append(t)
        collective_list.append([])
        t.start()


def print_links(a_links):
    for link in a_links:
        print(link["linkName"] + ' | ' + link["linkUrl"])


# the list the crawlers contributed to
def print_final_list(combined_list):
    with open('products.csv', 'w') as f:
        f.write('Category;Name;Price;ImageUrl\n')
        for i in range(crawler_number):
            for category in combined_list[i]:
                if category is not None:
                    for product in category:
                        print(product["p_cat"] + ' | ' + product["p_name"] + ' | ' + product["p_price"] + ' | ' + product["p_img"])
                        f.write(product["p_cat"] + ';' + product["p_name"] + ';' + product["p_price"] + ';' + product["p_img"] + '\n')


collective_list = []
thread_list = []
crawler_number = 2

# get links
metroCrawler = Crawler()
links = metroCrawler.crawl()
#links = links[0:3]
print_links(links)
metroCrawler.close()

split_link_array(crawler_number, links)

for t in thread_list:
    t.join()

print(collective_list)
print_final_list(collective_list)
print('Test completed!')

#
# for i in range(5):
#     ting = [{'name': 'baby', 'id': i*i}, {'name': 'shmurda', 'id': i*i*i} ]
#     #tester.append([])
#     tester.append(ting)
#
# print(tester)

#
# print ('-------------------FINISHED------------------')
# print (collective_list)


# t = threading.Thread(target=get_metro_data, args=(links[0:3], 0))
# collective_list.append([])
# t2 = threading.Thread(target=get_metro_data, args=(links[3:7], 1))
#
# t.start()
# time.sleep(1)
# t2.start()
#
# t.join()
# t2.join()

# metroCrawler2 = Crawler("https://metro-online.pk/store/frozen-food/frozen-ready-to-cook/parathas")
# #first 5
# for i in range(6):
#     print(links[i]["linkName"] + ' | ' + links[i]["linkUrl"])
#     metroCrawler.scrape(links[i]["linkUrl"])
#
# #next 5
# for i in range(6,11):
#     print(links[i]["linkName"] + ' | ' + links[i]["linkUrl"])
#     metroCrawler2.scrape(links[i]["linkUrl"])

#


# for link in links:
#     print(link["linkName"] + ' | ' + link["linkUrl"])
#     metroCrawler.scrape(link["linkUrl"])


# def test_logic():
#     driver = webdriver.Chrome('chromedriver.exe')
#     url = 'https://metro-online.pk/'
#     driver.get(url)
#     # Implement your test logic
#     time.sleep(2)
#     driver.quit()
#
# N = 5   # Number of browsers to spawn
# thread_list = list()
#
# # Start test
# for i in range(N):
#     t = Thread(name='Test {}'.format(i), target=test_logic)
#     t.start()
#     time.sleep(1)
#     print (t.name + ' started!')
#     thread_list.append(t)
#
# # Wait for all thre<ads to complete
# for thread in thread_list:
#     thread.join()


# TODO
# write to csv
