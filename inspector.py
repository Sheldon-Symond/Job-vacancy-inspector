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

for i, block in enumerate(json_ld, start=1):
    try:
        data = json.loads(block.string)
        print(f"JSON-LD {i} type:", data.get("@type"))
    except Exception:
        print(f"JSON-LD {i}: Could not parse")

keywords = [
    "customer service",
    "job",
    "salary",
    "experience",
    "Mumbai"
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