import csv
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
my_url = 'https://www.newegg.com/global/ph-en/Processors-Desktops/SubCategory/ID-343?Tid=1544852'

csvFilename = "output.csv"

# OPEN CONNECTION GRAB PAGE
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

# THIS WILL PARSE THE GIVEN HTML URL
page_soup = soup(page_html, "html.parser")

# SAMPLE OUTPUT OF h1
# page_soup.h1
# <h1 class="page-title-text">Processors - Desktops</h1>

# CONTAINERS WILL CONTAIN ALL ITEMS IN A CONTAINER CLASS FROM HTML
containers = page_soup.findAll("div", {"class":"item-container"})

with open(csvFilename, 'w', newline='', encoding="utf-8") as file:
    writer = csv.writer(file, delimiter='|')
    writer.writerow(["BRAND","PRODUCT_NAME","OLD_PRICE","NEW_PRICE"])

    for container in containers:
        # BRAND NAME
        brand = container.div.a.img["title"]

        # PRODUCT NAME 
        title_container = container.findAll("a", {"class":"item-title"})
        # STRIP LIKE TRIM in VB
        product_name = title_container[0].text.strip()

        # PRICE
        price_container = container.findAll("ul", {"class":"price"})
        price_before = price_container[0].li

        if len(price_before) > 0:
            price_before = price_container[0].li.span.text
        else:
            price_before = ""

        # CURRENT PRICE
        price_current_container = price_container[0].findAll("li", {"class":"price-current"})
        price_now = price_current_container[0].text

        writer.writerow([brand,product_name,price_before,price_now])

        # print("brand: " + brand)
        # print("name: " + product_name)
        # print("old price: " + price_before)
        # print("new price: " + price_now)
        # print("---")
        # print(" ")

print("Done!")