import requests
from bs4 import BeautifulSoup
import json
url = input("Enter the URL to inspect: ")
response = requests.get(url)
print("'\nJob secure inspector")
print("URL: ", url)
print("Status Code: ", response.status_code)
print("Final URL: ", response.url)
print("Content Type: ", response.headers.get('Content-Type'))
print("Response Size:", len(response.text), "characters")

start = response.text.find("<title>")
end = response.text.find("</title>")

if start != -1 and end != -1:
    title = response.text[start + 7:end]
    print("Page Title:", title)
else:
    print("Page Title: Not found") 

soup = BeautifulSoup(response.text, "html.parser")

print("Number of links:", len(soup.find_all("a")))
print("Number of headings:", len(soup.find_all(["h1", "h2", "h3"])))
print("Number of forms:", len(soup.find_all("form")))
print("Number of scripts:", len(soup.find_all("script")))

json_ld = soup.find_all("script", type="application/ld+json")

print("JSON-LD blocks:", len(json_ld))

job = None

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
    except Exception:
        print(f"JSON-LD {i}: Could not parse")

print("\nClean Job Record:")

if job:
    for key, value in job.items():
        print(f"{key}: {value}")
else:
    print("No JobPosting data found.")

keywords = [
    "customer service",
    "job",
    "salary",
    "experience",
    "Mumbai",
    "Work from home",
]

print("\nKeyword inspection:")

for keyword in keywords:
    count = response.text.lower().count(keyword.lower())
    print(f"{keyword}: {count}")


print("\nFirst 30 links:")

links = soup.find_all("a")

for i, link in enumerate(links[:30], start=1):
    text = link.get_text(" ", strip=True)
    href = link.get("href")

    print(f"{i}. TEXT: {text[:80]}")
    print(f"   URL: {href}")

print("\nVacancy links found:")

vacancy_links = []

for link in links:
    href = link.get("href")

    if href and href.startswith("/job/"):
        full_url = "https://apna.co" + href

        if full_url not in vacancy_links:
            vacancy_links.append(full_url)

for i, vacancy_url in enumerate(vacancy_links, start=1):
    print(f"{i}. {vacancy_url}")

print("Total vacancy links:", len(vacancy_links))