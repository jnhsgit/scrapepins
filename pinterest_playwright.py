import time

import requests
from bs4 import BeautifulSoup
from playwright.sync_api import Playwright, sync_playwright

#Things we need to do:
#1) Figure out how to take user input to search for images
#2) Create a folder based off the image search, eg: 'red_car'
#3) Create filenames based off the image search, eg: 'red_car_1.jpg'
#4) Store the files in the folder
def extract_alt_text(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    img_tags = soup.find_all("img", src=True)
    alt_texts = [img.get("src", "") for img in img_tags]
    #This line gets us the high resolution images
    alt_texts = [sub.replace("236x", "736x") for sub in alt_texts]
    return alt_texts


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto(
        "https://www.pinterest.com.au/search/pins/?q=2%20tier%20wedding%20cake%20blue"
    )
    page.wait_for_load_state()
    time.sleep(5)
    content = page.content()
    alt_texts = extract_alt_text(content)
    context.close()
    browser.close()
    return alt_texts


with sync_playwright() as playwright:
    alt_texts = run(playwright)

for img in alt_texts:
    r = requests.get(img)
    filename = img.split("/")[-1]
    with open(filename, "wb") as file:
        file.write(r.content)
