import logging

from linkedin_scraper import LinkedInScraper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    scraper = LinkedInScraper()

    # 1. Find the geocode for a location
    locations = scraper.search_locations("San Francisco")
    geocode = locations["data"][0]["id"]
    logger.info("Geocode for San Francisco: %s", geocode)

    # 2. Search for remote software engineering jobs
    jobs = scraper.search_jobs(
        keyword="Software Engineer",
        geocode=geocode,
        remote="remote",
        job_type="full_time",
        experience_level="mid_senior",
        sort_by="recent",
    )
    logger.info("Found %d jobs", len(jobs["data"]))

    for job in jobs["data"][:3]:
        print(f"\n{'─' * 60}")
        print(f"Title:    {job['title']}")
        print(f"Company:  {job['company']['name']}")
        print(f"Location: {job['location']}")
        print(f"URL:      {job['url']}")

        # 3. Get full details for each job
        detail = scraper.get_job_detail(job["id"], include_skills=True)
        data = detail["data"]
        salary = data.get("salary", {})
        if salary.get("salary_exists"):
            print(f"Salary:   {salary['min_salary']}-{salary['max_salary']} {salary['currency']}/{salary['pay_period']}")
        skills = data.get("skills", [])
        if skills:
            print(f"Skills:   {', '.join(s['name'] for s in skills[:5])}")

    # 4. Look up a company profile
    print(f"\n{'═' * 60}")
    company = scraper.get_company_profile(company="google")
    c = company["data"]
    print(f"\nCompany:  {c['name']}")
    print(f"Industry: {', '.join(c.get('industries', []))}")
    print(f"Staff:    {c.get('staff_count', 'N/A')}")

    # 5. Search for people
    print(f"\n{'═' * 60}")
    people = scraper.search_people("Sundar", current_company="1441", title="CEO")
    for person in people["data"][:3]:
        print(f"\n{person['name']} — {person.get('headline', '')}")


if __name__ == "__main__":
    main()
