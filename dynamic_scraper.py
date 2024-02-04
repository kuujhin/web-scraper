from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
from job import Job


def scrape_wanted(keyword):
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto(f"https://www.wanted.co.kr/search?query={keyword}&tab=position")
    time.sleep(3)

    for _ in range(5):
        page.keyboard.down("End")
        time.sleep(2)

    soup = BeautifulSoup(page.content(), "html.parser")

    p.stop()

    jobs = soup.find_all("div", class_="JobCard_container__FqChn")

    result = []

    for job in jobs:
        link = f"https://www.wanted.co.kr{job.find('a')['href']}"
        title = job.find("strong", class_="JobCard_title__ddkwM").text
        company_name = job.find("span", class_="JobCard_companyName__vZMqJ").text
        location = job.find("span", class_="JobCard_location__2EOr5").text
        reward = job.find("span", class_="JobCard_reward__sdyHn").text

        description = f"Location: {location}\nReward: {reward}"
        job = Job(title, company_name, description, link)

        result.append(job)

    return result
