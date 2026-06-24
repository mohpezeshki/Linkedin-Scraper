"""LinkedIn Scraper API client.

A Python wrapper for the Fresh LinkedIn Scraper API on RapidAPI,
covering jobs, posts, user profiles, companies, search, groups, and ads.
"""

from dotenv import load_dotenv
import logging
import os
import requests

from linkedin_scraper import urls
from linkedin_scraper.validators import validate_params


load_dotenv()

logger = logging.getLogger(__name__)


class LinkedInScraper:
    """Client for the Fresh LinkedIn Scraper API.

    Provides methods for all 45 API endpoints. Authenticates via a
    RapidAPI key passed directly or read from the ``RAPID_API_TOKEN``
    environment variable.

    Args:
        api_key: RapidAPI key. Falls back to the ``RAPID_API_TOKEN``
            environment variable when not provided.

    Raises:
        ValueError: If no API key is provided or found in the environment.

    Example:
        >>> scraper = LinkedInScraper()
        >>> jobs = scraper.search_jobs("Data Engineer", remote="remote")
        >>> print(jobs["data"][0]["title"])
    """

    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("RAPID_API_TOKEN")
        if not self.api_key:
            raise ValueError("RAPID_API_TOKEN not set")
        self.session = requests.Session()
        self.session.headers["X-RapidAPI-Key"] = self.api_key

    def _get(self, url, params=None):
        """Sends a GET request, stripping ``None``-valued params.

        Args:
            url: The full endpoint URL.
            params: Query parameters. Keys with ``None`` values are removed
                before the request is sent.

        Returns:
            The parsed JSON response as a dict.

        Raises:
            requests.HTTPError: If the API returns a non-2xx status code.
        """
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
        """Searches for jobs based on keyword and optional filters.

        Args:
            keyword: Search term for job titles or descriptions.
            page: Page number for pagination (default 1).
            sort_by: Sort order. One of ``"recent"`` or ``"relevant"``.
            date_posted: Posting recency filter. One of ``"anytime"``,
                ``"past_month"``, ``"past_week"``, or ``"past_24_hours"``.
            geocode: Numeric geocode for location-based filtering.
            company: Numeric company ID to filter by.
            experience_level: Required seniority. One of ``"internship"``,
                ``"entry_level"``, ``"associate"``, ``"mid_senior"``,
                ``"director"``, or ``"executive"``.
            remote: Workplace type. One of ``"onsite"``, ``"remote"``,
                or ``"hybrid"``.
            job_type: Employment type. One of ``"full_time"``,
                ``"part_time"``, ``"contract"``, ``"temporary"``,
                ``"volunteer"``, ``"internship"``, or ``"other"``.
            easy_apply: If ``True``, only return Easy Apply jobs.
            has_verifications: If ``True``, only return verified companies.
            under_10_applicants: If ``True``, only return jobs with fewer
                than 10 applicants.
            fair_chance_employer: If ``True``, only return fair chance
                employers.
            industry_ids: Comma-separated industry IDs (e.g. ``"4,435"``).

        Returns:
            A dict with keys ``"success"``, ``"cost"``, and ``"data"``
            where ``"data"`` is a list of job summary dicts.

        Raises:
            ValueError: If a categorical parameter has an invalid value.
            requests.HTTPError: On API error responses.
        """
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
        """Gets detailed information about a specific job posting.

        Args:
            job_id: Numeric job ID string (e.g. ``"4413763968"``).
            include_skills: If ``True``, include required skills in the
                response. Consumes an additional API request.

        Returns:
            A dict with keys ``"success"``, ``"cost"``, and ``"data"``
            containing full job details (title, description, salary,
            company, location, etc.).

        Raises:
            requests.HTTPError: On API error responses.
        """
        return self._get(urls.JOB_DETAIL, {
            "job_id": job_id,
            "include_skills": include_skills,
        })

    # ── Post ─────────────────────────────────────────────────────────────

    def get_post_detail(self, post_id):
        """Gets the full content of a LinkedIn post.

        Args:
            post_id: Numeric post ID string.

        Returns:
            A dict with keys ``"success"``, ``"cost"``, and ``"data"``
            containing the post content.

        Raises:
            requests.HTTPError: On API error responses.
        """
        return self._get(urls.POST_DETAIL, {"post_id": post_id})

    def get_post_comments(self, post_id, page=None, sort_order=None, post_type=None):
        """Gets comments on a LinkedIn post.

        Args:
            post_id: Numeric post ID string.
            page: Page number for pagination (default 1).
            sort_order: Comment sort order. One of ``"recent"`` or
                ``"relevance"``.
            post_type: Post type. One of ``"activity"`` or ``"ugc"``.

        Returns:
            A dict with keys ``"success"``, ``"cost"``, ``"total"``,
            ``"has_more"``, and ``"data"`` (list of comment dicts).

        Raises:
            ValueError: If a categorical parameter has an invalid value.
            requests.HTTPError: On API error responses.
        """
        params = {
            "post_id": post_id,
            "page": page,
            "sort_order": sort_order,
            "post_type": post_type,
        }
        validate_params("get_post_comments", params)
        return self._get(urls.POST_COMMENTS, params)

    def get_post_reactions(self, post_id, page=None, type=None):
        """Gets reactions on a LinkedIn post.

        Args:
            post_id: Numeric post ID string.
            page: Page number for pagination (default 1).
            type: Reaction type filter. One of ``"all"``, ``"like"``,
                ``"praise"``, ``"empathy"``, ``"appreciation"``,
                or ``"interest"``.

        Returns:
            A dict with keys ``"success"``, ``"cost"``, ``"total"``,
            ``"has_more"``, and ``"data"`` (list of reaction dicts).

        Raises:
            ValueError: If a categorical parameter has an invalid value.
            requests.HTTPError: On API error responses.
        """
        params = {
            "post_id": post_id,
            "page": page,
            "type": type,
        }
        validate_params("get_post_reactions", params)
        return self._get(urls.POST_REACTIONS, params)

    def get_post_reposts(self, post_id, page=None, pagination_token=None):
        """Gets reposts of a LinkedIn post.

        Args:
            post_id: Numeric post ID string.
            page: Page number for pagination (default 1).
            pagination_token: Token for cursor-based pagination.

        Returns:
            A dict with keys ``"success"``, ``"cost"``, ``"total"``,
            ``"has_more"``, ``"pagination_token"``, and ``"data"``.

        Raises:
            requests.HTTPError: On API error responses.
        """
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
        """Gets a LinkedIn user's profile.

        Each ``include_*`` flag adds a section to the response and
        consumes an additional API request.

        Args:
            username: LinkedIn username (e.g. ``"satyanadella"``).
            include_follower_and_connection: Include follower/connection
                counts.
            include_experiences: Include work experience.
            include_skills: Include skills.
            include_services: Include offered services.
            include_certifications: Include licenses and certifications.
            include_publications: Include publications.
            include_honors: Include honors and awards.
            include_volunteers: Include volunteer experience.
            include_educations: Include education history.
            include_bio: Include the about/bio section.

        Returns:
            A dict with keys ``"success"``, ``"cost"``, and ``"data"``
            containing the user profile.

        Raises:
            requests.HTTPError: On API error responses.
        """
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
        """Gets a LinkedIn user's contact information.

        Args:
            username: LinkedIn username.

        Returns:
            A dict with keys ``"success"``, ``"cost"``, and ``"data"``
            containing contact details.

        Raises:
            requests.HTTPError: On API error responses.
        """
        return self._get(urls.USER_CONTACT, {"username": username})

    def get_user_posts(self, urn=None, username=None, page=None, pagination_token=None):
        """Gets posts authored by a LinkedIn user.

        Provide either ``urn`` or ``username`` to identify the user.

        Args:
            urn: LinkedIn member URN.
            username: LinkedIn username.
            page: Page number for pagination (default 1).
            pagination_token: Token for cursor-based pagination.

        Returns:
            A dict with keys ``"success"``, ``"cost"``, and ``"data"``
            (list of post dicts).

        Raises:
            requests.HTTPError: On API error responses.
        """
        return self._get(urls.USER_POSTS, {
            "urn": urn,
            "username": username,
            "page": page,
            "pagination_token": pagination_token,
        })

    def get_user_comments(self, urn=None, username=None, page=None, pagination_token=None):
        """Gets comments made by a LinkedIn user.

        Provide either ``urn`` or ``username`` to identify the user.

        Args:
            urn: LinkedIn member URN.
            username: LinkedIn username.
            page: Page number for pagination (default 1).
            pagination_token: Token for cursor-based pagination.

        Returns:
            A dict with keys ``"success"``, ``"cost"``,
            ``"pagination_token"``, and ``"data"``.

        Raises:
            requests.HTTPError: On API error responses.
        """
        return self._get(urls.USER_COMMENTS, {
            "urn": urn,
            "username": username,
            "page": page,
            "pagination_token": pagination_token,
        })

    def get_user_videos(self, urn=None, username=None, page=None, pagination_token=None):
        """Gets videos posted by a LinkedIn user.

        Provide either ``urn`` or ``username`` to identify the user.

        Args:
            urn: LinkedIn member URN.
            username: LinkedIn username.
            page: Page number for pagination (default 1).
            pagination_token: Token for cursor-based pagination.

        Returns:
            A dict with keys ``"success"``, ``"cost"``,
            ``"pagination_token"``, and ``"data"``.

        Raises:
            requests.HTTPError: On API error responses.
        """
        return self._get(urls.USER_VIDEOS, {
            "urn": urn,
            "username": username,
            "page": page,
            "pagination_token": pagination_token,
        })

    def get_user_images(self, urn=None, username=None, page=None, pagination_token=None):
        """Gets images posted by a LinkedIn user.

        Provide either ``urn`` or ``username`` to identify the user.

        Args:
            urn: LinkedIn member URN.
            username: LinkedIn username.
            page: Page number for pagination (default 1).
            pagination_token: Token for cursor-based pagination.

        Returns:
            A dict with keys ``"success"``, ``"cost"``,
            ``"pagination_token"``, and ``"data"``.

        Raises:
            requests.HTTPError: On API error responses.
        """
        return self._get(urls.USER_IMAGES, {
            "urn": urn,
            "username": username,
            "page": page,
            "pagination_token": pagination_token,
        })

    def get_user_reactions(self, urn=None, username=None, page=None, pagination_token=None):
        """Gets reactions made by a LinkedIn user.

        Provide either ``urn`` or ``username`` to identify the user.

        Args:
            urn: LinkedIn member URN.
            username: LinkedIn username.
            page: Page number for pagination (default 1).
            pagination_token: Token for cursor-based pagination.

        Returns:
            A dict with keys ``"success"``, ``"cost"``,
            ``"pagination_token"``, and ``"data"``.

        Raises:
            requests.HTTPError: On API error responses.
        """
        return self._get(urls.USER_REACTIONS, {
            "urn": urn,
            "username": username,
            "page": page,
            "pagination_token": pagination_token,
        })

    def get_user_documents(self, username, page=None, pagination_token=None):
        """Gets documents shared by a LinkedIn user.

        Args:
            username: LinkedIn username.
            page: Page number for pagination (default 1).
            pagination_token: Token for cursor-based pagination.

        Returns:
            A dict with keys ``"success"``, ``"cost"``, and ``"data"``.

        Raises:
            requests.HTTPError: On API error responses.
        """
        return self._get(urls.USER_DOCUMENTS, {
            "username": username,
            "page": page,
            "pagination_token": pagination_token,
        })

    def get_user_recommendations(self, urn=None, username=None, page=None, type=None):
        """Gets recommendations for a LinkedIn user.

        Provide either ``urn`` or ``username`` to identify the user.

        Args:
            urn: LinkedIn member URN.
            username: LinkedIn username.
            page: Page number for pagination (default 1).
            type: Filter direction. One of ``"received"`` or ``"given"``.

        Returns:
            A dict with keys ``"success"``, ``"cost"``, ``"total"``,
            ``"has_more"``, and ``"data"``.

        Raises:
            ValueError: If ``type`` has an invalid value.
            requests.HTTPError: On API error responses.
        """
        params = {
            "urn": urn,
            "username": username,
            "page": page,
            "type": type,
        }
        validate_params("get_user_recommendations", params)
        return self._get(urls.USER_RECOMMENDATIONS, params)

    def save_user_profile_to_pdf(self, username):
        """Exports a LinkedIn user's profile as a PDF.

        Args:
            username: LinkedIn username.

        Returns:
            A dict containing the PDF download URL or binary data.

        Raises:
            requests.HTTPError: On API error responses.
        """
        return self._get(urls.USER_SAVE_TO_PDF, {"username": username})

    # ── User Additional Data ─────────────────────────────────────────────

    def get_user_about(self, urn=None, username=None, page=None):
        """Gets a LinkedIn user's about/bio section.

        Provide either ``urn`` or ``username`` to identify the user.

        Args:
            urn: LinkedIn member URN.
            username: LinkedIn username.
            page: Page number for pagination (default 1).

        Returns:
            A dict with keys ``"success"``, ``"cost"``, and ``"data"``.

        Raises:
            requests.HTTPError: On API error responses.
        """
        return self._get(urls.USER_ABOUT, {
            "urn": urn,
            "username": username,
            "page": page,
        })

    def get_user_skills(self, urn=None, username=None, page=None):
        """Gets a LinkedIn user's skills.

        Provide either ``urn`` or ``username`` to identify the user.

        Args:
            urn: LinkedIn member URN.
            username: LinkedIn username.
            page: Page number for pagination (default 1).

        Returns:
            A dict with keys ``"success"``, ``"cost"``, ``"total"``,
            ``"has_more"``, and ``"data"``.

        Raises:
            requests.HTTPError: On API error responses.
        """
        return self._get(urls.USER_SKILLS, {
            "urn": urn,
            "username": username,
            "page": page,
        })

    def get_user_educations(self, urn=None, username=None, page=None):
        """Gets a LinkedIn user's education history.

        Provide either ``urn`` or ``username`` to identify the user.

        Args:
            urn: LinkedIn member URN.
            username: LinkedIn username.
            page: Page number for pagination (default 1).

        Returns:
            A dict with keys ``"success"``, ``"cost"``, ``"total"``,
            ``"has_more"``, and ``"data"``.

        Raises:
            requests.HTTPError: On API error responses.
        """
        return self._get(urls.USER_EDUCATIONS, {
            "urn": urn,
            "username": username,
            "page": page,
        })

    def get_user_certifications(self, urn=None, username=None, page=None):
        """Gets a LinkedIn user's licenses and certifications.

        Provide either ``urn`` or ``username`` to identify the user.

        Args:
            urn: LinkedIn member URN.
            username: LinkedIn username.
            page: Page number for pagination (default 1).

        Returns:
            A dict with keys ``"success"``, ``"cost"``, ``"total"``,
            ``"has_more"``, and ``"data"``.

        Raises:
            requests.HTTPError: On API error responses.
        """
        return self._get(urls.USER_CERTIFICATIONS, {
            "urn": urn,
            "username": username,
            "page": page,
        })

    def get_user_publications(self, urn=None, username=None, page=None):
        """Gets a LinkedIn user's publications.

        Provide either ``urn`` or ``username`` to identify the user.

        Args:
            urn: LinkedIn member URN.
            username: LinkedIn username.
            page: Page number for pagination (default 1).

        Returns:
            A dict with keys ``"success"``, ``"cost"``, ``"total"``,
            ``"has_more"``, and ``"data"``.

        Raises:
            requests.HTTPError: On API error responses.
        """
        return self._get(urls.USER_PUBLICATIONS, {
            "urn": urn,
            "username": username,
            "page": page,
        })

    def get_user_honors(self, urn=None, username=None, page=None):
        """Gets a LinkedIn user's honors and awards.

        Provide either ``urn`` or ``username`` to identify the user.

        Args:
            urn: LinkedIn member URN.
            username: LinkedIn username.
            page: Page number for pagination (default 1).

        Returns:
            A dict with keys ``"success"``, ``"cost"``, ``"total"``,
            ``"has_more"``, and ``"data"``.

        Raises:
            requests.HTTPError: On API error responses.
        """
        return self._get(urls.USER_HONORS, {
            "urn": urn,
            "username": username,
            "page": page,
        })

    def get_user_experience(self, urn=None, username=None, page=None):
        """Gets a LinkedIn user's work experience.

        Provide either ``urn`` or ``username`` to identify the user.

        Args:
            urn: LinkedIn member URN.
            username: LinkedIn username.
            page: Page number for pagination (default 1).

        Returns:
            A dict with keys ``"success"``, ``"cost"``, ``"total"``,
            ``"has_more"``, and ``"data"``.

        Raises:
            requests.HTTPError: On API error responses.
        """
        return self._get(urls.USER_EXPERIENCE, {
            "urn": urn,
            "username": username,
            "page": page,
        })

    def get_user_volunteers(self, urn=None, username=None, page=None):
        """Gets a LinkedIn user's volunteer experience.

        Provide either ``urn`` or ``username`` to identify the user.

        Args:
            urn: LinkedIn member URN.
            username: LinkedIn username.
            page: Page number for pagination (default 1).

        Returns:
            A dict with keys ``"success"``, ``"cost"``, ``"total"``,
            ``"has_more"``, and ``"data"``.

        Raises:
            requests.HTTPError: On API error responses.
        """
        return self._get(urls.USER_VOLUNTEERS, {
            "urn": urn,
            "username": username,
            "page": page,
        })

    def get_user_follower_and_connection(self, username):
        """Gets a LinkedIn user's follower and connection counts.

        Args:
            username: LinkedIn username.

        Returns:
            A dict with keys ``"success"``, ``"cost"``, and ``"data"``.

        Raises:
            requests.HTTPError: On API error responses.
        """
        return self._get(urls.USER_FOLLOWER_AND_CONNECTION, {"username": username})

    # ── User Interests ───────────────────────────────────────────────────

    def get_user_interest_companies(self, urn=None, username=None, page=None, pagination_token=None):
        """Gets companies a LinkedIn user follows.

        Provide either ``urn`` or ``username`` to identify the user.

        Args:
            urn: LinkedIn member URN.
            username: LinkedIn username.
            page: Page number for pagination (default 1).
            pagination_token: Token for cursor-based pagination.

        Returns:
            A dict with keys ``"success"``, ``"cost"``, and ``"data"``.

        Raises:
            requests.HTTPError: On API error responses.
        """
        return self._get(urls.USER_INTERESTS_COMPANIES, {
            "urn": urn,
            "username": username,
            "page": page,
            "pagination_token": pagination_token,
        })

    def get_user_interest_groups(self, urn=None, username=None, page=None, pagination_token=None):
        """Gets groups a LinkedIn user is a member of.

        Provide either ``urn`` or ``username`` to identify the user.

        Args:
            urn: LinkedIn member URN.
            username: LinkedIn username.
            page: Page number for pagination (default 1).
            pagination_token: Token for cursor-based pagination.

        Returns:
            A dict with keys ``"success"``, ``"cost"``, and ``"data"``.

        Raises:
            requests.HTTPError: On API error responses.
        """
        return self._get(urls.USER_INTERESTS_GROUPS, {
            "urn": urn,
            "username": username,
            "page": page,
            "pagination_token": pagination_token,
        })

    def get_user_interest_top_voices(self, urn=None, username=None, page=None, pagination_token=None):
        """Gets top voices a LinkedIn user follows.

        Provide either ``urn`` or ``username`` to identify the user.

        Args:
            urn: LinkedIn member URN.
            username: LinkedIn username.
            page: Page number for pagination (default 1).
            pagination_token: Token for cursor-based pagination.

        Returns:
            A dict with keys ``"success"``, ``"cost"``, and ``"data"``.

        Raises:
            requests.HTTPError: On API error responses.
        """
        return self._get(urls.USER_INTERESTS_TOP_VOICES, {
            "urn": urn,
            "username": username,
            "page": page,
            "pagination_token": pagination_token,
        })

    # ── Group ────────────────────────────────────────────────────────────

    def get_group_info(self, group_id):
        """Gets information about a LinkedIn group.

        Args:
            group_id: Numeric group ID string.

        Returns:
            A dict with keys ``"success"``, ``"cost"``, and ``"data"``.

        Raises:
            requests.HTTPError: On API error responses.
        """
        return self._get(urls.GROUP_INFO, {"group_id": group_id})

    def get_group_posts(self, group_id, page=None):
        """Gets posts from a LinkedIn group.

        Args:
            group_id: Numeric group ID string.
            page: Page number for pagination (default 1).

        Returns:
            A dict with keys ``"success"``, ``"cost"``, ``"total"``,
            ``"has_more"``, and ``"data"``.

        Raises:
            requests.HTTPError: On API error responses.
        """
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
        """Searches for LinkedIn people by name and optional filters.

        Args:
            name: Search query for the person's name.
            page: Page number for pagination (default 1).
            geocode_location: Numeric geocode for location filtering.
            current_company: Numeric company ID for current employer.
            follower_of: Filter by followers of a specific entity.
            past_company: Numeric company ID for past employer.
            school: Numeric school ID.
            profile_language: Language code (e.g. ``"en"``).
            industry: Numeric industry ID.
            service_category: Service category filter.
            first_name: Filter by first name.
            last_name: Filter by last name.
            title: Filter by job title.

        Returns:
            A dict with keys ``"success"``, ``"cost"``, ``"total"``,
            ``"has_more"``, and ``"data"`` (list of people dicts).

        Raises:
            requests.HTTPError: On API error responses.
        """
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
        """Searches for LinkedIn posts by keyword and optional filters.

        Args:
            keyword: Search term.
            page: Page number for pagination (default 1).
            date_posted: Posting recency filter. One of ``"past_month"``,
                ``"past_week"``, or ``"past_24h"``.
            sort_by: Sort order. One of ``"date_posted"`` or
                ``"relevance"``.
            content_type: Content filter. One of ``"videos"``,
                ``"photos"``, ``"jobs"``, ``"live_videos"``,
                ``"documents"``, or ``"collaborative_articles"``.
            from_member: Filter by member URN.
            from_company: Filter by company ID.
            limit: Maximum number of results.

        Returns:
            A dict with keys ``"success"``, ``"cost"``, ``"total"``,
            ``"has_more"``, and ``"data"`` (list of post dicts).

        Raises:
            ValueError: If a categorical parameter has an invalid value.
            requests.HTTPError: On API error responses.
        """
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
        """Searches for schools by keyword.

        Args:
            keyword: Search term for school names.
            page: Page number for pagination (default 1).

        Returns:
            A dict with keys ``"success"``, ``"cost"``, ``"total"``,
            ``"has_more"``, and ``"data"`` (list of school dicts).

        Raises:
            requests.HTTPError: On API error responses.
        """
        return self._get(urls.SEARCH_SCHOOLS, {
            "keyword": keyword,
            "page": page,
        })

    def search_locations(self, keyword):
        """Searches for location geocodes by keyword.

        Use the returned geocode values with location-based filters
        in other methods like ``search_jobs``.

        Args:
            keyword: Location search term (e.g. ``"San Francisco"``).

        Returns:
            A dict with keys ``"success"``, ``"cost"``, and ``"data"``
            (list of location dicts with geocodes).

        Raises:
            requests.HTTPError: On API error responses.
        """
        return self._get(urls.SEARCH_LOCATION, {"keyword": keyword})

    def search_industry_suggestions(self, keyword):
        """Searches for industry IDs by keyword.

        Use the returned IDs with the ``industry_ids`` parameter
        in ``search_jobs``.

        Args:
            keyword: Industry search term (e.g. ``"technology"``).

        Returns:
            A dict with keys ``"success"``, ``"cost"``, and ``"data"``
            (list of industry dicts with IDs and names).

        Raises:
            requests.HTTPError: On API error responses.
        """
        return self._get(urls.SEARCH_SUGGESTION_INDUSTRY, {"keyword": keyword})

    # ── Ad Library ───────────────────────────────────────────────────────

    def search_ads(self, keyword=None, advertiser_name=None, country=None, date=None, pagination_token=None):
        """Searches the LinkedIn ad library.

        Args:
            keyword: Search term for ad content.
            advertiser_name: Filter by advertiser name.
            country: Country code filter.
            date: Date range filter. One of ``"last-30-days"``,
                ``"current-month"``, ``"current-year"``,
                or ``"last-year"``.
            pagination_token: Token for cursor-based pagination.

        Returns:
            A dict with keys ``"success"``, ``"cost"``, ``"data"``,
            ``"has_more"``, and ``"pagination_token"``.

        Raises:
            ValueError: If ``date`` has an invalid value.
            requests.HTTPError: On API error responses.
        """
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
        """Gets detailed information about a LinkedIn ad.

        Args:
            ad_id: Numeric ad ID string.

        Returns:
            A dict with keys ``"success"``, ``"cost"``, and ``"data"``.

        Raises:
            requests.HTTPError: On API error responses.
        """
        return self._get(urls.AD_DETAIL, {"ad_id": ad_id})

    # ── Company ──────────────────────────────────────────────────────────

    def get_company_profile(self, company=None, company_id=None):
        """Gets a LinkedIn company's profile.

        Provide either ``company`` (universal name / slug) or
        ``company_id`` (numeric ID).

        Args:
            company: Company universal name (e.g. ``"google"``).
            company_id: Numeric company ID string.

        Returns:
            A dict with keys ``"success"``, ``"cost"``, and ``"data"``
            containing company details (description, staff count,
            headquarters, specialities, etc.).

        Raises:
            requests.HTTPError: On API error responses.
        """
        return self._get(urls.COMPANY_PROFILE, {
            "company": company,
            "company_id": company_id,
        })

    def get_company_posts(self, company_id=None, company=None, page=None, sort_by=None):
        """Gets posts published by a LinkedIn company.

        Provide either ``company`` or ``company_id``.

        Args:
            company_id: Numeric company ID string.
            company: Company universal name.
            page: Page number for pagination (default 1).
            sort_by: Sort order. One of ``"top"`` or ``"recent"``.

        Returns:
            A dict with keys ``"success"``, ``"cost"``, ``"total"``,
            ``"has_more"``, and ``"data"``.

        Raises:
            ValueError: If ``sort_by`` has an invalid value.
            requests.HTTPError: On API error responses.
        """
        params = {
            "company_id": company_id,
            "company": company,
            "page": page,
            "sort_by": sort_by,
        }
        validate_params("get_company_posts", params)
        return self._get(urls.COMPANY_POSTS, params)

    def get_company_people(self, company_id=None, company=None, page=None):
        """Gets employees of a LinkedIn company.

        Provide either ``company`` or ``company_id``.

        Args:
            company_id: Numeric company ID string.
            company: Company universal name.
            page: Page number for pagination (default 1).

        Returns:
            A dict with keys ``"success"``, ``"cost"``, ``"total"``,
            ``"has_more"``, and ``"data"``.

        Raises:
            requests.HTTPError: On API error responses.
        """
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
        """Gets job listings from a LinkedIn company.

        Provide either ``company`` or ``company_id``. Accepts the
        same job filters as ``search_jobs``.

        Args:
            company_id: Numeric company ID string.
            company: Company universal name.
            page: Page number for pagination (default 1).
            sort_by: Sort order. One of ``"recent"`` or ``"relevant"``.
            date_posted: Posting recency filter. One of ``"anytime"``,
                ``"past_month"``, ``"past_week"``, or ``"past_24_hours"``.
            geocode: Numeric geocode for location filtering.
            experience_level: Required seniority. One of ``"internship"``,
                ``"entry_level"``, ``"associate"``, ``"mid_senior"``,
                ``"director"``, or ``"executive"``.
            remote: Workplace type. One of ``"onsite"``, ``"remote"``,
                or ``"hybrid"``.
            job_type: Employment type. One of ``"full_time"``,
                ``"part_time"``, ``"contract"``, ``"temporary"``,
                ``"volunteer"``, ``"internship"``, or ``"other"``.
            easy_apply: If ``True``, only return Easy Apply jobs.
            has_verifications: If ``True``, only return verified companies.
            under_10_applicants: If ``True``, only return jobs with fewer
                than 10 applicants.
            fair_chance_employer: If ``True``, only return fair chance
                employers.

        Returns:
            A dict with keys ``"success"``, ``"cost"``, and ``"data"``.

        Raises:
            ValueError: If a categorical parameter has an invalid value.
            requests.HTTPError: On API error responses.
        """
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
        """Gets the total number of job listings for a company.

        Provide either ``company`` or ``company_id``.

        Args:
            company_id: Numeric company ID string.
            company: Company universal name.

        Returns:
            A dict with keys ``"success"``, ``"cost"``, and ``"data"``.

        Raises:
            requests.HTTPError: On API error responses.
        """
        return self._get(urls.COMPANY_JOB_COUNT, {
            "company_id": company_id,
            "company": company,
        })

    def get_company_associated_member_insights(self, company_id=None, company=None):
        """Gets member insights associated with a company.

        Provide either ``company`` or ``company_id``.

        Args:
            company_id: Numeric company ID string.
            company: Company universal name.

        Returns:
            A dict with keys ``"success"``, ``"cost"``, and ``"data"``.

        Raises:
            requests.HTTPError: On API error responses.
        """
        return self._get(urls.COMPANY_ASSOCIATED_MEMBER_INSIGHTS, {
            "company_id": company_id,
            "company": company,
        })

    def get_company_affiliated_pages(self, company_id=None, company=None):
        """Gets affiliated pages (subsidiaries, brands) for a company.

        Provide either ``company`` or ``company_id``.

        Args:
            company_id: Numeric company ID string.
            company: Company universal name.

        Returns:
            A dict with keys ``"success"``, ``"cost"``, and ``"data"``.

        Raises:
            requests.HTTPError: On API error responses.
        """
        return self._get(urls.COMPANY_AFFILIATED_PAGES, {
            "company_id": company_id,
            "company": company,
        })
