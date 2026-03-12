import requests
import re


def clean_html(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text).strip()


def scrape_linkedin_jobs(keyword):

    keyword = keyword.replace(" ", "%20")

    url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={keyword}&location=India"

    response = requests.get(url)

    jobs = []

    if response.status_code != 200:
        return jobs

    html = response.text

    cards = html.split('base-card')

    for card in cards:

        # -------------------
        # Job Title
        # -------------------
        try:
            title = card.split('base-search-card__title">')[1].split("</")[0]
            title = clean_html(title)
        except:
            continue

        # -------------------
        # Company Name
        # -------------------
        try:
            company = card.split('base-search-card__subtitle">')[1].split("</")[0]
            company = clean_html(company)
        except:
            company = "Unknown Company"

        # -------------------
        # Location
        # -------------------
        try:
            location = card.split('job-search-card__location">')[1].split("</")[0]
            location = clean_html(location)
        except:
            location = "India"

        # -------------------
        # Job URL
        # -------------------
        try:
            link = card.split('href="')[1].split('"')[0]
        except:
            link = "#"

        # -------------------
        # Description
        # -------------------
        description = f"{title} role at {company} located in {location}. This role requires relevant technical skills and industry knowledge."

        jobs.append({
            "title": title,
            "company": company,
            "location": location,
            "description": description,
            "url": link
        })

        # Limit to 5 jobs
        if len(jobs) >= 5:
            break

    return jobs