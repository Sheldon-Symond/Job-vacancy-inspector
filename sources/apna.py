import json
import requests
from bs4 import BeautifulSoup


def extract_job(soup):

    json_ld = soup.find_all("script", type="application/ld+json")

    print("JSON-LD blocks:", len(json_ld))

    for i, block in enumerate(json_ld, start=1):

        try:
            data = json.loads(block.string)

            print(f"\nJSON-LD {i} type:", data.get("@type"))

            if data.get("@type") == "JobPosting":

                job = {
                    "title": data.get("title"),
                    "description": data.get("description"),
                    "date_posted": data.get("datePosted"),
                    "valid_through": data.get("validThrough"),
                    "employment_type": data.get("employmentType"),
                    "company": data.get("hiringOrganization", {}).get("name"),
                    "job_id": data.get("identifier", {}).get("value"),
                    "location": data.get("jobLocation", {}).get("address", {}).get("addressLocality"),
                    "address": data.get("jobLocation", {}).get("address", {}).get("streetAddress"),
                    "salary_min": data.get("baseSalary", {}).get("value", {}).get("minValue"),
                    "salary_max": data.get("baseSalary", {}).get("value", {}).get("maxValue"),
                    "salary_currency": data.get("baseSalary", {}).get("currency"),
                    "salary_period": data.get("baseSalary", {}).get("value", {}).get("unitText"),
                    "experience_months": data.get("experienceRequirements", {}).get("monthsOfExperience"),
                    "industry": data.get("industry"),
                    "category": data.get("occupationalCategory"),
                    "direct_apply": data.get("directApply"),
                    "url": data.get("url"),
                }

                return job

        except Exception:
            print(f"JSON-LD {i}: Could not parse")

    return None


def find_vacancy_links(soup):

    links = soup.find_all("a")
    vacancy_links = []

    for link in links:

        href = link.get("href")

        if href and href.startswith("/job/"):

            full_url = "https://apna.co" + href

            if full_url not in vacancy_links:
                vacancy_links.append(full_url)

    return vacancy_links


def fetch_and_extract_job(url):

    response = requests.get(url)

    if response.status_code != 200:

        print(f"Failed to fetch: {url}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    job = extract_job(soup)

    if job:
        job["url"] = url

    return job