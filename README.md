# LitScout

LitScout helps with a literature review. It turns a research question into search queries, screens papers against the criteria, and for each included paper pulls out details with exact quotes, writes a summary that names its sentences, and explains the paper in plain words.

## What the assistant does

`python3 main.py` uses the tools like this.

When you type a paper number (or `all` for every paper):

1. **Screener** (`screen`): includes or excludes the paper, with a reason.
2. If the paper is included: **Detail** (`extract`) pulls out the task, data, method and results, each with
   an exact quote.
3. **Summarizer** (`summarize`) writes three points, each with the sentence it comes from.
4. **Explainer** (`explain`) explains the paper in plain words for a high school student, with one quote.

When you type `search`:

5. **Search** (`build_queries`) turns the research question into search queries.

Each tool is one function in one file in `llm/`. When every tool works, the whole assistant works.
`main.py` stops at the first tool that is not written yet and says "Not ready yet", so in Phase 1 you test
your own tool on its own (see "Test and score your tool").

## Get the code

1. On this project's GitHub page, click the green **Code** button, then **Download ZIP**.
2. Unzip the file. You get a folder whose name ends in `-main`, such as `LitScout-main`.
   On Windows, "Extract All" can put it inside a second folder with the same name: use the folder that has `main.py` in it.
3. In VS Code, choose **File > Open Folder...** and pick that folder. The VS Code Terminal then starts in it.
   Run every command from this folder.

## Set up

1. Install Ollama from https://ollama.com and open it. It must be running whenever you use the project.
2. In the Terminal, run `ollama pull llama3.2`. This downloads the model (about 2 GB), once.
3. Install the Python package: `python3 -m pip install -r requirements.txt`.
4. Check it: run `python3 main.py`. It starts and waits for you to type. Until the tools are written, it says
   "Not ready yet" for anything you type. Type `quit` to stop.

On Windows, type `py` where this README says `python3`. For example: `py -m pip install -r requirements.txt`.

## Your work, step by step

Use your own file and tool name where this list says `llm/screener.py` and `screener`.

1. Do "Get the code" and "Set up" above.
2. Find your role in "Find your file". Open your tool file and read its docstring: it is the contract.
3. Read your role in "Your role" below. It says what score.py checks and gives tips.
4. In your tool file, write the four prompt parts (`instruction`, `context`, `examples`, `output_format`).
   They start as TODO.
5. Follow the TODO comments in your function. Write the code, then delete the `raise NotImplementedError` line.
6. Run `python3 llm/screener.py` and try your function on one input.
7. Run `python3 score.py screener given`. Change your prompt and code until most of the 10 given
   papers pass. The teacher's version scores 8 to 10 of 10.
8. Add your 30 test papers in your cases file (see the section "Add 30 test papers of your own"), then run
   `python3 score.py screener` for the score out of 40.
9. Save your tool file and your cases file. Give them to your teacher or team.

When your function and your prompt parts are written, your file does the same job as the teacher's
`Completed` version.

## Find your file

Find your role in the table. You change two files: you write your function in your tool file, and you add
30 test papers in your cases file. **Do not change any other file.**

| Role | Your tool file | Write this function | Your cases file | Score it |
|---|---|---|---|---|
| LS.1 Screener | `llm/screener.py` | `screen` | `data/my_cases/screener.json` | `python3 score.py screener` |
| LS.2 Detail | `llm/details.py` | `extract` | `data/my_cases/details.json` | `python3 score.py details` |
| LS.3 Summarizer | `llm/summarizer.py` | `summarize` | `data/my_cases/summarizer.json` | `python3 score.py summarizer` |
| LS.5 Search | `llm/search.py` | `build_queries` | `data/my_cases/search.json` | `python3 score.py search` |
| LS.6 Explainer | `llm/explainer.py` | `explain` | `data/my_cases/explainer.json` | `python3 score.py explainer` |

There is no LS.4 role.

## What is in your file

Open your file. From top to bottom it has:

1. **The docstring**, the text between the `"""` marks at the top. **It is the contract**: the inputs, the
   output and a sample of each. Do not change the function name, its inputs or the keys of its output,
   because `main.py` and `score.py` use them.
2. **The import lines.** The `if __package__:` lines let the file run on its own and from `main.py`.
   Leave them as they are. To use one more function from `utils.py`, add its name to both import lines.
3. **Four prompt parts**: `instruction`, `context`, `examples` and `output_format`. Each one says TODO. Write them.
4. **`build_prompt`**: already written. It puts the four parts and the input into one prompt. Do not change it.
5. **Your function.** It has TODO comments with the steps, and `raise NotImplementedError(...)`.
   Write the function, then delete the `raise NotImplementedError` line.
6. **A small test** at the bottom, under `if __name__ == "__main__":`. Some tests ask you to type an input.

You may add your own helper functions to your file, and you may import more from `utils.py`.

## How every tool works

Every tool follows the same steps:

1. Make the prompt: `prompt = build_prompt(...)`, with your function's inputs.
2. Call the LLM:
   `output = ollama.generate(model="llama3.2", prompt=prompt, format="json", options={"num_predict": 500})`.
   `format="json"` makes the LLM answer in JSON. `num_predict` stops an answer that runs on too long.
3. Turn the answer into a dict: `answer = read_json(output.response)`. If the answer is not complete JSON,
   you get `{}`.
4. Check the answer: are all the keys there, and are the values allowed (for example, a word from your list)?
   If not, ask again. Use a `while` loop that stops after 3 tries.
5. If the 3rd answer is still not usable, `raise ValueError("...")` with a short message. `main.py` then says
   "Sorry, we couldn't process this" and saves nothing.
6. Return what the contract says.

Some tools need more than one LLM call, or code that does part of the work. The TODO comments in your
function and the tips for your role below say how.

## Your role

### LS.1 Screener: `llm/screener.py`

Write `screen(paper_text, research_question, criteria)`. It gets a paper's abstract, the research question and the criteria, and returns `{"decision": ..., "reason": ...}`.

- **score.py passes a given paper when** `decision` is the one in the answer key.
- **Your papers** (`data/my_cases/screener.json`): `title` and `abstract`: a real paper from arxiv.org, with its whole abstract as plain text (score.py numbers the sentences [S1], [S2], ...). `decision`: `"include"` or `"exclude"`, for the research question and criteria in `data/cases.json`. Add `"source"` with the paper's link.
- **Tip:** `build_prompt` already puts the research question and the criteria into the prompt. Use `context` and `examples` to show how to apply them.
- **Tip:** The five excluded papers still talk about rain or fog (weather science, radio links), so "it mentions fog" is not enough to include a paper.
- **Tip:** `DECISIONS` at the top of your file lists the two allowed words.

### LS.2 Detail: `llm/details.py`

Write `extract(paper_text)`. It returns four keys, `task`, `data`, `method` and `results`. Each value is `{"value": ..., "quote": ...}`.

- **score.py passes a given paper when** all four quotes are in the paper text, word for word.
- **Your papers** (`data/my_cases/details.json`): `title` and `abstract`: a real paper from arxiv.org, with its whole abstract as plain text (score.py numbers the sentences [S1], [S2], ...). `decision` is not needed for your tool. Add `"source"` with the paper's link.
- **Tip:** `KEYS` at the top of your file lists the four keys.
- **Tip:** A quote is copied without its `[S1]` tag. Your code can check each quote with `quote in paper_text`, and ask again if one is not there.

### LS.3 Summarizer: `llm/summarizer.py`

Write `summarize(paper_text)`. It returns a **string** of three lines, each `- point [S#]`.

- **score.py passes a given paper when** there are exactly three lines, each `- point [S#]`, where S# is a sentence number the paper has.
- **Your papers** (`data/my_cases/summarizer.json`): `title` and `abstract`: a real paper from arxiv.org, with its whole abstract as plain text (score.py numbers the sentences [S1], [S2], ...). `decision` is not needed for your tool. Add `"source"` with the paper's link.
- **Tip:** The LLM answers in JSON, so ask it for the three points and their sentence numbers. Your code then builds the three lines.
- **Tip:** Check that each sentence number is in the paper, such as `"[S2]" in paper_text`.

### LS.5 Search: `llm/search.py`

Write `build_queries(research_question)`. It returns a **list** of three to five queries.

- **score.py passes a given paper when** an included paper is found by at least one of your queries, or an excluded paper is found by none of them. score.py makes your queries once and tries them on all 10 papers. A query finds a paper if every word of the query starts a word in the paper's title or text (so "fog" finds "foggy").
- **Your papers** (`data/my_cases/search.json`): `title` and `abstract`: a real paper from arxiv.org, with its whole abstract as plain text (score.py numbers the sentences [S1], [S2], ...). `decision`: `"include"` or `"exclude"`, for the research question and criteria in `data/cases.json`. Add `"source"` with the paper's link.
- **Tip:** Short queries find more papers. Pair one weather word with one or two driving or vision words, so that weather-science papers are not found.
- **Tip:** The LLM answers in JSON, so ask for one key, `queries`, with a list.

### LS.6 Explainer: `llm/explainer.py`

Write `explain(paper_text, audience)`. It returns `{"explanation": ..., "quote": ...}`. `main.py` uses the audience "a high school student".

- **score.py passes a given paper when** the quote is in the paper word for word, and the explanation has 10 to 100 words.
- **Your papers** (`data/my_cases/explainer.json`): `title` and `abstract`: a real paper from arxiv.org, with its whole abstract as plain text (score.py numbers the sentences [S1], [S2], ...). `decision` is not needed for your tool. Add `"source"` with the paper's link.
- **Tip:** Ask for plain words and no new facts.
- **Tip:** A quote is copied without its `[S1]` tag. Check that it is in `paper_text`, and ask again if it is not.

## Add 30 test papers of your own

The 10 given papers in `data/cases.json` are only a start. Add 30 more for your tool, so that it is
tested on 40 papers.

1. Open your cases file, such as `data/my_cases/screener.json`. It starts with one sample paper.
   Change the sample, or replace it with your own.
2. Add your papers after it. Each paper is `{ ... }` with the fields that "Your role" lists for your
   tool. Put a comma between two papers. The file looks like this:

```json
[
  {
    "title": "Lane detection for self-driving cars in heavy rain",
    "abstract": "Camera-based lane detection often fails in heavy rain, because raindrops and road spray hide the lane markings. We test three lane detectors on 500 camera images of rainy roads taken from a self-driving test car. A detector trained with simulated rain finds 15% more lane markings than the same detector trained only on dry roads.",
    "decision": "include",
    "note": "A made-up paper, only to show the format. Replace it with a real paper from arxiv.org, and add its link as \"source\"."
  },
  {
    "title": "...",
    "abstract": "...",
    "decision": "..."
  }
]
```

3. Run `python3 score.py screener mine` (with your tool's name). score.py first checks your file. If a
   paper has a missing field or a wrong value, it tells you which one and scores nothing until you fix it.

Rules for good test papers:

- Decide the right answer for each paper before you run your tool. Never change an answer to match
  what your tool says.
- Cover papers to include and papers to exclude, and make at least a quarter of your papers hard: papers where a careless
  tool would go wrong.
- Do not copy your test papers, or the 10 given papers, into the `examples` of your prompt.
  A test shows something only if the tool has not seen the answer.
- Use real papers from arxiv.org, and add `"source"` with each paper's link. Your team can share papers, because every LitScout cases file has the same fields.
- score.py does not use the fields `source` and `note`. Use `note` to say why a paper is hard.

## Test and score your tool

Use your own tool's name in these commands.

- `python3 llm/screener.py`: runs the small test at the bottom of your tool file.
- `python3 score.py screener`: runs your tool on the 10 given papers, then on your own papers.
  Each paper prints PASS or FAIL and what your tool returned. At the end you see the score on the given
  papers, the score on yours, and the total, such as `Score: 34 of 40`.
- `python3 score.py screener given` or `python3 score.py screener mine`: only the given papers,
  or only yours.
- `python3 score.py screener 3` runs given paper 3, and `python3 score.py screener mine 3` runs
  your paper 3. One paper is quicker while you change your prompt.
- An LLM does not give the same answer every time. Run score.py two or three times before you decide that a
  change made your prompt better.
- The teacher's version of each tool scores 8 to 10 of 10 on the given papers with llama3.2.

What the messages mean:

- `data/my_cases/... is not valid JSON ... on line 5`: look for a missing comma, quote mark or bracket on that
  line or the line before it. JSON needs double quotes, and `true`, `false` and `null` in small letters.
- `data/my_cases/... has mistakes`: the list under it says which of your papers has a missing field or a
  wrong value.
- `... is not written yet`: your function still has `raise NotImplementedError`.
- `FAIL  error: ...`: your function stopped with an error on that case. If it is your ValueError, the LLM gave
  3 answers your code could not use: make `output_format` and `examples` clearer.
- `Failed to connect to Ollama`: open the Ollama app, then try again.
- `model "llama3.2" not found`: run `ollama pull llama3.2`.
- `No module named 'ollama'`: do step 3 of "Set up".

To try another local model, download it with `ollama pull <name>` (the names are on https://ollama.com/search)
and change `model="llama3.2"` in your file. Score both models and compare.

## Files you do not change

- `llm/utils.py` (utils is short for utilities): functions that every tool can use. `load_data(name)` and `load_text(name)` read a file in `data/`, `save_data(name, data)` writes one, `split_sentences(text)` gives a list of sentences, and `read_json(text)` turns the LLM's answer into a dict (`{}` if the answer is not complete JSON).
- `llm/__init__.py`: makes `llm/` a package, so `main.py` can import your tool.
- `score.py`: checks your tool on the given papers and on yours.
- `main.py`: joins all the tools.
- `data/`: the given papers and the data that `main.py` saves. In `data/my_cases/`, change only your own cases file.

## Run the whole assistant

`python3 main.py`. Type a paper number, `all`, `search`, or `quit`.

## Data

- `data/cases.json`: the research question, the criteria and 10 labelled papers, used by score.py
- `data/my_cases/`: one cases file for each tool, such as `data/my_cases/screener.json`. Each starts with one sample; students add their own.

## Licence and sources

Titles and abstracts come from arXiv metadata, which is CC0 1.0. Each paper's arXiv link is in cases.json.

## Notes

- Five papers fit the research question and five do not. The five that do not still talk about rain or fog (weather science, radio links), so the Screener must read carefully.
- This project uses the local model llama3.2. Every call has `options={"num_predict": 500}`, so an answer that
  runs on too long stops instead of hanging your program.
