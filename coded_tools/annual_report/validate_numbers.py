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
import re
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Set
from typing import Union

from neuro_san.interfaces.coded_tool import CodedTool

logger = logging.getLogger(__name__)

_REPORT_PATH = "coded_tools/annual_report/complete_annual_report_2024.txt"

# Matches integers, comma-formatted integers, and decimal numbers.
# Examples: 1,234  |  19.7  |  1234  |  4.2  |  100
_NUMBER_PATTERN = re.compile(r"\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b|\b\d+\.\d+\b")

# Words that are too common to serve as meaningful context signals.
_STOPWORDS = {
    "a", "an", "the", "of", "in", "and", "to", "for", "at", "by", "our", "we",
    "is", "are", "was", "were", "be", "been", "or", "on", "as", "its", "it",
    "with", "from", "that", "this", "have", "has", "had", "their", "they",
}

# Sentence boundary characters used to delimit the context window.
_SENTENCE_BOUNDARIES = re.compile(r"[.\n|]")


def _signal_words(text: str, num_start: int, num_end: int) -> Set[str]:
    """
    Return meaningful words from the sentence containing the number at
    [num_start, num_end).  Sentence boundaries are '.', newlines, and '|'
    (table cell separators).  Drops stopwords and single-character tokens.
    """
    # Walk left to find the sentence start.
    left = _SENTENCE_BOUNDARIES.search(text[:num_start][::-1])
    sent_start = (num_start - left.start()) if left else 0

    # Walk right to find the sentence end.
    right = _SENTENCE_BOUNDARIES.search(text, num_end)
    sent_end = right.start() if right else len(text)

    sentence = text[sent_start:sent_end].lower()
    tokens = re.findall(r"[a-z]+", sentence)
    return {t for t in tokens if t not in _STOPWORDS and len(t) > 2}


class ReportNumberValidator(CodedTool):
    """
    CodedTool that validates every number in a draft response against
    Cognizant's complete 2024 Annual Report text.

    Extracts all numeric tokens from the provided response using regex,
    then verifies each one exists verbatim in the source document.
    If any number cannot be found, the tool returns a prominent error
    declaring the response invalid.
    """

    def __init__(self):
        self._report_text: Optional[str] = None

    def _load_report(self) -> str:
        """Load the complete annual report text (cached after first read)."""
        if self._report_text is None:
            try:
                with open(_REPORT_PATH, "r", encoding="utf-8") as f:
                    self._report_text = f.read()
                logger.debug("Annual report loaded for number validation (%d chars).", len(self._report_text))
            except OSError as e:
                logger.error("Failed to load annual report for validation: %s", e)
                raise
        return self._report_text

    @staticmethod
    def _extract_numbers(text: str) -> List[str]:
        """Return a deduplicated, order-preserving list of numeric tokens found in text."""
        matches = _NUMBER_PATTERN.findall(text)
        seen: Set[str] = set()
        unique: List[str] = []
        for match in matches:
            if match not in seen:
                seen.add(match)
                unique.append(match)
        return unique

    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Union[Dict[str, Any], str]:
        """
        :param args: An argument dictionary with the following keys:
            - "response" (str): The complete draft response text to validate.

        :param sly_data: Shared bulletin board (treated as read-only here).

        :return:
            If all numbers are verified:
                {"valid": True, "message": "...", "validated_numbers": [...]}
            If any number is missing or has mismatched context:
                {"valid": False, "message": "<LOUD ERROR>",
                 "missing_numbers": [...], "context_mismatches": [...]}
            On error:
                A plain error string.
        """
        response_text: str = args.get("response", "")
        if not response_text:
            return "Error: No response text provided for number validation."

        try:
            report_text = self._load_report()
        except OSError as e:
            return f"Error: Could not load the annual report for validation: {e}"

        numbers = self._extract_numbers(response_text)

        if not numbers:
            logger.debug("No numbers found in the response — validation trivially passes.")
            return {
                "valid": True,
                "message": "No numbers found in the response. Validation passed.",
                "validated_numbers": [],
            }

        missing, context_mismatches = self._check_numbers(
            response_text, report_text,
        )
        return self._build_result(numbers, missing, context_mismatches)

    @staticmethod
    def _check_numbers(
        response_text: str, report_text: str,
    ) -> tuple:
        """Check each number for presence and context match in the report.

        Returns (missing, context_mismatches) lists.
        """
        missing: List[str] = []
        context_mismatches: List[str] = []
        checked: Set[str] = set()

        for m in _NUMBER_PATTERN.finditer(response_text):
            number = m.group()
            if number in checked:
                continue
            checked.add(number)

            # 1. Verbatim presence check.
            if number not in report_text:
                missing.append(number)
                continue

            # 2. Context check: at least one occurrence of this number in the report
            #    must share a signal word with the response context.
            resp_signals = _signal_words(response_text, m.start(), m.end())
            if resp_signals:
                context_ok = False
                for rm in re.finditer(re.escape(number), report_text):
                    report_signals = _signal_words(report_text, rm.start(), rm.end())
                    if not report_signals:
                        context_ok = True
                        break
                    if resp_signals & report_signals:
                        context_ok = True
                        break
                if not context_ok:
                    context_mismatches.append(number)

        return missing, context_mismatches

    @staticmethod
    def _build_result(
        numbers: List[str],
        missing: List[str],
        context_mismatches: List[str],
    ) -> Dict[str, Any]:
        """Build the validation result dictionary."""
        flagged = set(missing) | set(context_mismatches)
        validated = [n for n in numbers if n not in flagged]

        if not missing and not context_mismatches:
            logger.debug("Number validation passed: all %d figure(s) verified.", len(numbers))
            return {
                "valid": True,
                "message": (
                    f"All {len(numbers)} number(s) in the response were verified against "
                    "Cognizant's 2024 Annual Report. The information is valid."
                ),
                "validated_numbers": validated,
            }

        sections: List[str] = []
        if missing:
            sections.append(
                f"NOT found in the report ({len(missing)}):\n"
                + "\n".join(f"  - {n}" for n in missing)
            )
        if context_mismatches:
            sections.append(
                f"Found verbatim but nearby context does not match ({len(context_mismatches)}):\n"
                + "\n".join(f"  - {n}" for n in context_mismatches)
            )

        error_message = (
            "\n"
            "╔══════════════════════════════════════════════════════════════╗\n"
            "║           !! VALIDATION FAILED — DATA IS NOT VALID !!       ║\n"
            "╚══════════════════════════════════════════════════════════════╝\n"
            "\n"
            + "\n\n".join(sections)
            + "\n\n"
            "These figures are NOT verified against Cognizant's 2024 Annual Report "
            "and may be hallucinated or otherwise inaccurate.\n\n"
            "YOU MUST NOT deliver this response to the user as-is.\n"
            "Revisit the source material, correct every unverified figure, "
            "and re-validate before presenting any output."
        )
        logger.error(
            "NUMBER VALIDATION FAILED — missing: %s  context_mismatches: %s",
            missing,
            context_mismatches,
        )
        return {
            "valid": False,
            "message": error_message,
            "missing_numbers": missing,
            "context_mismatches": context_mismatches,
        }

    async def async_invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Union[Dict[str, Any], str]:
        """Runs the synchronous invoke in a thread to avoid blocking the event loop."""
        return await asyncio.to_thread(self.invoke, args, sly_data)
