"""LS.5 Search: turns the research question into short search queries.

Function: build_queries(research_question)

Input:
    research_question (str): the question the review is about.
    Sample: "How do rain, fog and snow affect computer-vision systems for driving?"

Output (list of str): three to five queries. Each query is two to four words, and a paper matches the
    query only if it has every word. Use one weather word and one or two driving or vision words.
    Sample: ["fog driving camera", "snow lidar detection", "rain autonomous perception"]

Raises ValueError if the LLM's answer can't be used.
Test it: python3 llm/search.py      Score it: python3 score.py search
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


def build_prompt(research_question):
    prompt = f"""<instruction>{instruction}</instruction>
<context>{context}</context>
<examples>{examples}</examples>
<output_format>{output_format}</output_format>
<query>Question: {research_question}
Output:</query>"""
    return prompt


def build_queries(research_question):
    # TODO: write this function. The docstring at the top of this file is the contract.
    # 1. build_prompt(research_question), call
    #    ollama.generate(model="llama3.2", prompt=prompt, format="json", options={"num_predict": 500}),
    #    and read the answer with read_json. The LLM must answer in JSON, so ask for one key, queries,
    #    with a list of short queries.
    # 2. Check it: at least three queries, each a string that is not empty. Ask again (up to 3 tries)
    #    if not, then raise ValueError.
    # 3. Return the list (not a dict), with at most five queries.
    raise NotImplementedError("build_queries is not written yet")


if __name__ == "__main__":
    question = input("Research question: ")
    print(build_queries(question))
