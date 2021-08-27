from collections import Counter
from itertools import chain, zip_longest
import pathlib
import json

from appdirs import user_config_dir

from thataway.targets import TargetType

config_dir = pathlib.Path(user_config_dir('thataway'))
rules_file = config_dir / 'rules.json'


def find_rule(target_type, target) -> str:
    if target_type == TargetType.URL:
        return find_url_rule(target)
    return ''


def find_url_rule(target) -> str:
    with rules_file.open('r') as file:
        data = json.load(file)
        rules = data['url']

    if not isinstance(rules, dict):
        raise RuntimeError("rules file must be a key-pair JSON file")

    candidates = Counter()
    longest = 0
    for pattern in rules.keys():
        zipper = zip_longest(
            reversed(target.split('.')),
            reversed(pattern.split('.')),
            fillvalue=''
        )
        no_wildcard = True
        for t, p in zipper:
            if p == t:
                # Exact match, proceed
                candidates.update([pattern])
            elif p == '*':
                # Wildcard match, candidate
                if pattern not in candidates:
                    candidates.update([pattern])
                no_wildcard = False
            else:
                del candidates[pattern]
                break
        else:
            # Track length of longest candidate pattern
            longest = max(longest, len(pattern.split('.')))
            if no_wildcard:
                # Full exact match bonus
                candidates[pattern] = longest + 1

    +candidates  # remove zero and missing
    print(candidates)
    best_match = candidates.most_common()[0][0]
    return rules[best_match]


def add_url_rule(rule: str, cmd: str):
    try:
        with rules_file.open('r') as file:
            data = json.load(file)
            try:
                rules = data['url']
            except KeyError:
                rules = {}
    except FileNotFoundError:
        data = {}
        rules = {}

    rules[rule] = cmd
    data['url'] = rules

    with rules_file.open('w') as file:
        json.dump(data, file)


def add_rule(target_type: str, rule: str, cmd: str):
    config_dir.mkdir(exist_ok=True)
    if target_type == 'url':
        add_url_rule(rule, cmd)
    else:
        raise ValueError(f"Unknown target type {target_type}.")
