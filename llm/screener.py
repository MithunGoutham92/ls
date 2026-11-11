"""LS.1 Screener: decides if a paper fits the research question.

Function: screen(paper_text, research_question, criteria)

Input:
    paper_text (str): the paper's abstract, one numbered sentence per line ([S1], [S2], ...).
    research_question (str): the question the review is about.
    criteria (str): which studies to include and which to exclude.
    Sample: "[S1] We detect cars in fog with a camera and LiDAR. [S2] ...",
            "How do rain, fog and snow affect computer-vision systems for driving?",
            "Include studies of camera, LiDAR or other sensor perception for driving ..."

Output (dict):
    decision (str): include or exclude.
    reason (str): one short sentence that names the criterion used.
    Sample: {"decision": "include", "reason": "It studies camera and LiDAR perception for driving in fog."}

Raises ValueError if the LLM's answer can't be used.
Test it: python3 llm/screener.py      Score it: python3 score.py screener
"""
import ollama

# This lets the file work both as "python3 llm/screener.py" and as "from llm.screener import ...".
if __package__:
    from .utils import read_json
else:
    from utils import read_json

DECISIONS = ["include", "exclude"]

instruction = """TODO: say who the LLM is and what it must do."""

context = """TODO: the labels, rules and facts the LLM needs."""

examples = """TODO: a few examples of input and the exact output you want."""

output_format = """TODO: the exact JSON the LLM must return."""


def build_prompt(paper_text, research_question, criteria):
    prompt = f"""<instruction>{instruction}</instruction>
<context>{context}
Research question: {research_question}
Criteria: {criteria}</context>
<examples>{examples}</examples>
<output_format>{output_format}</output_format>
<query>Paper: {paper_text}
Output:</query>"""
    return prompt


def screen(paper_text, research_question, criteria):
    # TODO: write this function. The docstring at the top of this file is the contract.
    # 1. build_prompt(...), call
    #    ollama.generate(model="llama3.2", prompt=prompt, format="json", options={"num_predict": 500}),
    #    and read the answer with read_json.
    # 2. Check it: answer["decision"] is in DECISIONS and reason is a str.
    #    Ask again (up to 3 tries) if it fails, then raise ValueError.
    # 3. Return {"decision": ..., "reason": ...}.
    raise NotImplementedError("screen is not written yet")


if __name__ == "__main__":
    paper = input("Paper text: ")
    question = "How do rain, fog and snow affect computer-vision systems for driving?"
    criteria = "Include studies of camera or LiDAR perception for driving in rain, fog or snow. Exclude weather science."
    print(screen(paper, question, criteria))
