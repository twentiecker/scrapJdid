from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

url = "https://www.jd.id/map/sitemap.html"
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get(f"{url}")
time.sleep(2)  # Allow 2 seconds for the web page to open
page_soup = BeautifulSoup(driver.page_source, "html.parser")
driver.close()

# Get content category
content_soup = page_soup.find_all("div", {"class": "map-item"})
print(len(content_soup))

# Scraping category by level
list_category = []
for w in content_soup:
    level1_tag = w.find("div", {"class": "mt"})
    print(level1_tag.text)
    list_category.append(level1_tag.text)
    level2_tag = w.find_all("dl")
    for x in level2_tag:
        y = x.find("dt")
        print(f";{y.text}")
        list_category.append(f";{y.text}")
        level3_tag = x.find_all("dd")
        for z in level3_tag:
            print(f";;{z.text}")
            list_category.append(f";;{z.text}")

# Write scraped data to a csv file (semicolon separated)
f = open(f"jdid_kategori.csv", "w+", encoding="utf-8")  # open/create file and then append some item (a+)
headers = "Level 1;Level 2;Level 3\n"
f.write(headers)
for i in range(len(list_category)):
    f.write(f"{list_category[i]}\n")
f.close()
