# AIONOS Assignment 1 — Executive Productivity Agent

## 1. What this project does

This prototype converts messy executive inputs into a daily action brief for **Arjun Malhotra, VP Sales**.

It demonstrates all required assignment capabilities:

- Identify commitments made by the executive
- Separate **My Actions** from **Waiting on Others**
- Detect deadlines and status
- Deduplicate the same action across sources
- Flag unclear ownership instead of inventing it
- Produce a daily action brief
- Answer questions such as:
  - "What did I promise Raghav?"
  - "What needs action today?"
  - "Who am I waiting on?"
  - "What is the status of the Mumbai lease?"

## 2. Architecture

```text
Emails + Calendar + Meeting Transcript + Voice Notes
                         |
                         v
                Source Normalization
                         |
                         v
             Commitment / Event Extraction
                         |
                         v
                  Deduplication
                         |
              +----------+----------+
              |          |          |
              v          v          v
          My Actions  Waiting    Unclear Owner
              |          |          |
              +----------+----------+
                         |
                         v
               Deadline + Status Engine
                         |
                         v
                Daily Action Brief
                         |
                         v
                    AI Q&A Layer
                         |
                         v
                 Streamlit Prototype
```

## 3. Technology

- Python
- Streamlit
- JSON structured data
- Rule-based grounded Q&A for a reliable offline demo
- Optional LLM integration can be added later

The prototype intentionally works without an API key so a reviewer can run it locally.

## 4. Run locally

Requirements: Python 3.10+ recommended.

```bash
cd AIONOS_Assignment1_Executive_Productivity_Agent
python -m pip install -r requirements.txt
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal.

## 5. GitHub upload

```bash
git init
git add .
git commit -m "AIONOS Assignment 1 - Executive Productivity Agent"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

Do not upload API keys or private credentials.

## 6. Suggested demo flow

1. Open **Daily Action Brief**
2. Show the critical unowned Mumbai lease renewal
3. Show the pending vendor list
4. Open **My Actions**
5. Open **Waiting on Others**
6. Open **Unclear Ownership**
7. Open **Ask the Agent**
8. Ask: `What did I promise Raghav?`
9. Ask: `What needs action today?`
10. Show **Source Grounding**

## 7. Deduplication example

The vendor-list action appears in:
- Leadership Sync
- Vendor List email thread
- Arjun's voice note

These are represented as one canonical commitment: **Send updated vendor list to Raghav**.

## 8. Ownership rule

For the Mumbai lease renewal, the sources do not establish a confirmed owner. The agent therefore displays **UNASSIGNED** instead of assuming Facilities, Finance, Raghav, or Arjun.

## 9. Scope and assumptions

- The assignment data pack is the only source of truth.
- The dates are kept in the assignment's week of 21–25 September 2026.
- Voice notes are treated as Arjun's own reminders/commitments.
- `.example` email addresses are documentation/testing addresses.
- This prototype does not send real emails or modify calendars.

## 10. Future enhancements

- RAG/embeddings for larger document sets
- Gmail/Outlook connector
- Calendar connector
- LLM-based extraction with structured output
- Approval-based email drafting/sending
- Persistent reminders
- Conflict detection and free-slot recommendations
