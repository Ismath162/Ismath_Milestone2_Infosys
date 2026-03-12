import csv
import mysql.connector


# ----------------------------
# MYSQL CONNECTION
# ----------------------------
def create_mysql_connection():

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="career_platform"
    )

    return conn


# ----------------------------
# STORE JOBS IN CSV
# ----------------------------
def store_jobs_csv(jobs):

    file_name = "scraped_jobs.csv"

    try:
        file = open(file_name, "x")
        file.close()
        new_file = True
    except:
        new_file = False


    with open(file_name, "a", newline="", encoding="utf-8") as f:

        fieldnames = ["title","company","location","description","url","role"]

        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if new_file:
            writer.writeheader()

        for job in jobs:
            writer.writerow(job)


# ----------------------------
# STORE JOBS IN MYSQL
# ----------------------------
def store_jobs_mysql(jobs):

    conn = create_mysql_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO jobs (title, company, location, description, url, role)
    VALUES (%s,%s,%s,%s,%s,%s)
    """

    for job in jobs:

        cursor.execute(query, (
            job["title"],
            job["company"],
            job["location"],
            job["description"],
            job["url"],
            job["role"]
        ))

    conn.commit()

    cursor.close()
    conn.close()