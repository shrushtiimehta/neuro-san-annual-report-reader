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

from neuro_san.interfaces.coded_tool import CodedTool
from pypdf import PdfReader
from pypdf.errors import PyPdfError

logger = logging.getLogger(__name__)

# Base path for all knowdocs
_KNOWDOCS = "coded_tools/annual_report/knowdocs"

class ExtractDocs(CodedTool):
    """
    CodedTool implementation that extracts text from all PDFs/TXTs in a given
    directory, or from a single file when a file-level app_name is used.
    Returns a dictionary mapping each file name to its extracted text.
    """

    def __init__(self):
        self.default_path = _KNOWDOCS

        self.docs_path = {
            # Directory-level key — returns all files
            "all": _KNOWDOCS,
            # File-level keys — each maps to a single .txt in knowdocs/
            "business_overview_and_segments": f"{_KNOWDOCS}/business_overview_and_segments.txt",
            "competition_ip_people_culture": f"{_KNOWDOCS}/competition_ip_people_culture.txt",
            "services_solutions_and_delivery": f"{_KNOWDOCS}/services_solutions_and_delivery.txt",
            "ai_era_and_industry_expertise": f"{_KNOWDOCS}/ai_era_and_industry_expertise.txt",
            "cover_and_shareholder_letter": f"{_KNOWDOCS}/cover_and_shareholder_letter.txt",
            "financial_performance_summary": f"{_KNOWDOCS}/financial_performance_summary.txt",
            "partnerships_and_case_studies": f"{_KNOWDOCS}/partnerships_and_case_studies.txt",
            "auditor_report_and_opinions": f"{_KNOWDOCS}/auditor_report_and_opinions.txt",
            "consolidated_financial_statements": f"{_KNOWDOCS}/consolidated_financial_statements.txt",
            "notes_acctg_policies_and_revenue": f"{_KNOWDOCS}/notes_acctg_policies_and_revenue.txt",
            "critical_estimates_and_market_risk": f"{_KNOWDOCS}/critical_estimates_and_market_risk.txt",
            "liquidity_and_capital_resources": f"{_KNOWDOCS}/liquidity_and_capital_resources.txt",
            "operating_margin_and_income": f"{_KNOWDOCS}/operating_margin_and_income.txt",
            "benefits_stock_comp_segments": f"{_KNOWDOCS}/benefits_stock_comp_segments.txt",
            "business_combos_investments_ppe": f"{_KNOWDOCS}/business_combos_investments_ppe.txt",
            "fair_value_oci_commitments": f"{_KNOWDOCS}/fair_value_oci_commitments.txt",
            "income_taxes_and_derivatives": f"{_KNOWDOCS}/income_taxes_and_derivatives.txt",
            "leases_goodwill_accrued_debt": f"{_KNOWDOCS}/leases_goodwill_accrued_debt.txt",
            "risk_factors_market_and_operations": f"{_KNOWDOCS}/risk_factors_market_and_operations.txt",
            "risk_factors_cyber_currency_climate": f"{_KNOWDOCS}/risk_factors_cyber_currency_climate.txt",
            "risk_factors_legal_tax_governance": f"{_KNOWDOCS}/risk_factors_legal_tax_governance.txt",
            "directors_and_board_committees": f"{_KNOWDOCS}/directors_and_board_committees.txt",
            "equity_dividends_performance": f"{_KNOWDOCS}/equity_dividends_performance.txt",
            "md_a_exec_summary_and_revenues": f"{_KNOWDOCS}/md_a_exec_summary_and_revenues.txt",
            "results_of_operations_detail": f"{_KNOWDOCS}/results_of_operations_detail.txt",
            # Full report — single combined .txt file for single-agent access
            "annual_report_2024": "coded_tools/annual_report/complete_annual_report_2024.txt",
        }

    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Union[Dict[str, Any], str]:
        """
        :param args: An argument dictionary with the following keys:
            - "app_name" (str): The section or file key to retrieve.

        :param sly_data: A dictionary whose keys are defined by the agent hierarchy,
            but whose values are meant to be kept out of the chat stream.

            This dictionary is largely to be treated as read-only.
            It is possible to add key/value pairs to this dict that do not
            yet exist as a bulletin board, as long as the responsibility
            for which coded_tool publishes new entries is well understood
            by the agent chain implementation and the coded_tool implementation
            adding the data is not invoke()-ed more than once.

            Keys expected for this implementation are:
                None

        :return:
            If successful:
                A dictionary containing extracted text with the keys:
                - "files": A dict mapping file names to their extracted text.
            Otherwise:
                A text string error message in the format:
                "Error: <error message>"
        """
        app_name: str = args.get("app_name", None)
        logger.debug("App name: %s", app_name)
        if app_name is None:
            logger.error("No app name provided.")
            return "Error: No app name provided."
        path = self.docs_path.get(app_name, self.default_path)

        if not isinstance(path, (str, bytes, os.PathLike)):
            raise TypeError(f"Expected str, bytes, or os.PathLike object, got {type(path).__name__} instead")

        docs = {}

        # Handle single-file paths (file-level app_names)
        if os.path.isfile(path):
            if path.lower().endswith(".pdf"):
                content = self.extract_pdf_content(path)
                docs[os.path.basename(path)] = content
            elif path.lower().endswith(".txt"):
                content = self.extract_txt_content(path)
                docs[os.path.basename(path)] = content
        else:
            # Walk directory (section-level app_names)
            for root, _, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    if file.lower().endswith(".pdf"):
                        content = self.extract_pdf_content(file_path)
                        rel_path = os.path.relpath(file_path, path)
                        docs[rel_path] = content
                    elif file.lower().endswith(".txt"):
                        content = self.extract_txt_content(file_path)
                        rel_path = os.path.relpath(file_path, path)
                        docs[rel_path] = content

        if not docs:
            logger.error("No PDF or text files found in the path: %s", path)
            return "ERROR: No PDF or text files found in the path."
        return {"files": docs}

    async def async_invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Union[Dict[str, Any], str]:
        """
        Runs the synchronous invoke method in a thread to avoid blocking the event loop.
        """
        return await asyncio.to_thread(self.invoke, args, sly_data)

    @staticmethod
    def extract_pdf_content(pdf_path: str) -> str:
        """
        Extract text from a PDF file using pypdf, while attempting to preserve
        pagination (by inserting page headers).

        :param pdf_path: Full path to the PDF file.
        :return: Extracted text from the PDF.
        """
        text_output = []
        try:
            reader = PdfReader(pdf_path)
            for page_num, page in enumerate(reader.pages):
                # Add a page header for pagination
                text_output.append(f"\n\n--- Page {page_num + 1} ---\n\n")
                # Extract text from the page (fall back to empty string if None)
                page_text = page.extract_text() or ""
                text_output.append(page_text)
        except (PyPdfError, OSError) as e:
            error = f"Error reading PDF {pdf_path}: {e}"
            logger.error(error)
            return f"ERROR: {error}"

        return "".join(text_output)

    @staticmethod
    def extract_txt_content(txt_path: str) -> str:
        """
        Extract text from a plain text file.

        :param txt_path: Full path to the TXT file.
        :return: Content of the text file.
        """
        try:
            with open(txt_path, "r", encoding="utf-8") as f:
                return f.read()
        except OSError as e:
            error = f"Error reading TXT {txt_path}: {e}"
            logger.error(error)
            return f"ERROR: {error}"
