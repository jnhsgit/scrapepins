import os
import time
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import Playwright, sync_playwright
from tqdm import tqdm

# Things we need to do:
# 1) Exclude the tiny icon images in the results
# 2) Figure out a way to specify how many images we want, then get PlayWright
# to scroll down the page to load more images before or while we grab their
# img tags
# 3) Figure out a way to sequentially name files, eg: [user_input_text]_1.jpg,
# [user_input_text]_2.jpg, etc

user_input_text = input("Enter your image selection: ")
folder_name = user_input_text.replace(" ", "_")
# We replace the spaces with "%20" for the URL
user_input_transformed = user_input_text.replace(" ", "%20")
url = f"https://www.pinterest.com.au/search/pins/?q={user_input_transformed}"

folder = f"{folder_name}"
if not os.path.exists(f"{folder_name}"):
    print(f"{folder_name} folder has been created. Your images will be stored here.")
    os.makedirs(f"{folder_name}")

def extract_alt_text(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    img_tags = soup.find_all("img", src=True)
    img_srcs = [img.get("src", "") for img in img_tags]
    # This line gets us the high resolution images
    img_srcs = [sub.replace("236x", "736x") for sub in img_srcs]
    return img_srcs


def run(playwright: Playwright) -> None:
    print("Opening Pinterest...")
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto(url)
    page.wait_for_load_state()
    # add a sleeper to give the page more time to load since
    # page.wait_for_load_state() doesn't seem to be sufficient
    # sometimes.
    time.sleep(5)
    content = page.content()
    img_srcs = extract_alt_text(content)
    print("Image URL's extracted.")
    context.close()
    browser.close()
    return img_srcs


with sync_playwright() as playwright:
    img_srcs = run(playwright)
print("Downloading images...")
for img in tqdm(img_srcs):
    r = requests.get(img)
    filename = img.split("/")[-1]
    filepath = os.path.join(folder, filename)
    with open(filepath, "wb") as file:
        file.write(r.content)

print(f"{user_input_text} images have been downloaded.")
