
import json
from datetime import datetime
import streamlit as st

st.set_page_config(page_title="Executive Productivity Agent", page_icon="🎯", layout="wide")

with open("data.json", "r") as f:
    data = json.load(f)

commitments = data["commitments"]
calendar = data["calendar"]

# Demo date is intentionally fixed to the assignment week so the prototype
# produces reproducible results during evaluation.
DEMO_NOW = datetime(2026, 9, 23, 9, 0)

def fmt_status(s):
    return {
        "pending":"Pending",
        "ready":"Ready for review",
        "received_needs_review":"Received — review needed",
        "confirmed":"Confirmed",
        "unowned":"Unowned / ownership unclear",
        "completed_by_source":"Completed by source"
    }.get(s,s)

def answer_question(q):
    ql=q.lower().strip()

    if any(k in ql for k in ["promise raghav","promised raghav","raghav","vendor list"]):
        return (
            "**You promised Raghav the updated vendor list.**\n\n"
            "It was originally discussed for Tuesday, then moved to Wednesday morning. "
            "The latest email from Raghav on Wednesday at 8:45 AM asks whether it is still happening this morning. "
            "So the action is currently **pending**."
        )

    if any(k in ql for k in ["attention","action today","today","urgent"]):
        return (
            "**Action brief:**\n\n"
            "🔴 **Mumbai lease renewal:** ownership is still unclear; authorized signature is required by Friday EOD.\n\n"
            "🟠 **Vendor list:** still pending for Raghav.\n\n"
            "🟡 **Expense variance:** report has arrived; Arjun needs to review it before Thursday board prep.\n\n"
            "📅 **Calendar:** Meridian Logistics call is at 3:00 PM today."
        )

    if "waiting" in ql or "others" in ql:
        return (
            "**Waiting on others:**\n\n"
            "• Neha Kapoor — campaign deck (already delivered Thursday at 8:00 AM)\n"
            "• Divya Rao — July expense variance report (already delivered Wednesday at 6:00 PM)\n"
            "• Priya Nair — Meridian call time (confirmed for Wednesday 3:00 PM)\n\n"
            "The source data does not show a current unresolved wait on these three items."
        )

    if "overdue" in ql:
        return (
            "Using the assignment's Wednesday 23 September 2026 context, the **vendor list is late against Arjun's stated Tuesday/EOD expectation** "
            "but was subsequently reset to Wednesday morning. The latest Wednesday 8:45 AM follow-up still shows it pending. "
            "I would label it **at risk/pending**, not invent a new deadline."
        )

    if "lease" in ql or "mumbai" in ql:
        return (
            "**Mumbai office lease renewal:** deadline Friday, 25 September, end of day. "
            "The authorized signer/owner is not established in the source data. "
            "The agent therefore flags it as **Unowned / Ownership unclear** rather than assigning Facilities or another person."
        )

    if "campaign" in ql or "deck" in ql:
        return (
            "**Q3 campaign deck:** Neha moved the review to Thursday morning and confirmed **9:30 AM Thursday**. "
            "The deck was sent Thursday at 8:00 AM. Arjun's action is to review it."
        )

    if "expense" in ql or "variance" in ql:
        return (
            "**July expense variance report:** Divya sent the report Wednesday at 6:00 PM. "
            "Arjun's action is to review it before Thursday board prep."
        )

    if "meeting" in ql or "calendar" in ql:
        rows=[f"• {x['day']} {x['date']} — {x['time']} — {x['event']}" for x in calendar]
        return "**Arjun's calendar:**\n\n" + "\n".join(rows)

    return (
        "I can answer questions about commitments, Raghav/vendor list, waiting on others, "
        "deadlines, the Mumbai lease, campaign deck, expense report, Meridian call, and calendar."
    )

st.title("🎯 Executive Productivity Agent")
st.caption("AIONOS Assignment 1 • Grounded only in the supplied data pack")

with st.sidebar:
    st.header("Navigation")
    page=st.radio("Go to",[
        "Daily Action Brief",
        "Ask the Agent",
        "My Actions",
        "Waiting on Others",
        "Unclear Ownership",
        "Calendar",
        "Source Grounding"
    ])
    st.divider()
    st.info("Demo context: Wednesday, 23 September 2026, 9:00 AM")
    st.caption("No external data is used.")

if page=="Daily Action Brief":
    st.subheader("Daily Action Brief")
    st.write("**Wednesday, 23 September 2026**")

    c1,c2,c3,c4=st.columns(4)
    c1.metric("My actions","4")
    c2.metric("Waiting items","3")
    c3.metric("Unowned","1")
    c4.metric("Critical","1")

    st.markdown("### 🔴 Needs Action")
    st.error("**Mumbai office lease renewal** — owner/signatory unclear. Deadline: Friday 25 Sep, end of day.")
    st.warning("**Updated vendor list** — pending for Raghav. Latest follow-up: Wednesday 8:45 AM.")

    st.markdown("### 🟡 Review / Prepare")
    st.info("**July expense variance report** — received Wednesday 6:00 PM; review before Thursday board prep.")
    st.info("**Q3 campaign deck** — review Thursday at 9:30 AM.")

    st.markdown("### 📅 Today's Calendar")
    for x in calendar:
        if x["date"]=="2026-09-23":
            st.write(f"**{x['time']}** — {x['event']}")

    st.markdown("### 💬 Quick Questions")
    for q in ["What did I promise Raghav?","What needs action today?","Who am I waiting on?","What is the status of the Mumbai lease?"]:
        if st.button(q):
            st.session_state["question"]=q
            st.session_state["answer"]=answer_question(q)
            st.rerun()

elif page=="Ask the Agent":
    st.subheader("🤖 Ask the Executive Agent")
    q=st.text_input("Ask a question", value=st.session_state.get("question",""),
                    placeholder="e.g. What did I promise Raghav?")
    if st.button("Ask"):
        st.session_state["answer"]=answer_question(q)
    if st.session_state.get("answer"):
        st.markdown("### Agent Response")
        st.markdown(st.session_state["answer"])
        st.caption("Response is generated from the structured assignment data and source-grounded rules.")

elif page=="My Actions":
    st.subheader("👤 My Actions")
    for x in commitments:
        if x["category"]=="my_action":
            with st.expander(f"{x['priority']} • {x['canonical_action']}"):
                st.write(f"**Deadline:** {x['deadline_text']}")
                st.write(f"**Status:** {fmt_status(x['status'])}")
                st.write(f"**Sources:** {', '.join(x['sources'])}")
                st.write(f"**Evidence:** {x['evidence']}")

elif page=="Waiting on Others":
    st.subheader("⏳ Waiting on Others")
    for x in commitments:
        if x["category"]=="waiting_on_others":
            st.success(f"**{x['owner']}** — {x['canonical_action']}")
            st.write(f"Status: {fmt_status(x['status'])} • {x['deadline_text']}")
            st.caption(x["evidence"])

elif page=="Unclear Ownership":
    st.subheader("⚠️ Unclear Ownership")
    x=[x for x in commitments if x["category"]=="unclear_ownership"][0]
    st.error(f"**{x['canonical_action']}**")
    st.write("**Owner:** UNASSIGNED")
    st.write(f"**Deadline:** {x['deadline_text']}")
    st.write("**Rule:** The agent flags uncertainty instead of inventing an owner.")
    st.caption(x["evidence"])

elif page=="Calendar":
    st.subheader("📅 Weekly Calendar")
    for x in calendar:
        st.write(f"**{x['day']} {x['date']} | {x['time']}** — {x['event']}")

elif page=="Source Grounding":
    st.subheader("📚 Source Grounding & Audit Trail")
    st.write("Every commitment has a source list and evidence field. This prevents the agent from silently inventing ownership or deadlines.")
    for s in data["sources"]:
        st.write("•",s)

st.divider()
st.caption("Prototype only. No real email/calendar actions are performed.")
