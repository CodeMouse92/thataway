"""Parse and interpret targets to open."""

from enum import Enum, auto
import re
from typing import Tuple

url_regex = re.compile(r'(https?:\/{2}|file:\/{3})([^\/]+)\/?')


class TargetType(Enum):
    URL = auto()


def determine_target_type(target: str) -> TargetType:
    match = url_regex.match(target)
    if match is not None:
        return TargetType.URL
    else:
        raise ValueError("Unknown target type.")


def parse_url(target: str) -> str:
    match = url_regex.match(target)
    if match:
        return match.group(2)
    return ""


def parse(target: str) -> Tuple[TargetType, str]:
    target_type = determine_target_type(target)
    result = ''

    if target_type == TargetType.URL:
        result = parse_url(target)

    return (target_type, result)
