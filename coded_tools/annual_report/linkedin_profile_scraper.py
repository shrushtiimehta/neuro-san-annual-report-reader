# Copyright © 2025-2026 Cognizant Technology Solutions Corp, www.cognizant.com.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# END COPYRIGHT

import asyncio
import logging
import os
from typing import Any
from typing import Dict
from typing import Union

import requests
from neuro_san.interfaces.coded_tool import CodedTool
from requests.exceptions import RequestException
from requests.exceptions import Timeout

logger = logging.getLogger(__name__)

# Apify run-sync-get-dataset-items endpoint for apimaestro/linkedin-profile-detail
APIFY_ENDPOINT = (
    "https://api.apify.com/v2/acts/VhxlqQXRwhW8H5hNV/run-sync-get-dataset-items"
)


class ApifyLinkedinProfileScraper(CodedTool):
    """
    Scrapes a LinkedIn profile using the Apify apimaestro/linkedin-profile-detail actor.
    Returns name, about, current job, work experience, education (school, degree, major),
    and most recent original post.
    """

    def __init__(self):
        self.apify_token = os.getenv("APIFY_API_KEY")
        if not self.apify_token:
            logger.error("[LinkedIn Profile Scraper] APIFY_API_KEY environment variable not set")

    def run_actor(self, profile_url: str) -> list:
        # Actor accepts a full URL, bare slug, or LinkedIn URN as "username"
        try:
            resp = requests.post(
                APIFY_ENDPOINT,
                params={"token": self.apify_token},
                headers={"Content-Type": "application/json"},
                json={"username": profile_url},
                timeout=120,
            )
            resp.raise_for_status()
        except Timeout as exc:
            raise RuntimeError(f"Timeout calling Apify: {exc}") from exc
        except RequestException as exc:
            raise RuntimeError(f"Request error calling Apify: {exc}") from exc

        data = resp.json()
        return data if isinstance(data, list) else []

    def extract_profile(self, raw: list) -> dict:
        if not raw:
            return {"success": False, "message": "No profile data returned.", "data": {}}

        item = raw[0]
        logger.debug("[LinkedIn Profile Scraper] Raw item top-level keys: %s", list(item.keys()))

        basic = item.get("basic_info") or {}

        # Current job — first experience entry where is_current is True
        current_exp = next(
            (e for e in (item.get("experience") or []) if e.get("is_current")),
            None,
        )
        current_job = {
            "title": current_exp.get("title") if current_exp else basic.get("headline"),
            "company": basic.get("current_company"),
        }

        # Work experience
        experience = []
        for exp in item.get("experience") or []:
            experience.append({
                "title": exp.get("title"),
                "company": exp.get("company"),
            })

        # Education
        education = []
        for edu in item.get("education") or []:
            education.append({
                "school": edu.get("school"),
                "degree": edu.get("degree_name"),
                "major": edu.get("field_of_study"),
            })

        # Most recent post that is not a repost (reposts have no original description)
        recent_post = next(
            (
                {"text": p.get("description")}
                for p in (item.get("featured") or [])
                if p.get("type") == "post" and p.get("description", "").strip()
            ),
            None,
        )

        name = basic.get("fullname")
        if not name and not current_job["title"] and not experience and not education:
            logger.warning(
                "[LinkedIn Profile Scraper] Apify returned a response but all fields are null. "
                "Likely rate-limited or blocked by LinkedIn. Raw keys: %s",
                list(item.keys()),
            )
            return {
                "success": False,
                "message": (
                    "The LinkedIn profile was reached but returned no data. "
                    "This is typically caused by LinkedIn rate-limiting or blocking the scraper. "
                    "Please try again in a few minutes."
                ),
                "data": {},
            }

        return {
            "success": True,
            "data": {
                "name": name,
                "about": basic.get("about"),
                "current_job": current_job,
                "experience": experience,
                "education": education,
                "recent_post": recent_post,
            },
        }

    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Union[Dict, str]:
        """
        :param args: An argument dictionary with the following keys:
            - "profile" (str): Full LinkedIn profile URL, bare slug, or LinkedIn URN.

        :param sly_data: A dictionary whose keys are defined by the agent hierarchy,
            but whose values are meant to be kept out of the chat stream.

            This dictionary is largely to be treated as read-only.

            Keys expected for this implementation are:
                "mock_profile" (dict, optional): If present, bypasses the Apify API call
                    and returns this dict directly as the profile data. Used in tests.
                    Expected shape: {"name": str, "about": str, "current_job": {"title": str,
                    "company": str}, "experience": [...], "education": [...], "recent_post": ...}

        :return:
            If successful:
                A dictionary with keys:
                - "success": True
                - "data": dict containing "name", "about", "current_job",
                           "experience", "education", "recent_post"
            Otherwise:
                A dictionary with keys:
                - "success": False
                - "message": error description
                - "data": {}
        """
        profile_url = args.get("profile")
        if not profile_url:
            logger.error("[LinkedIn Profile Scraper] No profile URL provided.")
            return {"success": False, "message": "A valid LinkedIn profile URL is required.", "data": {}}

        # In tests, sly_data may carry a mock_profile to bypass the Apify API call.
        mock_profile = (sly_data or {}).get("mock_profile")
        if mock_profile:
            logger.info("[LinkedIn Profile Scraper] Using mock profile for: %s", profile_url)
            return {"success": True, "data": mock_profile}

        try:
            raw = self.run_actor(profile_url)
            result = self.extract_profile(raw)
            logger.info("[LinkedIn Profile Scraper] Profile scraped: %s", result.get("data", {}).get("name"))
            return result
        except RuntimeError as exc:
            logger.error("[LinkedIn Profile Scraper] %s", exc)
            return {"success": False, "message": str(exc), "data": {}}

    async def async_invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Union[Dict, str]:
        """
        Runs the synchronous invoke method in a thread to avoid blocking the event loop.
        """
        return await asyncio.to_thread(self.invoke, args, sly_data)
