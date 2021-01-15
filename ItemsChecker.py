import time

import bs4
from pip._vendor import requests

from MailSender import sendMail

time_to_wait_between_checks = 5
list_of_items = [
    {
        "link": "https://www.newegg.ca/gigabyte-geforce-rtx-3060-ti-gv-n306tgaming-oc-8gd/p/N82E16814932377"
                "?Description=rtx%203060&cm_re=rtx_3060-_-14-932-377-_-Product",
        "divClassName": "product-inventory",
        "type": "div",
        "stringThatMustNotContain": ["OUT OF STOCK"]
    },
    {
        "link": "https://www.newegg.ca/gigabyte-geforce-rtx-3060-ti-gv-n306tgamingoc-pro-8gd/p/N82E16814932376"
                "?Description=rtx%203060&cm_re=rtx_3060-_-14-932-376-_-Product",
        "divClassName": "product-inventory",
        "type": "div",
        "stringThatMustNotContain": ["OUT OF STOCK"]
    },
    {
        "link": "https://www.newegg.ca/evga-geforce-rtx-3060-ti-08g-p5-3667-kr/p/N82E16814487537?Description=rtx"
                "%203060&cm_re=rtx_3060-_-14-487-537-_-Product",
        "divClassName": "product-inventory",
        "type": "div",
        "stringThatMustNotContain": ["OUT OF STOCK"]
    },
    {
        "link": "https://www.canadacomputers.com/product_info.php?cPath=43_557_559&item_id=185406",
        "divClassName": "pi-prod-availability",
        "type": "div",
        "stringThatMustNotContain": ["In-Store Back Order", "In-Store Out Of Stock"]
    },
    {
        "link": "https://www.canadacomputers.com/product_info.php?cPath=43_557_559&item_id=185407",
        "divClassName": "pi-prod-availability",
        "type": "div",
        "stringThatMustNotContain": ["In-Store Back Order", "In-Store Out Of Stock"]
    },
    {
        "link": "https://www.canadacomputers.com/product_info.php?cPath=43_557_559&item_id=184759",
        "divClassName": "pi-prod-availability",
        "type": "div",
        "stringThatMustNotContain": ["In-Store Back Order", "In-Store Out Of Stock"]
    },
    {
        "link": "https://www.canadacomputers.com/product_info.php?cPath=43_557_559&item_id=185408",
        "divClassName": "pi-prod-availability",
        "type": "div",
        "stringThatMustNotContain": ["In-Store Back Order", "In-Store Out Of Stock"]
    },
    {
        "link": "https://www.canadacomputers.com/product_info.php?cPath=43_557_559&item_id=184760",
        "divClassName": "pi-prod-availability",
        "type": "div",
        "stringThatMustNotContain": ["In-Store Back Order", "In-Store Out Of Stock"]
    },
    {
        "link": "https://www.canadacomputers.com/product_info.php?cPath=43_557_559&item_id=185988",
        "divClassName": "pi-prod-availability",
        "type": "div",
        "stringThatMustNotContain": ["In-Store Back Order", "In-Store Out Of Stock"]
    },

    {
        "link": "https://www.bestbuy.ca/en-ca/product/evga-geforce-rtx-3060-ti-ftw3-ultra-8gb-gddr6-video-card/15200164",
        "divClassName": "availabilityMessage_1MO75 container_3LC03",
        "type": "span",
        "stringThatMustNotContain": ["Sold out online", "Coming soon"]
    },
]


def get_page_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/83.0.4103.116 Safari/537.36"}
    try:
        page = requests.get(url, headers=headers)
    except requests.exceptions.RequestException as e:
        return None
    return page.content


def check_item(page, divClass, typeOfAttribute, stringThatMustNotContain):
    if not page:
        return True

    soup = bs4.BeautifulSoup(page, 'html.parser')
    out_of_stock_div = soup.find(typeOfAttribute, {"class": divClass})
    # print("         " + out_of_stock_div.text.replace("\n", "").replace("  ", ""))

    if not out_of_stock_div:
        return True

    if not stringThatMustNotContain:
        return out_of_stock_div != "None"

    for phrase in stringThatMustNotContain:
        if phrase in out_of_stock_div.text:
            return True

    return False


def check_inventory(link, divClassName, typeOfAttribute, stringThatMustNotContain):
    return check_item(get_page_html(link), divClassName, typeOfAttribute, stringThatMustNotContain)


counter = 0
while True:
    counter = counter + 1
    if counter % 5 == 0:
        print("Checking for the time " + str(counter))
    for item in list_of_items:
        # print("     Checking for item " + item["link"])
        if not check_inventory(item["link"], item["divClassName"], item["type"], item["stringThatMustNotContain"]):
            print("----- Item is in stock! -----" + item["link"])
            sendMail(item["link"])
            list_of_items.remove(item)
            if not list_of_items:
                exit()
    time.sleep(time_to_wait_between_checks)
