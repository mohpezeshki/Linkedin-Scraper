import logging
from pprint import pprint

from linkedin_scraper import LinkedInScraper


logger = logging.getLogger(__name__)




if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    scraper = LinkedInScraper()

    result = scraper.search_jobs("Software Engineer", geocode="103644278")
    for job in result["data"]:
        pprint(job)
        break

    detail = scraper.get_job_detail("4413763968", include_skills=True)
    pprint(detail["data"]["title"])
