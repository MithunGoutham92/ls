"""LS.3 Summarizer: writes a three-point summary of a paper. Each point names the sentence it comes from.

Function: summarize(paper_text)

Input:
    paper_text (str): the paper's abstract, one numbered sentence per line ([S1], [S2], ...).

Output (str): three lines, each "- point [S#]", where S# is a sentence of the paper that backs up the point.
    Sample: "- Cameras fail in fog. [S1]\n- The paper tests a LiDAR detector. [S2]\n- It finds 20% more cars. [S3]"

Raises ValueError if the LLM's answer can't be used.
Test it: python3 llm/summarizer.py      Score it: python3 score.py summarizer
"""
import ollama

if __package__:
    from .utils import read_json
else:
    from utils import read_json

instruction = """TODO: say who the LLM is and what it must do."""

context = """TODO: the labels, rules and facts the LLM needs."""

examples = """TODO: a few examples of input and the exact output you want."""

output_format = """TODO: the exact JSON the LLM must return."""


def build_prompt(paper_text):
    prompt = f"""<instruction>{instruction}</instruction>
<context>{context}</context>
<examples>{examples}</examples>
<output_format>{output_format}</output_format>
<query>Paper:
{paper_text}
Output:</query>"""
    return prompt


def summarize(paper_text):
    # TODO: write this function. The docstring at the top of this file is the contract.
    # 1. build_prompt(paper_text), call
    #    ollama.generate(model="llama3.2", prompt=prompt, format="json", options={"num_predict": 500}),
    #    and read the answer with read_json. The LLM must answer in JSON, so ask for a list of three
    #    points, each with its text and the sentence it comes from (such as S2).
    # 2. Check it: three points, and each sentence number is in paper_text ("[S2]" in paper_text).
    #    Ask again (up to 3 tries) if not, then raise ValueError.
    # 3. Your code joins the points into the string the contract describes: three lines, each
    #    "- point [S#]". Return that string (not a dict).
    raise NotImplementedError("summarize is not written yet")


if __name__ == "__main__":
    paper = "[S1] Cameras fail in fog.\n[S2] We test a LiDAR detector on 300 foggy scenes.\n[S3] It finds 20% more cars."
    print(summarize(paper))
