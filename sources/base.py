class JobSource:

    def get_search_page(self, url):
        raise NotImplementedError

    def find_vacancy_links(self, soup):
        raise NotImplementedError

    def fetch_and_extract_job(self, url):
        raise NotImplementedError