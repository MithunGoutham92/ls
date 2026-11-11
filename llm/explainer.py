"""LS.6 Explainer: explains a paper to a reader who is not an expert, with one quote as evidence.

Function: explain(paper_text, audience)

Input:
    paper_text (str): the paper's abstract, one numbered sentence per line ([S1], [S2], ...).
    audience (str): who will read the explanation, such as "a high school student".

Output (dict):
    explanation (str): two to four short sentences in plain words, with no new facts.
    quote (str): the sentence of the paper that the explanation leans on most,
                 copied word for word (without the [S1] tag).
    Sample: {"explanation": "Cameras on self-driving cars see badly in fog. ...",
             "quote": "Cameras fail in fog."}

Raises ValueError if the LLM's answer can't be used.
Test it: python3 llm/explainer.py      Score it: python3 score.py explainer
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


def build_prompt(paper_text, audience):
    prompt = f"""<instruction>{instruction}</instruction>
<context>{context}</context>
<examples>{examples}</examples>
<output_format>{output_format}</output_format>
<query>Audience: {audience}
Paper:
{paper_text}
Output:</query>"""
    return prompt


def explain(paper_text, audience):
    # TODO: write this function. The docstring at the top of this file is the contract.
    # 1. build_prompt(...), call
    #    ollama.generate(model="llama3.2", prompt=prompt, format="json", options={"num_predict": 500}),
    #    and read the answer with read_json.
    # 2. Check it: explanation is a str that is not empty, and quote is a str that is not empty and is in paper_text, word for word.
    #    Ask again (up to 3 tries) if it fails, then raise ValueError.
    # 3. Return {"explanation": ..., "quote": ...}.
    raise NotImplementedError("explain is not written yet")


if __name__ == "__main__":
    paper = "[S1] Cameras fail in fog.\n[S2] We test a LiDAR detector on 300 foggy scenes.\n[S3] It finds 20% more cars."
    print(explain(paper, "a high school student"))
