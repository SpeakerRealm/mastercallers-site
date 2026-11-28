"""Generate the ten static training topic pages from their editorial source."""
from html import escape
from pathlib import Path

TOPICS = [
    dict(slug="brief-writing-for-ai", title="Brief-writing for AI", track="Build",
         summary="Turn an operational need into a clear assignment an AI tool can help complete and a person can review.",
         intro="A useful prompt starts before the prompt box. Teams learn to describe the job, the audience, the material the tool may use, the constraints it must honor, and what an acceptable result looks like. The aim is repeatable work that someone else on the team can understand and improve.",
         learn=["Translate a vague request into a brief with purpose, inputs, output format, and acceptance criteria.", "Supply examples and source material while separating facts from assumptions.", "Test a draft against the brief, spot missing evidence, and revise without starting over.", "Decide which steps require a person's judgment or approval."],
         practice="Bring a recurring task, such as drafting a client response, summarizing intake notes, or preparing a report. Rewrite it as a reusable brief and run a short review cycle on the result.",
         outcome="A reusable brief and a review checklist for one real team workflow.", audience="Teams beginning to use AI in daily operations, and managers who need consistent results across staff."),
    dict(slug="models-and-second-opinions", title="Models and second opinions", track="Build",
         summary="Choose the right tool for a task, then use an independent review to find what the first answer missed.",
         intro="Different models and tools have different strengths, costs, access rules, and failure modes. This session gives teams a practical way to compare them without treating any answer as automatically correct. A second opinion can help challenge a draft, but it still needs source checks and human judgment.",
         learn=["Match tasks such as research, writing, analysis, coding, and document review to appropriate tools.", "Compare outputs against the same brief rather than relying on style or confidence.", "Ask a second model or reviewer to identify omissions, contradictions, and unsupported claims.", "Keep sensitive material inside the organization's approved tools and handling rules."],
         practice="Run one approved task through two available tools. Compare accuracy, usefulness, effort, and what still needs verification before the work can be used.",
         outcome="A simple model-selection and second-review rubric for the team's common tasks.", audience="Staff and leaders who have access to more than one AI tool and need a consistent way to choose and review."),
    dict(slug="personal-assistant-agents", title="Personal-assistant agents", track="Build",
         summary="Design a bounded assistant for an individual's recurring work without giving it more authority than it needs.",
         intro="An assistant becomes useful when its job, inputs, tools, and stop points are explicit. Teams map a real role and identify work the agent can prepare, work it can carry out under supervision, and decisions it must return to a person. The session emphasizes testing and visibility over an impressive demo.",
         learn=["Choose a narrow task with a clear owner and measurable result.", "Define the information and tools the assistant may use, including what it must never access or send.", "Create approval points for messages, record changes, and other consequential actions.", "Test ordinary cases, incomplete information, and failure paths before wider use."],
         practice="Sketch and prototype an assistant for one recurring activity, such as meeting preparation, inbox triage, or drafting follow-up tasks, using sample or approved data.",
         outcome="An agent brief, prototype workflow, and test cases ready for a supervised pilot.", audience="Individual contributors and team leads who want an assistant tied to a specific workflow."),
    dict(slug="building-sites-and-applications", title="Building sites and applications", track="Build",
         summary="Move from a real organizational problem to a working web prototype with a clear path to ownership.",
         intro="A site or app is more than a screen. Participants work through the user journey, content, data, repository, hosting, and domain decisions that determine whether a prototype can become a dependable tool. The training uses current development tools while keeping the organization's requirements in charge.",
         learn=["Define the user, the task, and the smallest useful version of the product.", "Map pages, forms, data, and handoffs before generating code.", "Understand the roles of a repository, database, domain, and deployment environment.", "Review accessibility, permissions, testing, and maintenance needs before launch."],
         practice="Take one internal or public-facing use case and build a small working flow, such as an intake page or a simple record view. Review what would be needed to make it production-ready.",
         outcome="A working prototype and a practical next-step list for deployment and ownership. Production launch depends on the project's scope and review.", audience="Teams exploring an internal tool, service site, or custom application."),
    dict(slug="call-flows-and-qualification", title="Call flows and qualification", track="Run",
         summary="Understand how MasterVoice handles a conversation and turns it into a usable, reviewable record.",
         intro="Operators need to know what a voice system is trying to learn, how it asks, and what happens when a caller goes off script. This session walks through inbound and outbound scenarios, qualification criteria, record capture, and the points where the call should transfer or stop.",
         learn=["Read and explain the opening, discovery, qualification, and closing stages of a call flow.", "Identify required fields, disqualifying conditions, and what should be left unknown rather than guessed.", "Handle interruptions, unclear answers, opt-outs, and requests for a person according to the configured workflow.", "Review call outcomes and recordings or transcripts where enabled and permitted."],
         practice="Walk through sample calls with a role-specific flow. Mark what the system captured, what it missed, and when a human should take over.",
         outcome="A reviewed call-flow map and operator notes for common exceptions.", audience="Staff who supervise, receive handoffs from, or improve a MasterVoice deployment."),
    dict(slug="scheduling-and-handoff", title="Scheduling and handoff", track="Run",
         summary="Get qualified conversations into the right calendar, record, and person's queue.",
         intro="A successful call is incomplete if the next step disappears. Operators trace how information moves from qualification to scheduling and into the organization's existing CRM or work system. They learn to spot missing fields, duplicate records, failed bookings, and handoffs without an owner.",
         learn=["Map the required information between the voice workflow, calendar, CRM, and team queue.", "Understand booking rules, availability, confirmations, and rescheduling paths.", "Check that a qualified record has an owner, a status, and a clear next action.", "Resolve failed or ambiguous handoffs without silently losing the request."],
         practice="Follow sample records through successful, duplicate, and failed handoffs. Identify where the team should be notified and how each case is closed.",
         outcome="A handoff checklist and exception path tailored to the organization's connected systems.", audience="Operators, schedulers, sales or service teams, and anyone who owns the next step after a call."),
    dict(slug="supervision", title="Supervision", track="Run",
         summary="Run a voice or agent system with clear monitoring, escalation, and change control.",
         intro="Once a system is in use, someone must know what good performance looks like and when to intervene. This training covers routine reviews, unusual outcomes, escalation, and safe changes to prompts or flows. It also makes ownership visible so the system does not become a black box.",
         learn=["Review a small set of meaningful measures, such as completed handoffs, unresolved cases, and error patterns.", "Sample calls or agent actions for quality and adherence to the agreed workflow.", "Define who can pause a flow, correct a record, approve a change, or contact a customer.", "Record changes and retest affected paths before resuming wider use."],
         practice="Use a sample operator dashboard and exception log to decide which cases need correction, escalation, or a workflow change.",
         outcome="A supervision rhythm with named owners, review points, and escalation steps.", audience="Team leads and designated operators accountable for a deployed voice or agent system."),
    dict(slug="foundations", title="Foundations", track="Lead",
         summary="Give a team a shared, practical understanding of AI before asking it to adopt new workflows.",
         intro="This session builds a common language around models, prompts, agents, and data. Participants see useful examples and limitations in the context of their own organization, then identify where AI could assist without confusing a plausible answer with a verified one.",
         learn=["Explain what current models do well and where they are unreliable.", "Write a basic prompt with context, constraints, and an output format.", "Distinguish a one-time AI request from an agent that takes steps or uses tools.", "Recognize data that needs extra care and when an answer requires source or human review."],
         practice="Work through a familiar task as a group, compare a weak and strong brief, and identify one suitable pilot workflow.",
         outcome="A shared vocabulary, a starter brief, and a shortlist of sensible uses for the team.", audience="Organizations introducing AI to mixed-experience staff, boards, or leaders."),
    dict(slug="adoption", title="Adoption", track="Lead",
         summary="Move from scattered experimentation to a supported way of working that staff will actually use.",
         intro="Adoption is a people and process challenge. Leaders choose a narrow pilot, name its owner, train the staff involved, and collect feedback from actual use. The goal is to improve a workflow, not to announce a tool and hope it sticks.",
         learn=["Choose a pilot with a clear need, manageable risk, and a result that can be observed.", "Identify champions, affected staff, training needs, and an escalation route.", "Set a baseline and review usage, quality, time saved, and problems reported.", "Decide whether to revise, expand, or stop the pilot based on evidence."],
         practice="Draft an adoption plan for one workflow, including communication, training, check-ins, and a decision point after initial use.",
         outcome="A pilot adoption plan with owners, feedback channels, and review measures.", audience="Executives, department leads, and project owners responsible for organization-wide change."),
    dict(slug="governance", title="Governance", track="Lead",
         summary="Set practical boundaries for tools, data, approvals, and accountability across an organization.",
         intro="As AI use spreads, leaders need decisions that staff can apply in ordinary work. This session helps teams make those decisions visible: which tools are approved, what data may be used, which actions require human approval, and how issues are reported and reviewed. It is a working session, not a legal certification.",
         learn=["Classify common use cases by the data involved and the consequences of an error.", "Assign owners for tool access, output review, agent actions, and incident response.", "Define approval and recordkeeping rules for external messages, customer records, and automated actions.", "Create a regular review process as tools, policies, and organizational needs change."],
         practice="Use several realistic scenarios to draft a decision matrix: allowed, allowed with review, or not approved, with reasons and an escalation contact.",
         outcome="A draft AI-use decision matrix and a list of policy questions for the organization's leadership and advisers.", audience="Leaders, operations owners, and staff responsible for oversight, privacy, and risk."),
]

NAV = '''<nav>
  <div class="logo"><a href="../index.html"><img src="../logo-dark.jpg" alt="MasterCallers"></a></div>
  <div class="nav-links">
    <a href="../development.html">Development</a><a href="../training.html">Training</a>
    <a href="../teams.html">Teams</a><a href="../curriculum.html">Curriculum</a>
    <a href="../work.html">Work</a><a href="../about.html">About</a>
    <a href="../contact.html">Contact</a><a href="../contact.html" class="btn">Start a project</a>
  </div>
  <details class="mobile-menu"><summary>Menu</summary><div class="mobile-menu-links"><a href="../work.html">Work</a><a href="../development.html">What we build</a><a href="../training.html">Training</a><a href="../teams.html">Teams</a><a href="../curriculum.html">Curriculum</a><a href="../about.html">About</a><a href="../contact.html">Contact</a></div></details>
</nav>'''

for topic in TOPICS:
    e = escape
    title, track = topic["title"], topic["track"]
    points = "\n".join(f"<li>{e(point)}</li>" for point in topic["learn"])
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(title)} · {e(track)} Training · MasterCallers</title>
<meta name="description" content="{e(topic['summary'], quote=True)}">
<link rel="stylesheet" href="../styles.css">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;450;510;600&display=swap" rel="stylesheet">
</head>
<body>
{NAV}
<main>
  <header class="hero training-detail-hero">
    <a class="training-back" href="../training.html#{track.lower()}">Back to {e(track)} training</a>
    <div class="training-kicker">Training / {e(track)}</div>
    <h1>{e(title)}</h1>
    <p>{e(topic['summary'])}</p>
    <div class="accent-bar"></div>
  </header>
  <article class="section training-detail">
    <div class="training-detail-block"><h2>What this session covers</h2><p>{e(topic['intro'])}</p></div>
    <div class="training-detail-block"><h2>Your team will learn to</h2><ul>{points}</ul></div>
    <div class="training-detail-block"><h2>Working session</h2><p>{e(topic['practice'])}</p></div>
    <div class="training-detail-block training-detail-result"><h2>What you leave with</h2><p>{e(topic['outcome'])}</p></div>
    <div class="training-detail-block"><h2>Who it is for</h2><p>{e(topic['audience'])}</p><p>Delivery and scope are adapted to the organization and can be discussed before the engagement.</p></div>
    <div class="training-detail-nav"><a class="btn training-cta" href="../contact.html">Discuss this training</a><a class="training-back" style="margin:0" href="../training.html#{track.lower()}">Explore all {e(track)} topics</a></div>
  </article>
</main>
<footer class="footer"><div>MasterCallers</div><div><a href="../training.html">All training</a></div></footer>
</body></html>
'''
    Path(__file__).with_name(f"{topic['slug']}.html").write_text(html, encoding="utf-8")
