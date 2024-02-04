import requests
from bs4 import BeautifulSoup
from job import Job


def scrape_berlinstartupjobs(keyword):
    response = requests.get(
        f"https://berlinstartupjobs.com/skill-areas/{keyword}/",
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        },
    )

    soup = BeautifulSoup(response.text, "html.parser")

    jobs = soup.find_all("li", class_="bjs-jlid")

    result = []

    for job in jobs:
        title = job.find("h4", class_="bjs-jlid__h").find("a").text
        company_name = job.find("a", class_="bjs-jlid__b").text
        description = job.find("div", class_="bjs-jlid__description").text
        url = job.find("h4", class_="bjs-jlid__h").find("a")["href"]

        job = Job(title, company_name, description, url)

        result.append(job)

    return result


def scrape_weworkremotely(keyword):
    response = requests.get(
        f"https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term={keyword}"
    )

    soup = BeautifulSoup(response.content, "html.parser")

    jobss = soup.find_all("section", class_="jobs")

    result = []

    for jobs in jobss:
        jobs = jobs.find_all("li")[:-1]
        for job in jobs:
            title = job.find("span", class_="title").text
            company, position, region = job.find_all("span", class_="company")
            company = company.text
            position = position.text
            region = region.text
            description = f"Region: {region}\nPosition: {position}"
            url = job.find("div", class_="tooltip").next_sibling["href"]
            url = f"https://weworkremotely.com{url}"

            job = Job(title, company, description, url)

            result.append(job)

    return result


def scrape_web3(keyword):
    response = requests.get(
        f"https://web3.career/{keyword}-jobs",
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        },
    )

    soup = BeautifulSoup(response.text, "html.parser")

    jobs = soup.find_all("tr", class_="table_row")

    result = []

    for job in jobs:
        title = job.find("h2", class_="my-primary")
        company_and_location = job.find_all("td", class_="job-location-mobile")
        url = job.find("a")["href"]

        if title == None or company_and_location == [] or url == None:
            continue

        title = title.text
        company_name = company_and_location[0].find("h3").text
        locations = company_and_location[1].find_all("a")
        location = ""
        for l in locations:
            location = f"{l.text} {location}"
        if location == "":
            location = "Remote"
        description = f"Location: {location}"
        url = f"https://web3.career{url}"

        job = Job(title, company_name, description, url)

        result.append(job)

    return result
