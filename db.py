import csv
import os
import time

from job import Job

db_berlinstartupjobs = {}
db_weworkremotely = {}
db_web3 = {}
db_wanted = {}


def search_file():
    file_list = []
    os.chdir("C:/Users/kdoub/Desktop/coding/Python/Job_Scraper/file")
    files = os.listdir()
    for file in files:
        file_name = os.path.splitext(file)[0]
        keyword, site = file_name.split("_")
        modification_time = time.localtime(os.path.getmtime(file))
        modification_time = time.strftime("%Y-%m-%d %H:%M:%S", modification_time)
        file_list.append([keyword, site, modification_time])
    return file_list


def get_from_db():
    os.chdir("C:/Users/kdoub/Desktop/coding/Python/Job_Scraper/file")
    files = os.listdir()
    for file in files:
        filename = os.path.splitext(file)[0]
        keyword, site = filename.split("_")
        read_from_file(keyword, site)


def put_data_from_csv(reader):
    jobs = []

    for row in reader:
        title, company, description, link = row
        if title == "Title":
            continue
        jobs.append(Job(title, company, description, link))
    return jobs


def read_from_file(keyword, site):
    jobs = []

    file = open(
        f"{keyword}_{site}.csv",
        "r",
        encoding="UTF-8",
        newline="",
    )
    reader = csv.reader(file)

    if site == "berlinstartupjobs":
        db_berlinstartupjobs[keyword] = put_data_from_csv(reader)

    elif site == "weworkremotely":
        db_weworkremotely[keyword] = put_data_from_csv(reader)

    elif site == "web3":
        db_web3[keyword] = put_data_from_csv(reader)

    elif site == "wanted":
        db_wanted[keyword] = put_data_from_csv(reader)
