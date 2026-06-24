# LinkedIn Scraper

Python client for the [Fresh LinkedIn Scraper API](https://docs.saleleads.ai) via RapidAPI. Covers all 45 endpoints across jobs, profiles, posts, companies, search, groups, and ads.

## Setup

```bash
# requires Python 3.12+
uv sync

# add your RapidAPI key
echo "RAPID_API_TOKEN=your_key_here" > .env
```

Get your API key from [RapidAPI](https://rapidapi.com/freshdata-freshdata-default/api/fresh-linkedin-scraper-api).

## Quick Start

```python
from linkedin_scraper import LinkedInScraper

scraper = LinkedInScraper()

# find the geocode for a location
locations = scraper.search_locations("San Francisco")
geocode = locations["data"][0]["id"]

# search for remote jobs with filters
jobs = scraper.search_jobs(
    keyword="Software Engineer",
    geocode=geocode,
    remote="remote",
    job_type="full_time",
    experience_level="mid_senior",
    sort_by="recent",
)
for job in jobs["data"][:3]:
    print(job["title"], "—", job["company"]["name"])

    # get full details for each job
    detail = scraper.get_job_detail(job["id"], include_skills=True)
    print(detail["data"].get("salary", {}))

# look up a company
company = scraper.get_company_profile(company="google")
print(company["data"]["name"], company["data"].get("staff_count"))

# search for people
people = scraper.search_people("Sundar", current_company="1441", title="CEO")
for person in people["data"][:3]:
    print(person["name"], "—", person.get("headline", ""))
```

See [main.py](main.py) for a full runnable example.

## API Coverage

### Job

| Method | Description |
|--------|-------------|
| `search_jobs(keyword, ...)` | Search jobs with filters for location, experience, remote, job type, industry, etc. |
| `get_job_detail(job_id, include_skills=)` | Get full job details including salary, description, and optionally skills |

### Post

| Method | Description |
|--------|-------------|
| `get_post_detail(post_id)` | Get a post's full content |
| `get_post_comments(post_id, sort_order=, post_type=)` | Get comments on a post |
| `get_post_reactions(post_id, type=)` | Get reactions (like, praise, empathy, etc.) |
| `get_post_reposts(post_id)` | Get reposts with pagination |

### User Profile

| Method | Description |
|--------|-------------|
| `get_user_profile(username, ...)` | Full profile with optional includes (experiences, skills, education, etc.) |
| `get_user_contact(username)` | Contact info |
| `get_user_posts(username=)` | User's posts |
| `get_user_comments(username=)` | User's comments |
| `get_user_videos(username=)` | User's videos |
| `get_user_images(username=)` | User's images |
| `get_user_reactions(username=)` | User's reactions |
| `get_user_documents(username)` | User's documents |
| `get_user_recommendations(username=, type=)` | Recommendations received or given |
| `save_user_profile_to_pdf(username)` | Export profile as PDF |

### User Additional Data

| Method | Description |
|--------|-------------|
| `get_user_about(username=)` | About section |
| `get_user_skills(username=)` | Skills list |
| `get_user_educations(username=)` | Education history |
| `get_user_certifications(username=)` | Licenses and certifications |
| `get_user_publications(username=)` | Publications |
| `get_user_honors(username=)` | Honors and awards |
| `get_user_experience(username=)` | Work experience |
| `get_user_volunteers(username=)` | Volunteer experience |
| `get_user_follower_and_connection(username)` | Follower/connection counts |

### User Interests

| Method | Description |
|--------|-------------|
| `get_user_interest_companies(username=)` | Companies the user follows |
| `get_user_interest_groups(username=)` | Groups the user is in |
| `get_user_interest_top_voices(username=)` | Top voices the user follows |

### Group

| Method | Description |
|--------|-------------|
| `get_group_info(group_id)` | Group details |
| `get_group_posts(group_id)` | Posts in a group |

### Search

| Method | Description |
|--------|-------------|
| `search_people(name, ...)` | Search people with filters for company, school, title, industry, location |
| `search_posts(keyword, ...)` | Search posts by keyword, date, content type |
| `search_schools(keyword)` | Search schools |
| `search_locations(keyword)` | Search location geocodes |
| `search_industry_suggestions(keyword)` | Search industry IDs |

### Ad Library

| Method | Description |
|--------|-------------|
| `search_ads(keyword=, advertiser_name=, country=, date=)` | Search LinkedIn ads |
| `get_ad_detail(ad_id)` | Get ad details |

### Company

| Method | Description |
|--------|-------------|
| `get_company_profile(company=, company_id=)` | Company profile |
| `get_company_posts(company_id=, sort_by=)` | Company posts |
| `get_company_people(company_id=)` | Company employees |
| `get_company_jobs(company_id=, ...)` | Company job listings with filters |
| `get_company_job_count(company_id=)` | Total job count |
| `get_company_associated_member_insights(company_id=)` | Member insights |
| `get_company_affiliated_pages(company_id=)` | Affiliated company pages |

## Parameter Validation

Categorical parameters are validated before requests are sent. Passing an invalid value raises a `ValueError`:

```python
scraper.search_jobs("Engineer", sort_by="newest")
# ValueError: search_jobs() invalid sort_by='newest', must be one of ('recent', 'relevant')
```

Validated parameters and their allowed values:

| Parameter | Allowed Values |
|-----------|---------------|
| `sort_by` (jobs) | `recent`, `relevant` |
| `date_posted` (jobs) | `anytime`, `past_month`, `past_week`, `past_24_hours` |
| `experience_level` | `internship`, `entry_level`, `associate`, `mid_senior`, `director`, `executive` |
| `remote` | `onsite`, `remote`, `hybrid` |
| `job_type` | `full_time`, `part_time`, `contract`, `temporary`, `volunteer`, `internship`, `other` |
| `sort_order` (comments) | `recent`, `relevance` |
| `post_type` | `activity`, `ugc` |
| `type` (reactions) | `all`, `like`, `praise`, `empathy`, `appreciation`, `interest` |
| `type` (recommendations) | `received`, `given` |
| `date_posted` (search posts) | `past_month`, `past_week`, `past_24h` |
| `sort_by` (search posts) | `date_posted`, `relevance` |
| `content_type` | `videos`, `photos`, `jobs`, `live_videos`, `documents`, `collaborative_articles` |
| `date` (ads) | `last-30-days`, `current-month`, `current-year`, `last-year` |
| `sort_by` (company posts) | `top`, `recent` |

## Project Structure

```
linkedin_scraper/
  main.py                        # entry point / usage examples
  .env                           # RAPID_API_TOKEN=your_key
  linkedin_scraper/
    __init__.py
    linkedin_scraper.py          # LinkedInScraper client class
    urls.py                      # all endpoint URLs
    validators.py                # parameter validation rules
```

## License

MIT
