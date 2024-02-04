class Job:
    def __init__(self, title, company_name, description, link):
        self.title = title
        self.company = company_name
        self.description = description
        self.url = link


class Jobs:
    def __init__(self, keyword):
        self.keyword = keyword
        self.jobs = []

    def get_content(self, scrape_function):
        self.jobs = scrape_function(self.keyword)

    # def make_csv(self):
    #     save_to_file(self.keyword, self.jobs)
