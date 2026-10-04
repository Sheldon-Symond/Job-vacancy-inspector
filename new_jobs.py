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
    url
FROM jobs
WHERE status = 'NEW'
ORDER BY id DESC
""")

jobs = cursor.fetchall()

print("\n========== NEW JOBS ==========")
print("Jobs requiring action:", len(jobs))

for number, job in enumerate(jobs, start=1):

    print("\n-----------------------------")

    print("Job", number)
    print("Title:", job[1])
    print("Company:", job[2])
    print("Location:", job[3])
    print("Experience:", job[6], "months")
    print("Salary:", job[4], "-", job[5])
    print("Job ID:", job[0])
    print("URL:", job[7])

connection.close()