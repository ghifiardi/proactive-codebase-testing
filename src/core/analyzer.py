"""Core analyzer using Claude API."""

import os
import json
import time
import logging
from typing import List, Optional, Dict, Any
from anthropic import Anthropic
from dotenv import load_dotenv

from .findings import Finding, FindingType, Severity, Location, AnalysisResult
from .prompts import get_prompt

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


class CodeAnalyzer:
    """Analyzer that uses Claude API to analyze code."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-3-haiku-20240307",
        timeout: int = 30,
        max_retries: int = 3,
    ):
        """Initialize analyzer.

        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
            model: Claude model to use
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries on failure
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY not provided. Set it in environment or pass as argument."
            )

        self.client = Anthropic(api_key=self.api_key)
        self.model = model
        self.timeout = timeout
        self.max_retries = max_retries

    def _parse_finding(self, finding_data: Dict[str, Any], file_path: str) -> Finding:
        """Parse a single finding from API response.

        Args:
            finding_data: Finding data from API
            file_path: Path to the file being analyzed

        Returns:
            Finding object
        """
        # Map severity string to enum
        severity_str = finding_data.get("severity", "medium").lower()
        severity_map = {
            "critical": Severity.CRITICAL,
            "high": Severity.HIGH,
            "medium": Severity.MEDIUM,
            "low": Severity.LOW,
            "info": Severity.INFO,
        }
        severity = severity_map.get(severity_str, Severity.MEDIUM)

        # Map type string to enum
        type_str = finding_data.get("type", "QUALITY").upper()
        type_map = {
            "SECURITY": FindingType.SECURITY,
            "BUG": FindingType.BUG,
            "QUALITY": FindingType.QUALITY,
            "PERFORMANCE": FindingType.PERFORMANCE,
            "ACCESSIBILITY": FindingType.ACCESSIBILITY,
        }
        finding_type = type_map.get(type_str, FindingType.QUALITY)

        # Get location
        line = finding_data.get("line")
        location = Location(
            file_path=file_path,
            line=line,
            column=finding_data.get("column"),
            end_line=finding_data.get("end_line"),
            end_column=finding_data.get("end_column"),
        )

        return Finding(
            type=finding_type,
            severity=severity,
            message=finding_data.get("message", "Unknown issue"),
            location=location,
            remediation=finding_data.get("remediation"),
            confidence=finding_data.get("confidence", 0.8),
            code_snippet=finding_data.get("code_snippet"),
            rule_id=finding_data.get("rule_id"),
            metadata=finding_data.get("metadata", {}),
        )

    def _parse_api_response(self, response: str, file_path: str) -> List[Finding]:
        """Parse Claude API response into findings.

        Args:
            response: API response text
            file_path: Path to the file being analyzed

        Returns:
            List of Finding objects
        """
        findings = []

        try:
            # Try to extract JSON from markdown code blocks first
            import re
            json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response, re.DOTALL)
            if json_match:
                response = json_match.group(1)
            else:
                # Try to find JSON object in the response
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    response = json_match.group(0)
            
            # Try to parse as JSON
            data = json.loads(response)

            # Handle different response formats
            if isinstance(data, dict):
                findings_data = data.get("findings", [])
            elif isinstance(data, list):
                findings_data = data
            else:
                logger.warning(f"Unexpected response format: {type(data)}")
                return findings

            # Parse each finding
            for finding_data in findings_data:
                try:
                    finding = self._parse_finding(finding_data, file_path)
                    findings.append(finding)
                except Exception as e:
                    logger.error(f"Error parsing finding: {e}, data: {finding_data}")

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse API response as JSON: {e}")
            logger.debug(f"Response text: {response[:500]}")

        return findings

    def analyze_code(
        self,
        code: str,
        language: str,
        file_name: str = "unknown",
        analysis_type: str = "comprehensive",
    ) -> List[Finding]:
        """Analyze code using Claude API.

        Args:
            code: Source code to analyze
            language: Programming language
            file_name: Name of the file
            analysis_type: Type of analysis (security, bugs, quality, comprehensive)

        Returns:
            List of Finding objects
        """
        if not code or not code.strip():
            logger.warning(f"Empty code provided for {file_name}")
            return []

        # Get prompt
        prompt = get_prompt(analysis_type, file_name, code, language)

        # Call Claude API with retries
        for attempt in range(self.max_retries):
            try:
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=4096,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    timeout=self.timeout,
                )

                # Extract text from response
                if hasattr(response, "content") and response.content:
                    response_text = response.content[0].text
                else:
                    logger.error("Empty response from Claude API")
                    return []

                # Parse findings
                findings = self._parse_api_response(response_text, file_name)
                logger.info(
                    f"Analysis complete for {file_name}: {len(findings)} findings"
                )
                return findings

            except Exception as e:
                logger.error(
                    f"Error calling Claude API (attempt {attempt + 1}/{self.max_retries}): {e}"
                )
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logger.error(f"Failed to analyze {file_name} after {self.max_retries} attempts")
                    return []

        return []

    def analyze_directory(
        self,
        directory: str,
        analysis_type: str = "comprehensive",
        parser=None,
    ) -> AnalysisResult:
        """Analyze all files in a directory.

        Args:
            directory: Directory path to analyze
            analysis_type: Type of analysis
            parser: CodeParser instance (will create if not provided)

        Returns:
            AnalysisResult with all findings
        """
        from .parser import CodeParser

        if parser is None:
            parser = CodeParser()

        start_time = time.time()
        all_findings = []
        files_analyzed = 0
        total_lines = 0

        # Get files to analyze
        files = parser.get_files_to_analyze(directory)
        logger.info(f"Found {len(files)} files to analyze")

        # Analyze each file
        for file_path in files:
            try:
                file_data = parser.analyze_file(file_path)
                if not file_data:
                    continue

                findings = self.analyze_code(
                    code=file_data["content"],
                    language=file_data["language"],
                    file_name=file_data["path"],
                    analysis_type=analysis_type,
                )

                all_findings.extend(findings)
                files_analyzed += 1
                total_lines += file_data["line_count"]

                logger.info(
                    f"Analyzed {file_path}: {len(findings)} findings, "
                    f"{file_data['line_count']} lines"
                )

            except Exception as e:
                logger.error(f"Error analyzing file {file_path}: {e}")

        analysis_time = time.time() - start_time

        return AnalysisResult(
            findings=all_findings,
            files_analyzed=files_analyzed,
            total_lines=total_lines,
            analysis_time_seconds=analysis_time,
            metadata={
                "directory": directory,
                "analysis_type": analysis_type,
                "model": self.model,
            },
        )

