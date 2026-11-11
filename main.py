"""LitScout: joins the five tools into one literature-review helper.

Run from the project folder:  python3 main.py
Type a paper number (1 to 10), "all" for every paper in data/cases.json, "search" for the queries, or "quit".
"""
from llm.details import extract
from llm.explainer import explain
from llm.screener import screen
from llm.search import build_queries
from llm.summarizer import summarize
from llm.utils import load_data

DATA = load_data("cases.json")
AUDIENCE = "a high school student"


def review(case):
    """Screens one paper. If it is included, prints its details, summary and explanation."""
    print("\nPaper " + str(case["id"]) + ": " + case["title"])
    decision = screen(case["paper_text"], DATA["research_question"], DATA["criteria"])
    print("Decision: " + decision["decision"] + " (" + decision["reason"] + ")")
    if decision["decision"] != "include":
        return
    details = extract(case["paper_text"])
    for key in ["task", "data", "method", "results"]:
        print(key.capitalize() + ": " + details[key]["value"] + '  "' + details[key]["quote"] + '"')
    print("Summary:")
    print(summarize(case["paper_text"]))
    explained = explain(case["paper_text"], AUDIENCE)
    print("For " + AUDIENCE + ": " + explained["explanation"])
    print('Evidence: "' + explained["quote"] + '"')


def run(command):
    try:
        if command == "search":
            print("Research question: " + DATA["research_question"])
            print("Queries:", build_queries(DATA["research_question"]))
        elif command == "all":
            for case in DATA["cases"]:
                review(case)
        else:
            found = False
            for case in DATA["cases"]:
                if str(case["id"]) == command:
                    review(case)
                    found = True
            if not found:
                print("Type a paper number from 1 to " + str(len(DATA["cases"])) + ", all, search or quit.")
    except NotImplementedError as error:
        print("Not ready yet:", error)
    except (ValueError, ConnectionError) as error:
        print("Sorry, that did not work. Please try again.", error)


def main():
    print("LitScout. Research question: " + DATA["research_question"])
    print("Type a paper number, all, search, or quit.")
    while True:
        command = input("\n> ").strip().lower()
        if command in ("quit", "exit"):
            break
        if command:
            run(command)


if __name__ == "__main__":
    main()
