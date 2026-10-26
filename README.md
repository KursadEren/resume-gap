# resume-gap

A Claude skill that compares a job posting against your resumes and shows you
the gap.

It tells you which terms the posting asks for that your resume does not have,
which ones you do have but buried at the end of a line, which resume to send,
and what to change — **without ever writing in experience you do not have.**

That last part is the whole point. When it finds something missing, it does not
add it to your resume. It asks you: *have you actually done this? On which
project, for how long?* Putting a technology you have never used on a resume
sends you into an interview with a lie you will be caught in.

```
You: [pastes a job posting] am I a fit for this?

Claude: Coverage ~62%. Send Resume_Backend_EN.pdf.
        Biggest gap: the posting wants CI/CD and Kubernetes; neither appears
        in your resume.

        In the posting, not in your resume
        ┌─────────────┬────────────┬──────────────────────────────────────────┐
        │ CI/CD       │ 2×, req.   │ Have you set up a pipeline — GitHub      │
        │             │            │ Actions or similar? What did it automate?│
        │ Indexing    │ 2×, req.   │ Did you ever speed up a slow query with  │
        │             │            │ an index? Do you remember the before/after?│
        └─────────────┴────────────┴──────────────────────────────────────────┘

        You have it, but it's buried
        Docker — TECHNICAL SKILLS, line 11 → move into the experience bullet
                 where you describe deployment
```

## Install

```
/plugin marketplace add KursadEren/resume-gap
/plugin install resume-gap@resume-gap
```

Or as a plain skill, without the plugin system:

```bash
git clone https://github.com/KursadEren/resume-gap
cp -r resume-gap/skills/resume-gap ~/.claude/skills/
```

## Use

Paste a posting, or give it a link:

> Am I a fit for this? Which resume should I send?

It looks for your resumes in the working directory and `~/Desktop`, lists what
it found, and asks which to use. Reads `.pdf`, `.docx`, `.txt` and `.md`.

PDF support needs `pymupdf`, `.docx` needs `python-docx`:

```bash
pip3 install pymupdf python-docx
```

## What it does

**Weights the posting instead of counting words.** "Python" in a company blurb
is not "Python" under required qualifications. Requirements count 3×,
responsibilities 2×, nice-to-haves 1.5×, the company pitch and benefits 0.2×.

**Ignores boilerplate.** "Team player", "strong communication skills",
"detail-oriented" — these appear in every posting and separate no candidate
from another, so they are not treated as terms.

**Grounds every suggestion.** A rephrasing suggestion may sharpen a sentence,
but every technical name inside it already exists in your resume. No new
technologies get slipped in, and no numbers get invented.

**Refuses when it should.** If the posting has too few distinguishing terms, it
does not give you a percentage — it says why. Finding one term and knowing it
is not a "100% match".

**Does not invent an ATS score.** Those sites will score the same resume 55, 74
and 79; the number is vendor marketing. What actually matters is parse
cleanliness — is the text selectable, are the headings standard, does a
two-column layout scramble the reading order.

## Languages

Works with postings in any language and replies in whichever language you write
in. The resume reader recognises section headings in English, Turkish, German,
French and Spanish.

## Sibling project

[Kıyas](https://github.com/KursadEren/kiyas) is a Chrome extension that does a
narrower version of this in the browser, for free, with no model involved — one
click while you are looking at the posting.

The two solve the same problem from opposite ends. The extension needs a term
dictionary and statistical filtering precisely *because* there is no model
reading the posting; this skill needs none of that machinery, because Claude
reads it. Use the extension while browsing, the skill while editing.

## License

MIT — see [LICENSE](LICENSE).
