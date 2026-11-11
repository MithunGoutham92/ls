"""Scores one tool on the 10 given papers in data/cases.json and on your own papers. Do not change this file.

Run from the project folder:
    python3 score.py screener            the 10 given papers, then yours
    python3 score.py screener given      the 10 given papers only
    python3 score.py screener mine       your papers only
    python3 score.py screener 3          given paper 3 only
    python3 score.py screener mine 3     your paper 3 only
Tools: screener, details, summarizer, search, explainer
Your papers are in data/my_cases/<tool>.json, such as data/my_cases/screener.json. Write 30 of them.
"""
import json
import re
import sys

from llm.utils import load_data, split_sentences

GOAL = 30         # write 30 of your own, for 40 in all

DATA = load_data("cases.json")
QUERIES = []      # Search runs once, then every paper is checked against its queries.


def check_screener(case):
    from llm.screener import screen
    answer = screen(case["paper_text"], DATA["research_question"], DATA["criteria"])
    expected = case["expected"]["decision"]
    return answer["decision"] == expected, f"decision {answer['decision']!r}, expected {expected!r}: {answer['reason']}"


def check_details(case):
    from llm.details import extract
    answer = extract(case["paper_text"])
    not_found = []
    for key in ["task", "data", "method", "results"]:
        if answer[key]["quote"] not in case["paper_text"]:
            not_found.append(key)
    values = []
    for key in ["task", "data", "method", "results"]:
        values.append(answer[key]["value"])
    return not not_found, f"quotes not in the paper: {not_found}; values {values}"


def check_summarizer(case):
    from llm.summarizer import summarize
    summary = summarize(case["paper_text"])
    lines = summary.strip().splitlines()
    bad = []
    for line in lines:
        tag = re.search(r"\[(S\d+)\]\s*$", line)
        if not line.startswith("- ") or not tag or "[" + tag.group(1) + "]" not in case["paper_text"]:
            bad.append(line)
    ok = len(lines) == 3 and not bad
    return ok, f"{len(lines)} lines, lines without a real [S#]: {bad} -> {summary!r}"


def matches(query, text):
    """True if every word of the query starts a word in the text (so "fog" matches "foggy")."""
    for word in query.lower().split():
        if not re.search(r"\b" + re.escape(word), text.lower()):
            return False
    return True


def check_search(case):
    from llm.search import build_queries
    if not QUERIES:
        QUERIES.extend(build_queries(DATA["research_question"]))
        print("Queries:", QUERIES)
    text = case["title"] + " " + case["paper_text"]
    found_by = []
    for query in QUERIES:
        if matches(query, text):
            found_by.append(query)
    expected = case["expected"]["decision"]
    if expected == "include":
        return bool(found_by), f"include paper, found by {found_by} (should be found)"
    return not found_by, f"exclude paper, found by {found_by} (should not be found)"


def check_explainer(case):
    from llm.explainer import explain
    answer = explain(case["paper_text"], "a high school student")
    words = len(answer["explanation"].split())
    ok = answer["quote"] in case["paper_text"] and 10 <= words <= 100
    return ok, f"quote found: {answer['quote'] in case['paper_text']}, {words} words -> {answer['explanation']!r}"


CHECKS = {"screener": check_screener, "details": check_details, "summarizer": check_summarizer,
          "search": check_search, "explainer": check_explainer}


# ---------------------------------------------------------------------------
# Your own papers: data/my_cases/<tool>.json, a list of papers with these fields.
# "text" is text in quote marks, and a list of words means the value must be one of them.
# Any other field, such as "note" or "source", is allowed and not used.

DECISIONS = ["include", "exclude"]
PAPER = {"title": "text", "abstract": "text"}
FIELDS = {
    "screener": {"title": "text", "abstract": "text", "decision": DECISIONS},
    "details": PAPER,
    "summarizer": PAPER,
    "search": {"title": "text", "abstract": "text", "decision": DECISIONS},
    "explainer": PAPER,
}


def extra_problems(tool, case):
    """Checks that need more than one field."""
    problems = []
    sentences = len(split_sentences(case["abstract"]))
    if sentences < 3:
        problems.append(f"the abstract has {sentences} sentences: use the paper's whole abstract (3 or more)")
    return problems


def as_paper(case):
    """Turns your paper into the form of the given papers: the abstract as numbered sentences [S1], [S2], ..."""
    lines = []
    for number, sentence in enumerate(split_sentences(case["abstract"]), start=1):
        lines.append(f"[S{number}] {sentence}")
    return {"id": case["id"], "title": case["title"], "paper_text": "\n".join(lines),
            "expected": {"decision": case.get("decision")}}


def mine_screener(case):
    return check_screener(as_paper(case))


def mine_details(case):
    return check_details(as_paper(case))


def mine_summarizer(case):
    return check_summarizer(as_paper(case))


def mine_search(case):
    return check_search(as_paper(case))


def mine_explainer(case):
    return check_explainer(as_paper(case))


MINE = {"screener": mine_screener, "details": mine_details, "summarizer": mine_summarizer,
        "search": mine_search, "explainer": mine_explainer}


# ---------------------------------------------------------------------------
# Reading and checking your own papers

def field_problem(value, kind):
    """Returns what is wrong with one field of your paper, or "" if nothing is wrong."""
    if isinstance(kind, list):
        if value not in kind:
            return "must be one of: " + ", ".join(json.dumps(choice) for choice in kind)
    elif kind == "text":
        if not isinstance(value, str) or not value.strip():
            return "must be text in double quotes, and not empty"
    elif kind == "list of text":
        if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
            return 'must be a list of text, such as ["a", "b"], or [] for none'
    elif kind == "true or false":
        if not isinstance(value, bool):
            return "must be true or false, with no quote marks"
    elif kind == "list":
        if not isinstance(value, list):
            return "must be a list, in [ ]"
    return ""


def case_problems(tool, number, case):
    """Returns a list of the mistakes in one of your papers."""
    if not isinstance(case, dict):
        return [f"your paper {number}: must be {{ ... }}, like the sample paper"]
    problems = []
    for name, kind in FIELDS[tool].items():
        if name not in case:
            problems.append(f'your paper {number}: has no "{name}"')
        elif field_problem(case[name], kind):
            problems.append(f'your paper {number}: "{name}" {field_problem(case[name], kind)}')
    if not problems:
        for problem in extra_problems(tool, case):
            problems.append(f"your paper {number}: {problem}")
    return problems


def load_my_cases(tool):
    """Reads your papers from data/my_cases/<tool>.json and numbers them 1, 2, 3, ...
    If the file has a mistake, it prints what is wrong and returns None."""
    name = f"my_cases/{tool}.json"
    try:
        cases = load_data(name)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as error:
        print(f"data/{name} is not valid JSON: {error.msg}, on line {error.lineno}.")
        print("Look for a missing comma, quote mark or bracket on that line or the line before it.")
        return None
    if not isinstance(cases, list):
        print(f"data/{name} must be a list of papers: it starts with [ and ends with ].")
        return None
    problems = []
    for number, case in enumerate(cases, start=1):
        problems += case_problems(tool, number, case)
    if problems:
        print(f"data/{name} has mistakes:")
        for problem in problems:
            print("  " + problem)
        return None
    for number, case in enumerate(cases, start=1):
        case["id"] = number
    return cases


def run(check, cases, label):
    """Runs one check on each paper and prints PASS or FAIL.
    Returns how many passed, or None if the tool is not written yet."""
    passed = 0
    for case in cases:
        try:
            ok, note = check(case)
        except NotImplementedError as error:
            print(error)
            return None
        except Exception as error:
            ok, note = False, f"error: {error}"
        if ok:
            passed += 1
            print(f"{label} {case['id']}: PASS  {note}")
        else:
            print(f"{label} {case['id']}: FAIL  {note}")
    return passed


def main():
    args = sys.argv[1:]
    if not args or args[0] not in CHECKS:
        print("Usage: python3 score.py TOOL [given | mine] [NUMBER]   TOOL is one of:", ", ".join(CHECKS))
        return
    tool = args[0]
    which = "all"
    if len(args) > 1 and args[1] in ("given", "mine"):
        which = args[1]
        args = args[:1] + args[2:]
    number = None
    if len(args) > 1:
        number = args[1]
        if which == "all":
            which = "given"

    given = []
    mine = []
    if which in ("all", "given"):
        given = load_data("cases.json")["cases"]
    if which in ("all", "mine"):
        mine = load_my_cases(tool)
        if mine is None:
            return
    count_mine = len(mine)
    if number is not None:
        given = [case for case in given if str(case["id"]) == number]
        mine = [case for case in mine if str(case["id"]) == number]
        if not given and not mine:
            if which == "given":
                print(f"There is no given paper {number}.")
            else:
                print(f"There is no paper {number} in data/my_cases/{tool}.json.")
            return
    if which == "mine" and not mine:
        print(f"data/my_cases/{tool}.json has no papers yet.")
        return

    passed_given = 0
    passed_mine = 0
    if given:
        passed_given = run(CHECKS[tool], given, "Paper")
        if passed_given is None:
            return
    if mine:
        if given:
            print(f"Given papers: {passed_given} of {len(given)}")
        passed_mine = run(MINE[tool], mine, "Your paper")
        if passed_mine is None:
            return
        if given:
            print(f"Your papers: {passed_mine} of {len(mine)}")
    print(f"Score: {passed_given + passed_mine} of {len(given) + len(mine)}")
    if which != "given" and number is None and count_mine < GOAL:
        print(f"You have {count_mine} of your {GOAL} papers in data/my_cases/{tool}.json.")


if __name__ == "__main__":
    main()
