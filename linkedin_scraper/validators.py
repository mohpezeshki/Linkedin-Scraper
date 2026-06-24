SORT_BY_JOB = ("recent", "relevant")
DATE_POSTED_JOB = ("anytime", "past_month", "past_week", "past_24_hours")
EXPERIENCE_LEVEL = ("internship", "entry_level", "associate", "mid_senior", "director", "executive")
REMOTE = ("onsite", "remote", "hybrid")
JOB_TYPE = ("full_time", "part_time", "contract", "temporary", "volunteer", "internship", "other")

SORT_ORDER_COMMENT = ("recent", "relevance")
POST_TYPE = ("activity", "ugc")

REACTION_TYPE = ("all", "like", "praise", "empathy", "appreciation", "interest")

RECOMMENDATION_TYPE = ("received", "given")

DATE_POSTED_SEARCH = ("past_month", "past_week", "past_24h")
SORT_BY_SEARCH_POST = ("date_posted", "relevance")
CONTENT_TYPE = ("videos", "photos", "jobs", "live_videos", "documents", "collaborative_articles")

AD_DATE = ("last-30-days", "current-month", "current-year", "last-year")

SORT_BY_COMPANY_POST = ("top", "recent")


PARAM_RULES = {
    "search_jobs": {
        "sort_by": SORT_BY_JOB,
        "date_posted": DATE_POSTED_JOB,
        "experience_level": EXPERIENCE_LEVEL,
        "remote": REMOTE,
        "job_type": JOB_TYPE,
    },
    "get_post_comments": {
        "sort_order": SORT_ORDER_COMMENT,
        "post_type": POST_TYPE,
    },
    "get_post_reactions": {
        "type": REACTION_TYPE,
    },
    "get_user_recommendations": {
        "type": RECOMMENDATION_TYPE,
    },
    "search_posts": {
        "date_posted": DATE_POSTED_SEARCH,
        "sort_by": SORT_BY_SEARCH_POST,
        "content_type": CONTENT_TYPE,
    },
    "search_ads": {
        "date": AD_DATE,
    },
    "get_company_posts": {
        "sort_by": SORT_BY_COMPANY_POST,
    },
    "get_company_jobs": {
        "sort_by": SORT_BY_JOB,
        "date_posted": DATE_POSTED_JOB,
        "experience_level": EXPERIENCE_LEVEL,
        "remote": REMOTE,
        "job_type": JOB_TYPE,
    },
}


def validate_params(method_name, params):
    rules = PARAM_RULES.get(method_name, {})
    for param_name, allowed in rules.items():
        value = params.get(param_name)
        if value is not None and value not in allowed:
            raise ValueError(
                f"{method_name}() invalid {param_name}={value!r}, "
                f"must be one of {allowed}"
            )
