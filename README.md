# LitScout

LitScout helps with a literature review. A researcher asks a research question through a speech to text app, and the assistant searches arXiv, reads the papers it finds, screens each one against the question, and explains in plain words why the best ones are worth reading. It can also check papers that someone recommended to the researcher, and say if each citation is real.

Every LLM call runs on your own computer using llama3.2 for consistency across teams and teammates.

## Goals

The assistant receives a researcher's request as a messy JSON object that looks like this:

```json
[
  {
    "question": "umm so like, how do self-driving cars, you know, see the road when it snows?",
    "papers": [
      "10.48550/arXiv.1706.03762",
      {"doi": "10.48550/arXiv.2101.99999", "title": "A paper my advisor told me about"}
    ]
  }
]
```

- `question` is the research question as the researcher **spoke** it, with filler words from speech-to-text input, such as "umm", "like" and "you know".
- `papers` is optional (it can be empty: `[]`). It holds papers that someone recommended to the researcher: an
  arXiv DOI, or a paper as JSON data with a `doi` and some of `title` and `abstract`, possibly incorrect.

The assistant must:

1. **Work on papers it has not seen, for any research question.** Every paper comes from arXiv, and the question can
   be on any topic.
2. **Build its own search.** Create an appropriate search to be sent to arXiv using an API, pull in the details of the
   papers that arXiv finds, and analyze each one for its fit with the research question.
3. **Rank at least 5 papers.** Show the papers that best match the question in ranked order, best match first. For each
   paper, give its title, its arXiv link, and **why** the researcher should read it. The reason must come from the
   paper's own abstract, not from the LLM's trained memory.
4. **Use the researcher's papers.** For each paper in `papers`, pull in the missing data if needed (title, abstract, link) from
   the arXiv API. A paper that fits the question goes into the ranking.
5. **Check that each citation is real.** For each paper that the researcher included in `papers`, the assistant checks with arXiv that it exists, and tells the researcher one of these:
   - the paper is real and fits the question, so it is in the ranking;
   - the paper is real but **does not fit** the question, so the assistant ignores it and says briefly why;  
   - the DOI is **broken**: **no paper exists**.

   The assistant never shows a paper that does not exist, and never makes up a title, a link or a finding.

## Step 1: set up the team repository

1. **The team chooses one GitHub repository owner.** This person should:
   1. Make the team repository as a copy of this repository (for example, click **Fork** on this repository's GitHub page).
   2. On the team repository, add every teammate as a collaborator. To do this, each teammate must make a free GitHub account on https://github.com (if they do not have one) and share their user name with the repository owner. Each teammate accepts the email invitation.
   3. Send the team repository's URL to the team.
2. **Each person** clones the team repository onto their own computer. Each person copies their own tool file (such as `llm/screener.py`) and cases file (such as `data/my_cases/screener.json`) into the cloned folder.
3. **Each person** runs their tool to check that it still works, then pushes their work to the team's GitHub repository, following the guidance shared in class. **Each person must pull, merge with their teammates' commits, and push their own commits under their own GitHub account in the team repository** (see the rubric below).

## Step 2: build the project together

Once everyone's work is in the team's GitHub repository, join all the tools into one tool. Your objective is described (it is vague intentionally) in "Goals" at the start of this README. The team should define the work to be done and divide this work as the team sees fit (see "Peer evaluation" in the rubric).

Plan to support each other and to teach each other what you are not familiar with. Agentic tools such as Claude Code and OpenAI Codex are permitted, but each person must be able to describe the code they committed in their own words.

## Step 3: try your assistant on the kinds of questions that will be tested

Before you hand in, check that your assistant works as it should. Saeah will evaluate the project with 10 spoken research questions of her own, with filler words, one at a time. She gives each question as a JSON file in the format shown in "Goals", and runs your `main.py` on it. Write your own test files in the same format, on topics of your choice.

- **5 questions with no DOIs:** the assistant builds its own search and ranks at least 5 papers.
- **3 questions with good arXiv DOIs:** papers that are real and fit the question. The assistant checks them, pulls in
  their details, and uses them within the ranking if applicable, together with papers from its own search.
- **2 questions with unrelated arXiv DOIs:** papers that do not fit the question, or DOIs that are broken. The assistant
  tells the researcher that it ignores the paper and why, or that the DOI is broken and no paper exists. It still
  ranks at least 5 papers from its own search.

## Rubric

**Total = 28 points: peer evaluation (15) + technical submission (13).**

**Peer evaluation (15 points):** you will evaluate each of your teammates (not yourself) through the following questions.
Your responses are confidential and will never be shared with teammates under any circumstance.

| Question | Answer |
|---|---|
| Name | Their full name |
| Proactively seeks solutions, moving the team forward | Number: 1–5 Likert scale |
| Communicates respectfully | Number: 1–5 Likert scale |
| Can be trusted to complete their assigned task on time | Number: 1–5 Likert scale |
| Knows how and when to ask for help | Number: 1–5 Likert scale |
| Strengths | What does this teammate do particularly well? Give at least one specific detail. |
| Weaknesses | What are some specific ways this teammate could improve their contribution? Be constructive. |

The Likert scale is as follows:
- 5: strongly agree - 4: somewhat agree - 3: neutral - 2: somewhat disagree - 1: strongly disagree

**Technical submission (13 points):**

| Part | Points | Who | Full points when |
|---|---|---|---|
| Git merge | 1 | Each person | In the team repository's history, you have your own commits and at least one merge (a `git pull` that joined teammates' commits with yours). |
| Code description | 2 | Each person | You describe, in your own words, the code that you contributed: what it does and how it works. |
| 5 questions with no DOIs | 5 (1 each) | Whole team, shared equally | The assistant shows at least 5 papers in ranked order. Each paper is real (its arXiv link works) and fits the question. |
| 3 questions with good DOIs | 3 (1 each) | Whole team, shared equally | As above, and the assistant says that each DOI is real, pulls in its title and abstract from arXiv, and possiblyuses the paper within the ranking. |
| 2 questions with unrelated DOIs | 2 (1 each) | Whole team, shared equally | The assistant tells the researcher that it ignores the paper because it does not fit (with the reason), or that the DOI is broken and no paper exists. It still shows at least 5 ranked papers. |

Everyone on the team gets the same points for the 10 questions. The Git merge point and the code description points are for each person.
