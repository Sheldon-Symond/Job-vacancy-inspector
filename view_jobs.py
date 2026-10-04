import sqlite3

connection = sqlite3.connect("jobs.db")

cursor = connection.cursor()

cursor.execute("""
SELECT
    job_id,
    title,
    company,
    location,
    salary_min,
    salary_max,
    experience_months,
    status,
    url
FROM jobs
ORDER BY id DESC
""")

jobs = cursor.fetchall()

print("\n========== SAVED JOBS ==========")
print("Total jobs:", len(jobs))

for number, job in enumerate(jobs, start=1):

    print("\n-----------------------------")

    print("Job", number)
    print("Title:", job[1])
    print("Company:", job[2])
    print("Location:", job[3])
    print("Experience:", job[6], "months")
    print("Salary:", job[4], "-", job[5])
    print("Status:", job[7])
    print("URL:", job[8])

connection.close()