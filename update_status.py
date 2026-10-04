import sqlite3

allowed_statuses = [
    "NEW",
    "APPLIED",
    "INTERVIEW",
    "SELECTED",
    "REJECTED"
]

job_id = input("Enter Job ID: ")
new_status = input("Enter new status: ").upper()

if new_status not in allowed_statuses:

    print("Invalid status.")
    print("Allowed statuses:", ", ".join(allowed_statuses))

else:

    connection = sqlite3.connect("jobs.db")

    cursor = connection.cursor()

    cursor.execute("""
    UPDATE jobs
    SET status = ?
    WHERE job_id = ?
    """, (new_status, job_id))

    connection.commit()

    if cursor.rowcount > 0:
        print("Status updated successfully.")
    else:
        print("Job ID not found.")

    connection.close()