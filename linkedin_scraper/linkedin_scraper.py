
from dotenv import load_dotenv
import logging
import os
import requests
from pprint import pprint
import os
from linkedin_scraper import urls
from linkedin_scraper.validators import validate_params


load_dotenv()

class LinkedInScraper:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("RAPID_API_TOKEN")
        if not self.api_key:
            raise ValueError("RAPID_API_TOKEN not set")
        self.session = requests.Session()
        self.session.headers["X-RapidAPI-Key"] = self.api_key

    def _get(self, url, params=None):
        params = {k: v for k, v in (params or {}).items() if v is not None}
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    # ── Job ──────────────────────────────────────────────────────────────

    def search_jobs(
        self,
        keyword,
        page=None,
        sort_by=None,
        date_posted=None,
        geocode=None,
        company=None,
        experience_level=None,
        remote=None,
        job_type=None,
        easy_apply=None,
        has_verifications=None,
        under_10_applicants=None,
        fair_chance_employer=None,
        industry_ids=None,
    ):
        params = {
            "keyword": keyword,
            "page": page,
            "sort_by": sort_by,
            "date_posted": date_posted,
            "geocode": geocode,
            "company": company,
            "experience_level": experience_level,
            "remote": remote,
            "job_type": job_type,
            "easy_apply": easy_apply,
            "has_verifications": has_verifications,
            "under_10_applicants": under_10_applicants,
            "fair_chance_employer": fair_chance_employer,
            "industry_ids": industry_ids,
        }
        validate_params("search_jobs", params)
        return self._get(urls.JOB_SEARCH, params)

    def get_job_detail(self, job_id, include_skills=None):
        return self._get(urls.JOB_DETAIL, {
            "job_id": job_id,
            "include_skills": include_skills,
        })

    # ── Post ─────────────────────────────────────────────────────────────

    def get_post_detail(self, post_id):
        return self._get(urls.POST_DETAIL, {"post_id": post_id})

    def get_post_comments(self, post_id, page=None, sort_order=None, post_type=None):
        params = {
            "post_id": post_id,
            "page": page,
            "sort_order": sort_order,
            "post_type": post_type,
        }
        validate_params("get_post_comments", params)
        return self._get(urls.POST_COMMENTS, params)

    def get_post_reactions(self, post_id, page=None, type=None):
        params = {
            "post_id": post_id,
            "page": page,
            "type": type,
        }
        validate_params("get_post_reactions", params)
        return self._get(urls.POST_REACTIONS, params)

    def get_post_reposts(self, post_id, page=None, pagination_token=None):
        return self._get(urls.POST_REPOSTS, {
            "post_id": post_id,
            "page": page,
            "pagination_token": pagination_token,
        })

    # ── User Profile Data ────────────────────────────────────────────────

    def get_user_profile(
        self,
        username,
        include_follower_and_connection=None,
        include_experiences=None,
        include_skills=None,
        include_services=None,
        include_certifications=None,
        include_publications=None,
        include_honors=None,
        include_volunteers=None,
        include_educations=None,
        include_bio=None,
    ):
        return self._get(urls.USER_PROFILE, {
            "username": username,
            "include_follower_and_connection": include_follower_and_connection,
            "include_experiences": include_experiences,
            "include_skills": include_skills,
            "include_services": include_services,
            "include_certifications": include_certifications,
            "include_publications": include_publications,
            "include_honors": include_honors,
            "include_volunteers": include_volunteers,
            "include_educations": include_educations,
            "include_bio": include_bio,
        })

    def get_user_contact(self, username):
        return self._get(urls.USER_CONTACT, {"username": username})

    def get_user_posts(self, urn=None, username=None, page=None, pagination_token=None):
        return self._get(urls.USER_POSTS, {
            "urn": urn,
            "username": username,
            "page": page,
            "pagination_token": pagination_token,
        })

    def get_user_comments(self, urn=None, username=None, page=None, pagination_token=None):
        return self._get(urls.USER_COMMENTS, {
            "urn": urn,
            "username": username,
            "page": page,
            "pagination_token": pagination_token,
        })

    def get_user_videos(self, urn=None, username=None, page=None, pagination_token=None):
        return self._get(urls.USER_VIDEOS, {
            "urn": urn,
            "username": username,
            "page": page,
            "pagination_token": pagination_token,
        })

    def get_user_images(self, urn=None, username=None, page=None, pagination_token=None):
        return self._get(urls.USER_IMAGES, {
            "urn": urn,
            "username": username,
            "page": page,
            "pagination_token": pagination_token,
        })

    def get_user_reactions(self, urn=None, username=None, page=None, pagination_token=None):
        return self._get(urls.USER_REACTIONS, {
            "urn": urn,
            "username": username,
            "page": page,
            "pagination_token": pagination_token,
        })

    def get_user_documents(self, username, page=None, pagination_token=None):
        return self._get(urls.USER_DOCUMENTS, {
            "username": username,
            "page": page,
            "pagination_token": pagination_token,
        })

    def get_user_recommendations(self, urn=None, username=None, page=None, type=None):
        params = {
            "urn": urn,
            "username": username,
            "page": page,
            "type": type,
        }
        validate_params("get_user_recommendations", params)
        return self._get(urls.USER_RECOMMENDATIONS, params)

    def save_user_profile_to_pdf(self, username):
        return self._get(urls.USER_SAVE_TO_PDF, {"username": username})

    # ── User Additional Data ─────────────────────────────────────────────

    def get_user_about(self, urn=None, username=None, page=None):
        return self._get(urls.USER_ABOUT, {
            "urn": urn,
            "username": username,
            "page": page,
        })

    def get_user_skills(self, urn=None, username=None, page=None):
        return self._get(urls.USER_SKILLS, {
            "urn": urn,
            "username": username,
            "page": page,
        })

    def get_user_educations(self, urn=None, username=None, page=None):
        return self._get(urls.USER_EDUCATIONS, {
            "urn": urn,
            "username": username,
            "page": page,
        })

    def get_user_certifications(self, urn=None, username=None, page=None):
        return self._get(urls.USER_CERTIFICATIONS, {
            "urn": urn,
            "username": username,
            "page": page,
        })

    def get_user_publications(self, urn=None, username=None, page=None):
        return self._get(urls.USER_PUBLICATIONS, {
            "urn": urn,
            "username": username,
            "page": page,
        })

    def get_user_honors(self, urn=None, username=None, page=None):
        return self._get(urls.USER_HONORS, {
            "urn": urn,
            "username": username,
            "page": page,
        })

    def get_user_experience(self, urn=None, username=None, page=None):
        return self._get(urls.USER_EXPERIENCE, {
            "urn": urn,
            "username": username,
            "page": page,
        })

    def get_user_volunteers(self, urn=None, username=None, page=None):
        return self._get(urls.USER_VOLUNTEERS, {
            "urn": urn,
            "username": username,
            "page": page,
        })

    def get_user_follower_and_connection(self, username):
        return self._get(urls.USER_FOLLOWER_AND_CONNECTION, {"username": username})

    # ── User Interests ───────────────────────────────────────────────────

    def get_user_interest_companies(self, urn=None, username=None, page=None, pagination_token=None):
        return self._get(urls.USER_INTERESTS_COMPANIES, {
            "urn": urn,
            "username": username,
            "page": page,
            "pagination_token": pagination_token,
        })

    def get_user_interest_groups(self, urn=None, username=None, page=None, pagination_token=None):
        return self._get(urls.USER_INTERESTS_GROUPS, {
            "urn": urn,
            "username": username,
            "page": page,
            "pagination_token": pagination_token,
        })

    def get_user_interest_top_voices(self, urn=None, username=None, page=None, pagination_token=None):
        return self._get(urls.USER_INTERESTS_TOP_VOICES, {
            "urn": urn,
            "username": username,
            "page": page,
            "pagination_token": pagination_token,
        })

    # ── Group ────────────────────────────────────────────────────────────

    def get_group_info(self, group_id):
        return self._get(urls.GROUP_INFO, {"group_id": group_id})

    def get_group_posts(self, group_id, page=None):
        return self._get(urls.GROUP_POSTS, {
            "group_id": group_id,
            "page": page,
        })

    # ── Search ───────────────────────────────────────────────────────────

    def search_people(
        self,
        name,
        page=None,
        geocode_location=None,
        current_company=None,
        follower_of=None,
        past_company=None,
        school=None,
        profile_language=None,
        industry=None,
        service_category=None,
        first_name=None,
        last_name=None,
        title=None,
    ):
        return self._get(urls.SEARCH_PEOPLE, {
            "name": name,
            "page": page,
            "geocode_location": geocode_location,
            "current_company": current_company,
            "follower_of": follower_of,
            "past_company": past_company,
            "school": school,
            "profile_language": profile_language,
            "industry": industry,
            "service_category": service_category,
            "first_name": first_name,
            "last_name": last_name,
            "title": title,
        })

    def search_posts(
        self,
        keyword,
        page=None,
        date_posted=None,
        sort_by=None,
        content_type=None,
        from_member=None,
        from_company=None,
        limit=None,
    ):
        params = {
            "keyword": keyword,
            "page": page,
            "date_posted": date_posted,
            "sort_by": sort_by,
            "content_type": content_type,
            "from_member": from_member,
            "from_company": from_company,
            "limit": limit,
        }
        validate_params("search_posts", params)
        return self._get(urls.SEARCH_POSTS, params)

    def search_schools(self, keyword, page=None):
        return self._get(urls.SEARCH_SCHOOLS, {
            "keyword": keyword,
            "page": page,
        })

    def search_locations(self, keyword):
        return self._get(urls.SEARCH_LOCATION, {"keyword": keyword})

    def search_industry_suggestions(self, keyword):
        return self._get(urls.SEARCH_SUGGESTION_INDUSTRY, {"keyword": keyword})

    # ── Ad Library ───────────────────────────────────────────────────────

    def search_ads(self, keyword=None, advertiser_name=None, country=None, date=None, pagination_token=None):
        params = {
            "keyword": keyword,
            "advertiser_name": advertiser_name,
            "country": country,
            "date": date,
            "pagination_token": pagination_token,
        }
        validate_params("search_ads", params)
        return self._get(urls.AD_SEARCH, params)

    def get_ad_detail(self, ad_id):
        return self._get(urls.AD_DETAIL, {"ad_id": ad_id})

    # ── Company ──────────────────────────────────────────────────────────

    def get_company_profile(self, company=None, company_id=None):
        return self._get(urls.COMPANY_PROFILE, {
            "company": company,
            "company_id": company_id,
        })

    def get_company_posts(self, company_id=None, company=None, page=None, sort_by=None):
        params = {
            "company_id": company_id,
            "company": company,
            "page": page,
            "sort_by": sort_by,
        }
        validate_params("get_company_posts", params)
        return self._get(urls.COMPANY_POSTS, params)

    def get_company_people(self, company_id=None, company=None, page=None):
        return self._get(urls.COMPANY_PEOPLE, {
            "company_id": company_id,
            "company": company,
            "page": page,
        })

    def get_company_jobs(
        self,
        company_id=None,
        company=None,
        page=None,
        sort_by=None,
        date_posted=None,
        geocode=None,
        experience_level=None,
        remote=None,
        job_type=None,
        easy_apply=None,
        has_verifications=None,
        under_10_applicants=None,
        fair_chance_employer=None,
    ):
        params = {
            "company_id": company_id,
            "company": company,
            "page": page,
            "sort_by": sort_by,
            "date_posted": date_posted,
            "geocode": geocode,
            "experience_level": experience_level,
            "remote": remote,
            "job_type": job_type,
            "easy_apply": easy_apply,
            "has_verifications": has_verifications,
            "under_10_applicants": under_10_applicants,
            "fair_chance_employer": fair_chance_employer,
        }
        validate_params("get_company_jobs", params)
        return self._get(urls.COMPANY_JOBS, params)

    def get_company_job_count(self, company_id=None, company=None):
        return self._get(urls.COMPANY_JOB_COUNT, {
            "company_id": company_id,
            "company": company,
        })

    def get_company_associated_member_insights(self, company_id=None, company=None):
        return self._get(urls.COMPANY_ASSOCIATED_MEMBER_INSIGHTS, {
            "company_id": company_id,
            "company": company,
        })

    def get_company_affiliated_pages(self, company_id=None, company=None):
        return self._get(urls.COMPANY_AFFILIATED_PAGES, {
            "company_id": company_id,
            "company": company,
        })