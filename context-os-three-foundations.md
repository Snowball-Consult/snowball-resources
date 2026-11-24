# Three Foundations of a Context OS

> **About this resource:** This is shared by [Snowball Consult](https://snowball-consult.com) as a methodology demo.
> It's meant as inspiration - not as a plug-and-play solution. Some referenced dependencies may not be included.
> Questions? Don't hesitate to reach out at andreas@snowball-consult.com

My Context OS is a folder of documents, rules and skills that Claude Code works from. It holds my knowledge, my standards and my taste, and it grew step by step from daily use.

These three parts carry the rest. Each one shows how mine looks and gives you a prompt to build your own. I think describing your own system works better than adopting mine, so take what fits and leave the rest.

| Foundation | The question it answers |
|---|---|
| [1. Grow it from questions](#1-grow-it-from-questions) | Where do I start? |
| [2. Documents that can be found again](#2-documents-that-can-be-found-again) | How does the agent find the right knowledge? |
| [3. Sessions that stay](#3-sessions-that-stay) | How does it remember what we worked on? |

---

## 1. Grow it from questions

I had no blueprint. This is the order I went in:

1. **Tell it who you are.** What you do, your strengths, your weaknesses, what it should explain plainly. Mine says that I am not a developer and that I use terms I do not always understand.
2. **Tell it what the system is for.** Mine: add knowledge over time, get it back when it matters, include my taste.
3. **Ask for a structure, and ask it to question you.** Pick from what it suggests. "This makes sense", "this does not" and "I do not understand this" are all useful answers.
4. **Ask how it works, then steer.** I asked how it finds files. It starts with filenames, so I made filenames carry the search words. That became my first standard.
5. **Write every standard down once.** When you correct the same thing twice, turn the correction into a document that the agent reads next time.
6. **Extend when you run into something.** A second machine, call transcripts, client folders: each was added when I needed it.

**Where things go.** How you do the work goes into shared documents. Facts about one client, market or project go into that project's folder. The way I build a classifier is the same for every client, and the market facts inside it are not.

**Skills stay short.** A skill says what to do and points to the document that says how. Several skills can then follow one standard.

**Prompt to start with:**

```
I want to build a context system with you: a place for my knowledge, my standards and my
taste that you can search and use whenever it matters.

About me: <what you do, strengths, weaknesses, what to explain plainly>
What I want it to do for me: <your goal>

I am not an expert in this, so question my goal before you propose anything. Then:
1. Explain in plain words how you find and load files in this setup. Check the current
   official documentation and link it.
2. Suggest two or three simple structures, with what each is good and bad at.
3. Recommend one, and name the first three documents worth writing.
Build nothing until I pick.
```

---

## 2. Documents that can be found again

A document helps only if the agent finds it at the moment it matters. Three conventions do most of that work:

- **The filename is a search record.** Before naming a file, predict the words you would use when you need it, synonyms included, and put them into the name.

  ```
  doc-12_PROCEDURE_client-onboarding-tech-stack-audit-stakeholder-access.md
  ```

- **The first 20 lines say what it is.** A small table with the purpose, when to use it, what it leaves out, what it depends on, and how far to trust it.

- **Maturity is stated.** Draft, Working, Stable, Canonical or Obsolete. A document I have never used in practice gets less weight than one that held up many times.

When my words and the filename do not match, a short **topic router** translates: "is this person still there" leads to `employment`, `in-seat`, `job-change`. The agent looks in the cheapest place first and goes further only when it has to.

**Full documents:**

- [AI Context Document Standards](ai-context-document-standards.md): how every document is structured
- [Filename Generation](filename-generation-keyword-extraction-retrieval-optimization.md): how to choose the words in the name
- [Anatomy of a Context System](context-system-indexing-retrieval-architecture.md): how the parts work together when the agent searches

**Build your own:**

```
Read these three documents:
https://raw.githubusercontent.com/Snowball-Consult/snowball-resources/main/ai-context-document-standards.md
https://raw.githubusercontent.com/Snowball-Consult/snowball-resources/main/filename-generation-keyword-extraction-retrieval-optimization.md
https://raw.githubusercontent.com/Snowball-Consult/snowball-resources/main/context-system-indexing-retrieval-architecture.md

Treat them as one example. Look at the files I have and the way I phrase requests. Propose the
smallest version that would help me: a filename pattern, a header for each document, and the
categories I need. Show it on two of my own documents. Change nothing until I agree.
```

---

## 3. Sessions that stay

A session is one conversation in the Claude Code terminal. It holds decisions, corrections and reasons that are easy to lose when the window closes.

I end every session of value with one command, **`/exit-wrap`** (exit, then wrap). It:

- proposes a searchable name for the session
- writes or updates one **handover file per topic**: the goal, what was decided and why, what is open, how to pick it up
- commits only the files this session touched, and pushes them to GitHub

Weeks later I ask about the topic in a new session, and the agent finds the handover by its filename and continues from there. My second machine gets the same files through GitHub.

It is a command I type and choose to run. Some sessions are the equivalent of a web search, and saving those would add noise.

**The skill:** [`/exit-wrap`](skills/quality-of-life/exit-wrap/), with a build prompt and the questions to ask yourself when making your own.

**Check before the first run:** handovers contain conversation content. Keep them out of public repositories, and never write secrets into them.

---

## How the three work together

You ask for something. The agent finds the standard by its filename (2), works by rules you shaped (1), and the decisions you make on the way are there the next time (3). Corrections from those sessions become the next version of the standards.

---

*From [Snowball Consult](https://snowball-consult.com), a GTM data infrastructure consultancy.*
