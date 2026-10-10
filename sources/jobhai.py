import json
import requests
from bs4 import BeautifulSoup
from sources.base import JobSource

def get_search_page(url):
    response = requests.get(url)
    return response

def find_vacancy_links(soup):

    links = soup.find_all("a")

    vacancy_links = []

    for link in links:

        href = link.get("href")

        if href and "jid" in href.lower():

            if href.startswith("/"):
                href = "https://www.jobhai.com" + href

            if href not in vacancy_links:
                vacancy_links.append(href)

    return vacancy_links

def fetch_and_extract_job(url):

    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch: {url}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    json_ld = soup.find_all("script", type="application/ld+json")

    for block in json_ld:

        try:

            data = json.loads(block.string)

            if data.get("@type") == "JobPosting":

                print("JobPosting found")

                job = {
                "title": data.get("title"),
                "description": data.get("description"),
                "date_posted": data.get("datePosted"),
                "valid_through": data.get("validThrough"),
                "employment_type": (data.get("employmentType")[0]
                if isinstance(data.get("employmentType"), list)
                else data.get("employmentType")),
                "company": data.get("hiringOrganization", {}).get("name"),
                "job_id": data.get("identifier", {}).get("value"),
                "location": (data.get("jobLocation", {}).get("address", {}).get("addressLocality", "")+ ", "
                + data.get("jobLocation", {}).get("address", {}).get("addressRegion", "")),
                "address": data.get("jobLocation", {}).get("address", {}).get("streetAddress"),
                "salary_min": data.get("baseSalary", {}).get("value", {}).get("minValue"),
                "salary_max": data.get("baseSalary", {}).get("value", {}).get("maxValue"),
                "salary_currency": data.get("baseSalary", {}).get("currency"),
                "salary_period": data.get("baseSalary", {}).get("value", {}).get("unitText"),
                "experience_months": None,
                "industry": None,
                "category": None,
                "direct_apply": data.get("directApply"),
                "url": url,
                }

            return job

        except Exception:
            continue

    return None

class JobHaiSource(JobSource):

    def get_search_page(self, url):
        return get_search_page(url)

    def find_vacancy_links(self, soup):
        return find_vacancy_links(soup)

    def fetch_and_extract_job(self, url):
        return fetch_and_extract_job(url)
