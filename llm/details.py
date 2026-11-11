"""LS.2 Detail: pulls out the task, data, method and results of a paper, each with an exact quote.

Function: extract(paper_text)

Input:
    paper_text (str): the paper's abstract, one numbered sentence per line ([S1], [S2], ...).

Output (dict): four keys, task, data, method and results. Each value is a dict with:
    value (str): a short phrase in your own words.
    quote (str): the sentence of the paper that shows it, copied word for word (without the [S1] tag).
    Sample: {"task": {"value": "3D object detection in fog", "quote": "We detect cars in fog."}, ...}

Every quote must be found in the paper text, word for word.
Raises ValueError if the LLM's answer can't be used.
Test it: python3 llm/details.py      Score it: python3 score.py details
"""
import ollama

if __package__:
    from .utils import read_json
else:
    from utils import read_json

KEYS = ["task", "data", "method", "results"]

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


def extract(paper_text):
    # TODO: write this function. The docstring at the top of this file is the contract.
    # 1. build_prompt(...), call
    #    ollama.generate(model="llama3.2", prompt=prompt, format="json", options={"num_predict": 500}),
    #    and read the answer with read_json.
    # 2. Check it: every key in KEYS is a dict with a str value and a quote that is not empty and is in paper_text, word for word.
    #    Ask again (up to 3 tries) if it fails, then raise ValueError.
    # 3. Return a dict with, for each key, {"value": ..., "quote": ...}.
    raise NotImplementedError("extract is not written yet")


if __name__ == "__main__":
    paper = "[S1] Cameras fail in fog.\n[S2] We test a LiDAR detector on 300 foggy scenes.\n[S3] It finds 20% more cars."
    print(extract(paper))
