"""Lightweight, deterministic analysis of build and error logs."""

import re
from collections import Counter
from typing import TypedDict


class LogAnalysis(TypedDict):
    """Structured results consumed by the AI summarizer."""

    message_counts: dict[str, int]
    important_errors: list[str]
    important_warnings: list[str]
    failure_indicators: list[str]
    build_status: str
    total_lines: int


LEVEL_PATTERN = re.compile(r"\b(ERROR|WARNING|FATAL|INFO)\b", re.IGNORECASE)
FAILURE_PATTERNS = (
    re.compile(r"\bBUILD\s+FAILED\b", re.IGNORECASE),
    re.compile(r"\bBUILD\s+FAILURE\b", re.IGNORECASE),
    re.compile(r"\bCOMPILATION\s+FAILED\b", re.IGNORECASE),
    re.compile(
        r"\bFAILED\s+TO\s+(?:BUILD|COMPILE|RESOLVE|DOWNLOAD|INSTALL)\b",
        re.IGNORECASE,
    ),
    re.compile(r"\b(?:TASK|STEP)\b.*\bFAILED\b", re.IGNORECASE),
    re.compile(
        r"\b(?:EXIT(?:ED)?|FINISHED|RETURNED)\s+WITH\s+"
        r"(?:A\s+)?(?:NON[- ]ZERO|ERROR)\s+CODE\b",
        re.IGNORECASE,
    ),
    re.compile(r"\bPROCESS\s+FINISHED\s+WITH\s+EXIT\s+CODE\s+[1-9]\d*\b", re.IGNORECASE),
)
SUCCESS_PATTERNS = (
    re.compile(r"\bBUILD\s+SUCCESSFUL\b", re.IGNORECASE),
    re.compile(r"\bBUILD\s+SUCCEEDED\b", re.IGNORECASE),
    re.compile(r"\bBUILD\s+SUCCESS\b", re.IGNORECASE),
)


def analyze_log(log_text: str) -> LogAnalysis:
    """Count log levels and extract likely errors, warnings, and build failures."""
    counts: Counter[str] = Counter(
        {"ERROR": 0, "WARNING": 0, "FATAL": 0, "INFO": 0}
    )
    important_errors: list[str] = []
    important_warnings: list[str] = []
    failure_indicators: list[str] = []
    has_success_indicator = False

    for raw_line in log_text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        levels = {match.upper() for match in LEVEL_PATTERN.findall(line)}
        for level in levels:
            counts[level] += 1
        if levels.intersection({"ERROR", "FATAL"}):
            important_errors.append(line)
        if "WARNING" in levels:
            important_warnings.append(line)

        if any(pattern.search(line) for pattern in FAILURE_PATTERNS):
            failure_indicators.append(line)
        if any(pattern.search(line) for pattern in SUCCESS_PATTERNS):
            has_success_indicator = True

    if failure_indicators or counts["FATAL"] > 0:
        build_status = "Likely failed"
    elif has_success_indicator:
        build_status = "Likely successful"
    elif counts["ERROR"] > 0:
        build_status = "Errors found; build status unclear"
    else:
        build_status = "Unknown"

    return {
        "message_counts": dict(counts),
        "important_errors": important_errors,
        "important_warnings": important_warnings,
        "failure_indicators": failure_indicators,
        "build_status": build_status,
        "total_lines": len(log_text.splitlines()),
    }