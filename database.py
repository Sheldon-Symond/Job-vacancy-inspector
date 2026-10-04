import sqlite3

connection = sqlite3.connect("jobs.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS jobs (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    source TEXT NOT NULL,
    job_id TEXT NOT NULL,

    title TEXT,
    description TEXT,
    company TEXT,

    location TEXT,
    address TEXT,

    salary_min REAL,
    salary_max REAL,
    salary_currency TEXT,
    salary_period TEXT,

    experience_months INTEGER,

    employment_type TEXT,
    industry TEXT,
    category TEXT,

    direct_apply BOOLEAN,

    url TEXT,

    date_posted TEXT,
    valid_through TEXT,

    date_found TEXT,

    status TEXT DEFAULT 'NEW',

    UNIQUE(source, job_id)
)
""")

connection.commit()

connection.close()

print("Database created successfully.")