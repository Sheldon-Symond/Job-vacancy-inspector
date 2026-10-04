import requests
from bs4 import BeautifulSoup
import json
import sqlite3
from config import SEARCH_CONFIG

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

def save_job(job):
    
    if job is None:
        return

    connection = sqlite3.connect("jobs.db")

    cursor = connection.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO jobs (
        source,
        job_id,
        title,
        description,
        company,
        location,
        address,
        salary_min,
        salary_max,
        salary_currency,
        salary_period,
        experience_months,
        employment_type,
        industry,
        category,
        direct_apply,
        url,
        date_posted,
        valid_through,
        date_found,
        status
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "Apna",
        job.get("job_id"),
        job.get("title"),
        job.get("description"),
        job.get("company"),
        job.get("location"),
        job.get("address"),
        job.get("salary_min"),
        job.get("salary_max"),
        job.get("salary_currency"),
        job.get("salary_period"),
        job.get("experience_months"),
        job.get("employment_type"),
        job.get("industry"),
        job.get("category"),
        job.get("direct_apply"),
        job.get("url"),
        job.get("date_posted"),
        job.get("valid_through"),
        None,
        "NEW"
    ))

    connection.commit()

    connection.close()

def job_matches_keywords(job):

    text = " ".join([
        job.get("title") or "",
        job.get("description") or "",
        job.get("industry") or "",
        job.get("category") or ""
    ]).lower()

    required_keywords = SEARCH_CONFIG["required_keywords"]
    excluded_keywords = SEARCH_CONFIG["excluded_keywords"]

    required_match = any(
        keyword.lower() in text
        for keyword in required_keywords
    )

    excluded_match = any(
        keyword.lower() in text
        for keyword in excluded_keywords
    )

    return required_match and not excluded_match

# -----------------------------------
# MAIN PROGRAM
# -----------------------------------

url = input("Enter the URL to inspect: ")

response = requests.get(url)

print("\nJob Vacancy Inspector")
print("URL:", url)
print("Status Code:", response.status_code)
print("Final URL:", response.url)
print("Content Type:", response.headers.get("Content-Type"))
print("Response Size:", len(response.text), "characters")


soup = BeautifulSoup(response.text, "html.parser")


print("\nPage information:")
print("Number of links:", len(soup.find_all("a")))
print("Number of headings:", len(soup.find_all(["h1", "h2", "h3"])))
print("Number of forms:", len(soup.find_all("form")))
print("Number of scripts:", len(soup.find_all("script")))


# Find vacancy links from search page

vacancy_links = find_vacancy_links(soup)


print("\nVacancy links found:")

# Process all vacancy links

# Process all vacancy links

for i, vacancy_url in enumerate(vacancy_links, start=1):

    print(f"\nProcessing vacancy {i} of {len(vacancy_links)}")

    job = fetch_and_extract_job(vacancy_url)

    if job:

        location = job.get("location")
        experience = job.get("experience_months")
        salary_min = job.get("salary_min")
        salary_max = job.get("salary_max")
        salary_currency = job.get("salary_currency")
        salary_period = job.get("salary_period")

        if location and any(
            city.lower() in location.lower()
            for city in SEARCH_CONFIG["locations"]
        ) and job_matches_keywords(job):

            print("MATCH")
            print("Title:", job.get("title"))
            print("Company:", job.get("company"))
            print("Location:", location)
            print("Experience:", experience, "months")
            print("Salary:", salary_min, "-", salary_max, salary_currency, salary_period)
            print("Job ID:", job.get("job_id"))
            print("URL:", job.get("url"))

            save_job(job)

        else:

            print("SKIP - Does not match filters")

    else:

        print("FETCH/EXTRACTION FAILED")
            