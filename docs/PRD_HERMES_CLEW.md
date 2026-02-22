# PRD: Hermes Clew --- Agent Readiness Scanner for the Agentic Web

**Version:** 1.2 **Author:** Shara / L. Cordero **Date:** February 21,
2026 **Hackathon:** GitLab Duo Agent Platform Challenge **Deadline:**
March 25, 2026 @ 2:00 PM EDT / 11:00 AM PDT **Budget:** \~48 hours total
(1-2 hrs/day evenings/weekends, solo) **Type:** Developer tool (not an
app --- no UI, no frontend, no database)

------------------------------------------------------------------------

## Table of Contents

1.  [What This Is](#1-what-this-is)
2.  [Why This Exists](#2-why-this-exists)
3.  [Scope Contract](#3-scope-contract)
4.  [Architecture](#4-architecture)
5.  [How Code Gets Into the Scanner](#5-how-code-gets-into-the-scanner)
6.  [Agent Definition (GitLab Duo)](#6-agent-definition-gitlab-duo)
7.  [Scan Engine: What We Check](#7-scan-engine-what-we-check)
8.  [Claude Reasoning Layer](#8-claude-reasoning-layer)
9.  [Output: The Report](#9-output-the-report)
10. [Data Flow](#10-data-flow)
11. [File Map](#11-file-map)
12. [Security & Data Protection](#12-security--data-protection)
13. [QA Plan](#13-qa-plan)
14. [Timeline (32 Days)](#14-timeline-32-days)
15. [Demo Plan (3-Minute Video)](#15-demo-plan-3-minute-video)
16. [Hackathon Compliance: Trigger +
    Action](#16-hackathon-compliance-trigger--action)
17. [Anthropic Track Compliance](#17-anthropic-track-compliance)
18. [Platform Capability Matrix](#18-platform-capability-matrix)
19. [Submission Checklist](#19-submission-checklist)
20. [Stubbed Features
    (Post-Hackathon)](#20-stubbed-features-post-hackathon)
21. [Known Risks & Mitigations](#21-known-risks--mitigations)
22. [Spikes (Verify Before Building)](#22-spikes-verify-before-building)
23. [Glossary](#23-glossary)

------------------------------------------------------------------------

## 1. What This Is

Hermes Clew is a **read-only GitLab Duo developer tool** that scans
HTML, JSX, and TSX files in a GitLab repository and reports how well the
application would perform in the agentic web --- where AI agents, not
humans, are the primary users of the internet.

It is a **tool**, not an app. There is no frontend. No UI to build. No
database. No user accounts. It lives entirely inside GitLab Duo Chat.
You talk to it, it scans, it reports.

It does NOT modify code. It does NOT create merge requests. It does NOT
touch dependencies. It reads files, reasons about patterns using Claude
(Anthropic), and posts a structured report.

**One sentence:** "Hermes Clew tells you whether an AI agent can use
your app, and explains in plain English what to fix."

**Name origin:** Hermes --- the Greek messenger god who moved between
worlds. Hermes Clew bridges the human web and the agent web. Part of the
Clew suite (Ariadne Clew, Janus Clew, Lumen Clew, Metis Clew, etc.).

**Lineage:** Spiritual successor to Lumen Clew (GitHub code health
scanner). Same philosophy --- awareness, not judgment. New frontier ---
agent readiness, not code quality.

------------------------------------------------------------------------

## 2. Why This Exists

### The Problem

The internet was built for human eyes. Websites use visual layouts,
styled divs, custom click handlers, and JavaScript-rendered content that
humans navigate by sight. AI agents don't have eyes. They parse the DOM.
When a vibecoded app uses a `<div onclick="...">` instead of a
`<button>`, an agent literally cannot find the interactive element.

### Why It Matters Now

-   AI agents (OpenClaw, Operator, Gemini Live, Comet) are becoming
    primary web traffic
-   Vibecoding tools (Lovable, v0, Bolt) optimize for visual output,
    often producing agent-invisible markup
-   NLWeb, MCP, and A2A protocols are creating a machine-readable web
    layer
-   No tool exists that serves vibecoders with friendly, educational
    agent-readiness feedback

### Why It Matters for GitLab

Every web app deployed through GitLab CI/CD should be agent-ready. This
tool catches readiness issues inside the developer workflow --- before
shipping. It's the accessibility audit for the agentic web.

### Meta-Awareness: This Tool Is Built for Agents

Hermes Clew doesn't just scan for agent-readiness --- it IS agent-ready.
The codebase itself follows every principle it checks for. The repo
includes AGENTS.md. The report format is machine-readable. This is a
statement: "I understand the agentic web so deeply that I built my tool
for it, not just about it."

### Competitive Positioning

  ---------------------------------------------------------------------------
  Tool        Audience        What It Scans          Our Difference
  ----------- --------------- ---------------------- ------------------------
  WordLift AI Enterprise SEO  URLs for AI search     We scan source code in
  Audit       teams           visibility             the repo, not deployed
                                                     URLs. We serve
                                                     vibecoders, not
                                                     marketers.

  Factory     DevOps          Repos for coding-agent Factory checks if agents
  Agent       engineering     compatibility          can *code in* your repo.
  Readiness   orgs            (linters, CI/CD)       We check if agents can
                                                     *use* your app.

  Hermes Clew Vibecoders,     HTML/JSX/TSX source    Friendly, educational,
  (this)      indie devs      for agent navigability source-level,
                                                     Claude-reasoned, inside
                                                     GitLab workflow.
  ---------------------------------------------------------------------------

------------------------------------------------------------------------

## 3. Scope Contract

This section is the law. If it says MUST, it ships. If it says STUB, it
gets an interface/comment but no implementation. If it says NEVER, it
does not exist in this build.

**Re-read this section before every build session.**

### MUST (Ships for Hackathon)

-   [ ] GitLab Duo custom agent or flow, public, in the hackathon group
-   [ ] Scans HTML, JSX, and TSX files in the current GitLab project
    repo
-   [ ] Python scan engine produces raw findings (pass/fail per check)
-   [ ] Claude (Anthropic) reasons about raw findings --- catches false
    positives, weighs context, makes defensible judgments
-   [ ] Claude generates plain-English report with score, explanations,
    and fix suggestions
-   [ ] Agent Readiness Score (0-100) with 6 category breakdowns
-   [ ] Accessible via GitLab Duo Chat (user asks agent to scan)
-   [ ] Works on at least 5 demo repos (pushed to GitLab from Shara's
    portfolio)
-   [ ] AGENTS.md in repo root (this tool is itself agent-ready)
-   [ ] 3-minute demo video on YouTube
-   [ ] README with setup/usage instructions
-   [ ] MIT license, public repo in hackathon group

### STUB (Interface exists, logic deferred)

-   [ ] Path B input: scan a public GitHub URL or deployed URL
    (comment + empty function signature)
-   [ ] MR-triggered scanning (comment: `# STUB: MR event trigger`)
-   [ ] Configurable score thresholds
-   [ ] Historical score tracking across commits
-   [ ] NLWeb compatibility check
-   [ ] MCP endpoint detection
-   [ ] Visual "human view vs agent view" split-screen comparison

### NEVER (Not in this build, not even mentioned in code)

-   Code modification or auto-fixing
-   Merge blocking
-   Dependency analysis
-   Performance testing
-   SEO analysis
-   Any write operation to the repository
-   Any frontend, UI, dashboard, or web interface
-   Any database or persistent storage
-   Any user accounts or authentication beyond GitLab's own

------------------------------------------------------------------------

## 4. Architecture

### Design Principle: Agent-First (Practice What We Preach)

This tool is built for the agentic web. The codebase itself follows
every principle it scans for:

-   **Semantic file names** --- every file name describes its single
    responsibility
-   **AGENTS.md in repo root** --- describes the project to any agent
    that encounters it
-   **Machine-readable output** --- the report uses structured markdown
    that agents can parse
-   **One file, one job** --- no god files, no mixed concerns
-   **Zero UI** --- this is a tool, not an app. Agents don't need UIs.

### Three-Layer Architecture

    ┌─────────────────────────────────────────────────────┐
    │  LAYER 1: GitLab Duo Agent (Interface)              │
    │  - Receives user request via Duo Chat               │
    │  - Identifies target project/files                  │
    │  - Triggers scan                                    │
    │  - Posts final report to chat                       │
    └──────────────────┬──────────────────────────────────┘
                       │
    ┌──────────────────▼──────────────────────────────────┐
    │  LAYER 2: Scan Engine (Python — Mechanical)         │
    │  - Finds HTML/JSX/TSX files in repo                 │
    │  - Runs 6 category checks (pattern matching)        │
    │  - Produces raw JSON findings                       │
    │  - NO reasoning. NO judgment. Just facts.            │
    └──────────────────┬──────────────────────────────────┘
                       │
    ┌──────────────────▼──────────────────────────────────┐
    │  LAYER 3: Claude Reasoning (Anthropic — Judgment)   │
    │  - Receives raw findings JSON                       │
    │  - Reasons about patterns, context, false positives │
    │  - Weighs severity and interconnections             │
    │  - Generates defensible, plain-English report       │
    │  - Accessed via GitLab's built-in Anthropic model   │
    └─────────────────────────────────────────────────────┘

### Why Claude Is a Core Architectural Component (Not a Formatter)

A pure Python score is brittle. Examples of why reasoning matters:

-   A React component uses a custom `<Button>` that renders to a real
    `<button>` at build time. Python flags it as div-soup. Claude
    recognizes the pattern and adjusts.
-   A site has zero Schema.org markup but has excellent semantic HTML
    throughout. Python scores it low on structured data. Claude notes
    that the semantic HTML partially compensates and says "start here
    --- Schema.org would take you from 65 to 85."
-   A file has 100 divs but they're all inside a data visualization
    library. Python sees div-soup. Claude recognizes the pattern and
    says "these divs are chart containers, not interactive elements ---
    not a real issue."

Without Claude reasoning, the tool produces false positives that erode
trust. With Claude reasoning, the tool produces defensible, nuanced
assessments that developers actually listen to.

### Stack

  -----------------------------------------------------------------------
  Layer                Technology                       Role
  -------------------- -------------------------------- -----------------
  Interface            GitLab Duo Agent Platform        User interaction,
                                                        file access, chat
                                                        responses

  Scan Engine          Python (html.parser, regex)      Mechanical
                                                        pattern
                                                        detection, raw
                                                        findings

  Reasoning            Anthropic Claude (via GitLab)    Contextual
                                                        judgment, false
                                                        positive
                                                        detection, report
                                                        generation

  Report               Markdown                         Output format ---
                                                        human and agent
                                                        readable

  Config               YAML (`.gitlab/duo/`)            Agent/flow
                                                        configuration
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 5. How Code Gets Into the Scanner

### MVP (Path A): Code Lives in GitLab

The scanner reads files from the current GitLab project. The code must
be in a GitLab repo.

**For the hackathon demo:** Shara pushes 5 repos from her portfolio to
the GitLab hackathon group. These become the demo projects. Mix of
deployed URLs (where source is also available) and source-only repos.

**For other users:** They push or mirror their code to a GitLab repo,
then ask Hermes Clew to scan. This is friction for vibecoders who live
on GitHub, but it's the natural model for a GitLab hackathon tool.

**Why this is fine for the hackathon:** Judges are GitLab people testing
GitLab tools. Code being in GitLab is the expected workflow. No judge
will dock points for this.

### STUB (Path B): Accept External URLs

Post-hackathon, Hermes Clew will accept: - A public GitHub URL → clone,
scan, report, delete clone - A deployed URL → fetch HTML, scan, report

Stub in code:

``` python
# STUB: Path B — External URL scanning
# Post-hackathon: Accept GitHub URL or deployed URL as input.
# Clone public repo to temp directory, scan, delete after report.
# For deployed URLs: fetch rendered HTML, scan DOM output.
# Security: Only public repos. Delete clone immediately after scan.
# Never store cloned code. Never access private repos.
# See PRD Section 20 for full specification.
def scan_external_url(url: str) -> dict:
    raise NotImplementedError("Path B: External URL scanning — post-hackathon feature")
```

------------------------------------------------------------------------

## 6. Agent Definition (GitLab Duo)

### Custom Agent Configuration

The agent is defined as a GitLab Duo custom agent. Based on GitLab docs,
this requires:

1.  A project in the GitLab AI Hackathon group
2.  Agent configuration via the GitLab UI (system prompt + tools)
3.  The agent is enabled for the project and accessible via Duo Chat

### System Prompt (Draft)

    You are Hermes Clew, an agent-readiness scanner for web applications. You are part of the Clew suite of developer tools.

    Your job: Analyze HTML, JSX, and TSX files in this repository and evaluate how well an AI agent could navigate, understand, and interact with the application.

    You are read-only. You never modify files. You never create merge requests. You only analyze and report.

    Your philosophy is "awareness, not judgment." You explain problems like a knowledgeable colleague, not a compliance auditor.

    When you find issues, you explain WHY an agent would struggle (not just WHAT is wrong) and suggest the minimal fix.

    You produce a structured Agent Readiness Report with a score from 0-100, broken into 6 categories.

    You use the scan engine to produce raw findings, then you reason about those findings — catching false positives, weighing context, and making defensible judgments before generating the final report.

### Tools the Agent Needs Access To

-   **File read access** --- read HTML/JSX/TSX files in the project
-   **Shell command execution** --- run the Python scan script
-   **Anthropic Claude** --- reason about findings and generate report
    (via GitLab's built-in integration)
-   **Chat response** --- post the report back to the user

### SPIKE REQUIRED (See Section 22)

Before building, verify: - \[ \] Can a custom agent execute a Python
script via shell? - \[ \] Can a custom agent read arbitrary files in the
repo? - \[ \] What's the exact YAML structure for a custom agent with
these tools? - \[ \] Does the hackathon group give us access to
Anthropic Claude models? - \[ \] Can the agent invoke Claude separately
for reasoning (or is Claude already the underlying model)?

------------------------------------------------------------------------

## 7. Scan Engine: What We Check

Six categories scored independently. Each category has specific,
automatable checks. No subjective assessments at the Python layer. Every
check is binary (pass/fail) or countable. Subjectivity is handled by
Claude in Layer 3.

### JSX/TSX Parsing Honesty

**HTML:** Parsed reliably with `html.parser` and regex. High confidence.

**JSX/TSX:** Parsed heuristically, NOT via AST. We detect
high-confidence anti-patterns (e.g., `onClick` on `<div>`, missing
`aria-label` on icon-only elements) but we do NOT attempt full AST
correctness. Known limitations:

-   Component wrappers (e.g., `<Button>` rendering to `<button>`) appear
    as non-semantic tags in source
-   Spread props (`{...props}`) may include ARIA attributes we can't see
-   Conditional rendering may produce semantic HTML at runtime that
    isn't visible in source
-   Styled-components and CSS-in-JS create wrapper divs that aren't
    interactive

**Mitigation:** Claude reasoning layer is explicitly tasked with
softening JSX/TSX false positives. The report distinguishes HTML
findings (high confidence) from JSX/TSX findings (heuristic ---
interpret with context). If JSX/TSX parsing proves unreliable during
Phase 1 testing, we fall back to HTML-only scanning and stub JSX/TSX
support.

### Category 1: Semantic HTML (Weight: 25%)

**What agents need:** Standard HTML elements they can identify by tag
name.

  ------------------------------------------------------------------------
  Check                      Pass                   Fail
  -------------------------- ---------------------- ----------------------
  Interactive elements use   Tag found              `<div>` or `<span>`
  `<button>`, `<a>`,                                with onClick/onPress
  `<input>`, `<select>`,                            handlers
  `<textarea>`                                      

  Navigation uses `<nav>`    Tag found              Navigation links
                                                    inside generic `<div>`

  Main content uses `<main>` Tag found              No `<main>` tag

  Headers use `<h1>`-`<h6>`  Proper nesting         Skipped levels or
  hierarchy                                         styled divs as headers

  Lists use `<ul>`, `<ol>`,  Tags found             Styled divs as list
  `<li>`                                            items

  Forms use `<form>`         Tag found              No `<form>` wrapper
                                                    around inputs
  ------------------------------------------------------------------------

**Detection method:** Parse files with regex + html.parser. Count
semantic tags vs div-with-handler patterns.

### Category 2: Form Accessibility (Weight: 20%)

**What agents need:** Labeled fields they can identify and fill.

  ----------------------------------------------------------------------------
  Check                      Pass                       Fail
  -------------------------- -------------------------- ----------------------
  Every `<input>` has an     Paired                     Orphaned input
  associated `<label>` (via                             
  `for`/`id` or wrapping)                               

  Inputs have `type`         Type present               Missing type or
  attribute (text, email,                               type="text" on
  tel, etc.)                                            everything

  Inputs have `name`         Name present               Missing name
  attribute                                             

  Submit buttons exist and   `<button type="submit">`   No clear submit
  are identifiable           or `<input type="submit">` mechanism

  Required fields are marked Attribute present          No indication
  with `required` or                                    
  `aria-required`                                       
  ----------------------------------------------------------------------------

**Detection method:** Parse form elements, check attribute presence.

### Category 3: ARIA & Accessibility Attributes (Weight: 15%)

**What agents need:** Role and state information for complex widgets.

  ------------------------------------------------------------------------
  Check                      Pass                   Fail
  -------------------------- ---------------------- ----------------------
  Custom interactive         Role present           No role on custom
  components have `role`                            widgets
  attribute                                         

  Dynamic content areas have Attribute present      No live region
  `aria-live`                                       announcements

  Images have `alt` text     Alt present            Missing alt

  Icon-only buttons have     Label present          No accessible name
  `aria-label`                                      
  ------------------------------------------------------------------------

**Detection method:** Pattern match for components with event handlers
that lack ARIA attributes.

### Category 4: Structured Data (Weight: 15%)

**What agents need:** Machine-readable metadata about what the page/app
contains.

  -----------------------------------------------------------------------------------------
  Check                      Pass                                    Fail
  -------------------------- --------------------------------------- ----------------------
  Schema.org JSON-LD present `<script type="application/ld+json">`   No structured data
  in HTML                    found                                   

  Open Graph meta tags       `<meta property="og:...">` found        No OG tags
  present                                                            

  Page has descriptive       Title tag with content                  Empty or missing title
  `<title>`                                                          

  Meta description present   `<meta name="description">` found       Missing
  -----------------------------------------------------------------------------------------

**Detection method:** String search in HTML head sections.

### Category 5: Content in HTML (Weight: 15%) --- LOW CONFIDENCE ⚠️

**What agents need:** Content that exists in the initial HTML, not
behind JavaScript rendering.

**Confidence level: LOW in Path A (source-only scanning).** This
category is inherently unreliable without fetching the deployed URL. We
constrain to safe, high-confidence checks only. Everything beyond these
checks is Claude advisory, not verdict.

**Safe checks (Python --- scored):**

  --------------------------------------------------------------------------------
  Check                      Pass                      Fail
  -------------------------- ------------------------- ---------------------------
  HTML files are NOT empty   Content beyond            File is essentially
  root shells                `<div id="root"></div>`   `<div id="root"></div>` +
                                                       script tags only

  `<noscript>` fallback      Tag found                 No fallback
  present                                              

  SSR framework markers      `__NEXT_DATA__`, Nuxt     No SSR indicators
  present                    markers, Astro indicators 
                             detected                  
  --------------------------------------------------------------------------------

**Claude advisory (NOT scored --- mentioned in report as context):**

-   Whether the project structure suggests SSR/SSG (e.g., Next.js
    `pages/` or `app/` directory, Astro components)
-   Whether meaningful text content appears in source files vs. being
    loaded from API calls
-   Overall assessment of how much content an agent would see without
    JavaScript

**Detection method:** Check if HTML files contain meaningful text
content or are empty shells. Check for SSR indicators.

**Why low confidence:** A React SPA with excellent client-side rendering
might score poorly here because content lives in JS state, not HTML
source. But agents accessing the deployed URL (not source code) would
see the rendered content just fine. Scoring this definitively from
source alone erodes trust. Better to flag it honestly and let Claude
provide context.

**Path B upgrade (stubbed):** When deployed URL scanning is available,
this category becomes high-confidence by comparing source vs. rendered
DOM.

### Category 6: Link & Navigation Clarity (Weight: 10%)

**What agents need:** Predictable, descriptive navigation.

  ------------------------------------------------------------------------
  Check                      Pass                   Fail
  -------------------------- ---------------------- ----------------------
  Links have descriptive     Meaningful text        Generic text like
  text (not "click here")                           "click here", "learn
                                                    more", "read more"

  Links have `href`          href present           `<a onClick="...">`
  attributes (not JS-only                           without href
  navigation)                                       

  Navigation structure is    `<nav>` with links     Navigation scattered
  consistent                                        in divs
  ------------------------------------------------------------------------

**Detection method:** Parse anchor tags, check text content and
attributes.

### Scoring Formula (Python --- Mechanical)

    Raw Score = (Cat1 × 0.25) + (Cat2 × 0.20) + (Cat3 × 0.15) + (Cat4 × 0.15) + (Cat5 × 0.15) + (Cat6 × 0.10)

Each category score = (passing checks / total applicable checks) ×
category max points.

**Claude may adjust the final score** based on reasoning (e.g., "the raw
score is 52 but the semantic HTML is excellent --- the low score is
entirely due to missing Schema.org which is a 5-minute fix. Adjusted
context score: 58."). Claude explains any adjustment.

### Score Ranges

-   **80-100:** Agent-Ready --- agents can navigate and interact with
    this app
-   **60-79:** Partially Ready --- agents can find content but struggle
    with interactions
-   **40-59:** Agent-Challenged --- agents can see the page but can't do
    much with it
-   **0-39:** Agent-Invisible --- agents bounce immediately

------------------------------------------------------------------------

## 8. Claude Reasoning Layer

This is what separates Hermes Clew from a dumb linter. Claude doesn't
just format results --- it reasons about them.

### What Claude Does

1.  **Receives** raw JSON findings from the Python scan engine
2.  **Analyzes** patterns across categories (e.g., "great semantic HTML
    but zero structured data")
3.  **Catches false positives** (e.g., "these divs are from a charting
    library, not interactive elements")
4.  **Weighs severity** (e.g., "missing alt text on 2 decorative images
    is minor; missing form labels on a checkout page is critical")
5.  **Identifies quick wins** (e.g., "adding 4 lines of Schema.org
    JSON-LD would jump your score 15 points")
6.  **Generates** the final report in the developer's language,
    referencing their actual file names and patterns

### Claude Reasoning Prompt

    You are the reasoning layer of Hermes Clew, an agent-readiness scanner.

    You have received raw scan findings from a mechanical Python scanner. The scanner counts patterns — it does not understand context. Your job is to reason about these findings and produce a defensible, nuanced assessment.

    ## Raw Findings
    {raw_scan_json}

    ## Your Tasks

    1. REVIEW each category's findings for false positives. Common false positives:
       - React component libraries that use custom components (e.g., <Button>) that render to semantic HTML at build time
       - CSS-in-JS frameworks that produce div wrappers for styling but don't affect interactivity
       - Data visualization libraries that use many divs for chart containers
       - SPAs that use client-side routing (React Router, etc.) — href-less links may be intentional

    2. ASSESS severity. Not all failures are equal:
       - A missing <button> on a checkout CTA is critical
       - A missing alt on a decorative background is minor
       - Missing Schema.org on a personal portfolio is less urgent than on an e-commerce site

    3. IDENTIFY the top 3 highest-impact fixes. Rank by: smallest code change that produces the biggest score improvement.

    4. GENERATE the report sections:
       - "What's Working" — 2-3 specific positives, referencing actual files/patterns
       - "What Agents Struggle With" — Top 3 issues with WHY (from the agent's perspective) and a concrete fix example
       - "Suggested Fixes" — Ranked by impact. Include estimated score improvement.

    5. If you adjust the raw score, explain why in one sentence.

    ## Tone
    Friendly, educational, zero judgment. Like a knowledgeable colleague pointing things out over coffee. Use the phrase "awareness, not judgment" if it fits naturally. Never be preachy.

### Why This Is Defensible

If a developer disagrees with a finding, they can see: - The raw Python
check (mechanical, transparent) - Claude's reasoning about that check
(contextual, explained) - The specific fix suggestion (actionable)

This three-layer transparency --- data, reasoning, recommendation --- is
what makes Hermes Clew trustworthy instead of annoying.

------------------------------------------------------------------------

## 9. Output: The Report

The agent posts a markdown report to GitLab Duo Chat. The report itself
is structured so it is agent-readable (practicing what we preach).

### Report Template

``` markdown
# Hermes Clew — Agent Readiness Report

**Project:** {project_name}
**Files Scanned:** {file_count} HTML/JSX/TSX files
**Scan Date:** {date}

---

## Overall Score: {score}/100 — {rating}

| Category | Score | Status |
|----------|-------|--------|
| Semantic HTML | {cat1}/25 | {status} |
| Form Accessibility | {cat2}/20 | {status} |
| ARIA & Accessibility | {cat3}/15 | {status} |
| Structured Data | {cat4}/15 | {status} |
| Content in HTML | {cat5}/15 | {status} |
| Link & Navigation | {cat6}/10 | {status} |

{score_adjustment_note_if_any}

---

## What's Working
{claude_generated_positives}

## What Agents Struggle With
{claude_generated_issues_with_explanations}

## Suggested Fixes (Smallest Changes, Biggest Impact)
{claude_generated_fixes_ranked_by_impact}

---

*Hermes Clew — Awareness, not judgment. Built for the agentic web.*
*Part of the Clew suite: ariadne-clew | janus-clew | lumen-clew | metis-clew | hermes-clew*
```

------------------------------------------------------------------------

## 10. Data Flow

    User opens GitLab Duo Chat
        ↓
    User selects Hermes Clew agent
        ↓
    User says: "Scan this project" (or "scan" or "check agent readiness")
        ↓
    LAYER 1 — GitLab Duo Agent:
        → Identifies HTML/JSX/TSX files in the current project
        → Triggers Python scan script
        ↓
    LAYER 2 — Scan Engine (Python):
        → Reads files (READ-ONLY, mode='r')
        → Runs 6 category checks (pattern matching)
        → Outputs raw JSON: scores + findings per category
        → NO reasoning, NO judgment, just counts and patterns
        ↓
    LAYER 3 — Claude Reasoning (Anthropic via GitLab):
        → Receives raw JSON
        → Reasons about context, false positives, severity
        → Generates final score (with adjustment explanation if needed)
        → Generates plain-English report sections
        → Returns formatted markdown report
        ↓
    LAYER 1 — GitLab Duo Agent:
        → Posts report to Duo Chat
        ↓
    User reads report

### What Does NOT Happen

-   No data is stored after the scan
-   No files are written to the repo
-   No code is modified
-   No external services are called (Claude accessed via GitLab's
    built-in Anthropic integration)
-   No cloned code persists (Path A reads files in-place; Path B stub
    would clone-scan-delete)
-   Completely stateless --- every scan is independent

------------------------------------------------------------------------

## 11. File Map

Every file has one job. File names describe the job. If any file starts
doing a second job, stop and create a new file.

    hermes-clew/
    ├── AGENTS.md                          # Describes project to any agent (agent-first principle)
    ├── README.md                          # Human-readable setup, usage, architecture, roadmap
    ├── LICENSE                            # MIT
    ├── .gitlab/
    │   └── duo/
    │       └── agent-config.yml           # GitLab Duo flow/agent configuration
    ├── scan/
    │   ├── __init__.py                    # Empty. Makes scan/ a Python package.
    │   ├── scanner.py                     # ENTRY POINT. Orchestrates checks → outputs JSON. No check logic here.
    │   ├── check_semantic_html.py         # Category 1 checks ONLY. Returns dict.
    │   ├── check_form_accessibility.py    # Category 2 checks ONLY. Returns dict.
    │   ├── check_aria.py                  # Category 3 checks ONLY. Returns dict.
    │   ├── check_structured_data.py       # Category 4 checks ONLY. Returns dict.
    │   ├── check_content_in_html.py       # Category 5 checks ONLY. Returns dict.
    │   ├── check_link_navigation.py       # Category 6 checks ONLY. Returns dict.
    │   ├── file_finder.py                 # Finds HTML/JSX/TSX files in repo. Returns list of paths. Nothing else.
    │   ├── scoring.py                     # Takes category dicts → applies weights → returns total. No HTML knowledge.
    │   ├── report_prompt.py               # Builds Claude reasoning prompt from raw JSON. Does NOT call Claude.
    │   └── external_url.py                # STUB: Path B external URL scanning. Raises NotImplementedError.
    ├── tests/
    │   ├── test_check_semantic_html.py    # Unit tests for Category 1
    │   ├── test_check_form_accessibility.py
    │   ├── test_check_aria.py
    │   ├── test_check_structured_data.py
    │   ├── test_check_content_in_html.py
    │   ├── test_check_link_navigation.py
    │   ├── test_scoring.py
    │   ├── test_file_finder.py
    │   └── fixtures/                      # Small, hand-written test HTML/JSX files
    │       ├── good_semantic.html         # Passes all Category 1 checks
    │       ├── bad_div_soup.html          # Fails Category 1 checks
    │       ├── good_form.html             # Passes Category 2 checks
    │       ├── bad_form.html              # Fails Category 2 checks
    │       ├── good_structured_data.html  # Has Schema.org, OG tags
    │       ├── bad_no_metadata.html       # No structured data at all
    │       ├── good_react_component.jsx   # Semantic React component
    │       └── bad_react_component.jsx    # Div-soup React component
    └── demo/
        ├── demo_repos.md                  # List of 5 repos to scan in demo, with expected scores
        └── scan_results/                  # Pre-generated scan results (backup if live scan fails in video)
            ├── repo1_results.json
            └── repo2_results.json

    # --- PLAN C ONLY (add if CI pipeline fallback needed) ---
    # .gitlab-ci.yml                      # Pipeline definition with hermes-scan job
    # scan/ci_wrapper.sh                  # Shell script: runs scanner.py, saves JSON as CI artifact

### File Responsibility Rules (The Law)

-   `scanner.py` calls the check files. It does NOT contain check logic.
-   Each `check_*.py` file returns a dict:
    `{"score": int, "max": int, "findings": [{"check": str, "passed": bool, "detail": str}]}`
-   `scoring.py` takes those dicts, applies weights, returns total. It
    does NOT know about HTML.
-   `report_prompt.py` builds a Claude prompt string from JSON. It does
    NOT call Claude.
-   `file_finder.py` returns a list of file paths. It does NOT read file
    contents.
-   `external_url.py` raises `NotImplementedError`. It does NOTHING
    else.

**If any file starts doing a second job, stop and refactor into a new
file.**

------------------------------------------------------------------------

## 12. Security & Data Protection

### Threat Model

  -----------------------------------------------------------------------
  Threat             Severity                Mitigation
  ------------------ ----------------------- ----------------------------
  Agent modifies     CRITICAL                Agent has NO write tools.
  files in repo                              All `open()` calls use `'r'`
                                             mode only.

  Scan script        HIGH                    Script reads files as text
  executes code from                         strings. Zero `eval()`,
  scanned files                              `exec()`, or dynamic
                                             imports.

  API keys exposed   HIGH                    No API keys in code. Claude
  in repo                                    accessed via GitLab's
                                             built-in Anthropic
                                             integration. No `.env`
                                             files.

  Malicious          MEDIUM                  `file_finder.py` sanitizes
  filenames (path                            paths. Only
  traversal)                                 `.html`/`.jsx`/`.tsx`
                                             extensions. No symlinks. No
                                             `..` in paths.

  Report leaks       MEDIUM                  Report references file names
  sensitive code                             and pattern descriptions
  from scanned files                         only. Never includes full
                                             source code or code blocks
                                             from scanned files. Claude
                                             prompt explicitly instructs:
                                             "Do not reproduce source
                                             code in the report."

  Scanned project    MEDIUM                  Tool runs within GitLab's
  contains                                   security model. Agent only
  proprietary code                           accesses repos the user
                                             already has access to. No
                                             code leaves GitLab's
                                             infrastructure. Claude is
                                             accessed via GitLab's
                                             built-in integration --- not
                                             an external API call.
  -----------------------------------------------------------------------

### Data Protection Policy

1.  **No data storage.** Scan results are generated, posted to chat, and
    discarded. Nothing is written to disk, database, or external
    service.
2.  **No code reproduction.** The report never includes verbatim source
    code from the scanned project. It references file names and
    describes patterns.
3.  **No external transmission.** All processing happens within GitLab's
    infrastructure. Claude is accessed through GitLab's built-in
    Anthropic integration --- no API keys, no external endpoints.
4.  **GitLab's access model.** The agent can only access repos that the
    requesting user already has permission to view. It adds no new
    access.
5.  **Stateless.** Every scan is independent. No memory of previous
    scans. No user profiles. No tracking.

### Security Rules (Enforced in Code)

1.  Every `open()` call uses `mode='r'`. No exceptions.
2.  Zero `eval()` or `exec()` anywhere in the codebase.
3.  Zero `import` of any file from the scanned project.
4.  `file_finder.py` rejects paths containing `..`, rejects symlinks,
    rejects files outside project root.
5.  No environment variables. No `.env` files. No secrets in code.
6.  Claude is accessed ONLY through GitLab's Anthropic integration.
7.  Claude prompt includes: "Do not reproduce source code from the
    scanned files in the report."

### Security QA Checklist (Run Before Submission)

-   [ ] `grep -r "open(" scan/ | grep -v "'r'"` returns nothing
-   [ ] `grep -r "eval\|exec" scan/` returns nothing
-   [ ] `grep -r "import.*os.system\|subprocess" scan/` returns only
    sanitized calls in scanner.py
-   [ ] No `.env` file exists in repo
-   [ ] No API keys in any file:
    `grep -ri "api_key\|secret\|token\|password" scan/`
-   [ ] `file_finder.py` test confirms path traversal rejection
-   [ ] Claude prompt includes source code reproduction prohibition

------------------------------------------------------------------------

## 13. QA Plan

### Unit Tests (Write BEFORE Implementation)

Each `check_*.py` file gets a corresponding test file with: - One test
using a fixture file that should PASS all checks - One test using a
fixture file that should FAIL all checks - One edge case test (empty
file, file with only comments, etc.)

Test fixtures are committed to `tests/fixtures/`. They are small,
hand-written HTML/JSX files.

### Integration Test

`scanner.py` runs against `tests/fixtures/` and produces valid JSON with
all 6 categories populated.

### Acceptance Criteria (Definition of Done)

The project is DONE when:

1.  [ ] Agent is registered and public in GitLab hackathon group
2.  [ ] User can open Duo Chat, select Hermes Clew, ask it to scan
3.  [ ] Agent scans all HTML/JSX/TSX files in the current project
4.  [ ] Agent returns a report with a score and 6 category breakdowns
5.  [ ] Report includes Claude-reasoned explanations (not just formatted
    counts)
6.  [ ] All unit tests pass
7.  [ ] All security checks pass
8.  [ ] AGENTS.md exists and accurately describes the project
9.  [ ] README explains setup in \<5 minutes of reading
10. [ ] Demo video is ≤3 minutes and shows trigger → action → result
11. [ ] Devpost submission is complete with all required fields

### What We Do NOT Test

-   Performance / scan speed
-   Concurrent users
-   Edge cases beyond empty files and single-line files
-   Cross-browser (no browser --- it's a chat tool)

------------------------------------------------------------------------

## 14. Timeline (32 Days)

### Constraints

-   Solo builder
-   1-2 hours per day (evenings/weekends)
-   Never used GitLab before
-   \~48 total hours
-   No frontend work (tool, not app)

### Phase 0: Foundations (Days 1-7, \~10 hours)

**Goal:** Can I build and run a GitLab Duo custom agent? If NO at end of
Phase 0, reassess. Update Platform Capability Matrix (Section 18) with
spike outcomes.

-   [ ] Day 1-2: Create GitLab account. Request hackathon group access.
    Join Discord #ai-hackathon. **CRITICAL: Set Default GitLab Duo
    namespace to the hackathon group** (Settings → Preferences → GitLab
    Duo → Default namespace). Read GitLab Duo Agent Platform docs
    (overview + getting started).
-   [ ] Day 3-4: Complete GitLab Duo getting-started tutorial (Parts 1-3
    of their 8-part guide). Understand agents vs flows vs chat.
-   [ ] Day 5: **SPIKE 1** --- Create a trivial custom agent that
    responds to "hello" in Duo Chat. Verify it works. If it doesn't,
    check namespace setting FIRST.
-   [ ] Day 6: **SPIKE 2** --- Can the agent read files in the repo? Can
    it execute a Python script? **SPIKE 3** --- Is Anthropic Claude
    available? Which model? Does GitLab Duo integration count for
    Anthropic prize? **SPIKE 4** --- Is the agent already Claude?
    Document findings.
-   [ ] Day 7: **GO/NO-GO DECISION.** Update Platform Capability Matrix
    (Section 18) with all spike results. Follow decision tree to select
    Plan A/B/C/D. If Plan D is the only option, consider pivoting
    project. If Plan A/B/C, proceed.

**Exit Criteria:** A working custom agent in the hackathon group that
responds to chat. Platform Capability Matrix fully populated. Execution
plan (A/B/C) selected.

### Phase 1: Scan Engine (Days 8-16, \~12 hours)

**Goal:** Python scan script works, produces correct JSON for all 6
categories.

-   [ ] Day 8: Write test fixtures (good/bad HTML for each category).
    Write `file_finder.py` + test.
-   [ ] Day 9: Write `check_semantic_html.py` + test.
-   [ ] Day 10: Write `check_form_accessibility.py` + test.
-   [ ] Day 11: Write `check_aria.py` + test.
-   [ ] Day 12: Write `check_structured_data.py` +
    `check_content_in_html.py` + tests.
-   [ ] Day 13: Write `check_link_navigation.py` + test. Write
    `scoring.py` + test.
-   [ ] Day 14: Write `scanner.py` (orchestrator). Integration test
    against fixtures.
-   [ ] Day 15: Write `report_prompt.py`. Test prompt output manually
    (paste into Claude chat).
-   [ ] Day 16: Run full scan against 2-3 of own repos (pushed to
    GitLab). Verify results.

**Exit Criteria:** `python scanner.py /path/to/repo` produces valid JSON
with all 6 categories.

### Phase 2: Agent Integration (Days 17-24, \~10 hours)

**Goal:** Scan engine runs inside GitLab Duo, triggered from chat,
Claude reasons, report posted.

-   [ ] Day 17-18: Connect scan script to GitLab Duo agent/flow. Agent
    calls scanner, gets JSON.
-   [ ] Day 19-20: Agent sends JSON to Claude (via GitLab's Anthropic
    integration) with reasoning prompt. Gets report markdown.
-   [ ] Day 21: Agent posts formatted report to Duo Chat. End-to-end
    works.
-   [ ] Day 22: Push 5 demo repos to GitLab. Test scans on each. Note
    scores.
-   [ ] Day 23: Fix bugs from demo repo testing. Polish report
    formatting.
-   [ ] Day 24: Run all unit tests. Run all security checks. Fix
    failures.

**Exit Criteria:** User asks Hermes Clew to scan → agent reads files →
Claude reasons → formatted report posted.

### Phase 3: Submission (Days 25-32, \~8 hours)

**Goal:** Everything submitted, polished, documented.

-   [ ] Day 25: Write README (setup, usage, architecture, roadmap).
-   [ ] Day 26: Write AGENTS.md. Add stubs for Path B and other future
    features. Verify repo is agent-first.
-   [ ] Day 27: Record demo video (draft). Review for clarity.
-   [ ] Day 28: Re-record if needed. Upload to YouTube.
-   [ ] Day 29: Complete Devpost submission form.
-   [ ] Day 30: Final QA --- all acceptance criteria checked.
-   [ ] Day 31: Buffer day.
-   [ ] Day 32: Submit. Do not touch anything after submission.

### Buffer Rules

-   If Phase 0 takes longer than 7 days: cut Phase 3 buffer days.
-   If Phase 1 has a blocker: skip Category 5 (Content in HTML) ---
    hardest to assess from source.
-   If Phase 2 has agent-execution blocker: fall back to agent that
    instructs user to run script manually and paste results.
-   NEVER borrow time from Phase 3. Submission quality matters.

------------------------------------------------------------------------

## 15. Demo Plan (3-Minute Video)

### Structure

  ------------------------------------------------------------------------
  Time             Content                  On Screen
  ---------------- ------------------------ ------------------------------
  0:00-0:20        "AI agents are becoming  Text overlay or simple slide
                   the primary users of the 
                   web. But most vibecoded  
                   apps are invisible to    
                   them."                   

  0:20-0:40        "Hermes Clew is a GitLab GitLab project page, Duo Chat
                   Duo tool that scans your open
                   codebase and tells you   
                   how agent-ready your app 
                   is --- with              
                   Claude-powered           
                   reasoning."              

  0:40-1:30        Live demo: Open Duo Chat Screen recording of actual
                   → select Hermes Clew →   scan
                   "Scan this project" →    
                   agent runs → report      
                   appears                  

  1:30-2:10        Walk through report:     Scrolling through report in
                   score, categories,       chat
                   Claude's reasoning, fix  
                   suggestions              

  2:10-2:40        Show contrast: scan an   Side-by-side results
                   agent-ready repo (high   
                   score) vs an agent-poor  
                   repo (low score)         

  2:40-3:00        "Awareness, not          End card with repo link
                   judgment. Hermes Clew.   
                   Part of the Clew suite." 
  ------------------------------------------------------------------------

### Backup Plan

If live scan is flaky during recording: use pre-generated results from
`demo/scan_results/`. Note in video description that results are
pre-generated for clarity. Judges can test live if they choose.

------------------------------------------------------------------------

## 16. Hackathon Compliance: Trigger + Action

The hackathon requires projects that are "not chat-only" --- agents must
react to a trigger and take an action. This section maps Hermes Clew to
judging criteria explicitly.

### Trigger

**Primary:** User message in Duo Chat --- "scan this project", "check
agent readiness", or "hermes scan".

**Fallback (Plan C):** Manual or scheduled CI pipeline trigger (see Plan
C in Section 18). The agent/flow initiates the scan via pipeline rather
than direct Python execution.

### Action

The agent/flow takes the following concrete actions (not just chat
responses):

1.  **Identifies** HTML/JSX/TSX files in the project repository
2.  **Executes** the Python scan engine (via direct execution OR CI
    pipeline)
3.  **Produces** raw JSON findings
4.  **Invokes** Claude (Anthropic) to reason about findings
5.  **Posts** a structured Agent Readiness Report back to Duo Chat

This is NOT chat-only. The agent reads files, runs analysis, invokes an
AI model for reasoning, and produces a structured deliverable. Each step
is a distinct action, not a conversational reply.

### Judging Criteria Mapping

  -----------------------------------------------------------------------
  Hackathon Criterion             How Hermes Clew Meets It
  ------------------------------- ---------------------------------------
  At least one public custom      Hermes Clew is a public custom agent in
  agent or flow                   the hackathon group

  Reacts to a trigger             Trigger: user message in Duo Chat
                                  ("scan this project")

  Takes an action                 Action: scans files, runs analysis,
                                  invokes Claude, posts report

  Runs on GitLab Duo Agent        Built on Duo Agent Platform with
  Platform                        agent/flow configuration

  Public repo in hackathon group  Yes, MIT licensed

  Demo video ≤3 min               Yes, shows trigger → action → result
  -----------------------------------------------------------------------

### GitLab-Specific Setup Gotcha

**CRITICAL:** You must set your Default GitLab Duo namespace to the
hackathon group, or agents/flows won't run properly. This is documented
in the participant onboarding notes. Set this FIRST in Phase 0, before
any spike work. If agents aren't responding, this is the most likely
cause.

Instructions: GitLab → Settings → Preferences → GitLab Duo → Default
namespace → select the AI Hackathon group.

------------------------------------------------------------------------

## 17. Anthropic Track Compliance

Hermes Clew targets the Anthropic prize track (\$10K+). This section
documents exactly how Anthropic is used "through GitLab" to satisfy
prize eligibility.

### Integration Path

Claude (Anthropic) is accessed through GitLab's built-in model
integration --- NOT via a direct API call to Anthropic. This means:

-   No Anthropic API key in the codebase
-   No direct calls to `api.anthropic.com`
-   Claude is invoked via GitLab Duo's model selector / agent
    configuration
-   GitLab handles the Anthropic integration, billing, and model routing

### Role in Architecture

Claude is NOT a formatting layer. It is the core reasoning engine (Layer
3):

  ------------------------------------------------------------------------
  Step           Component                  What It Does
  -------------- -------------------------- ------------------------------
  1              Python Scan Engine         Mechanical pattern detection
                                            --- counts, finds, flags

  2              Claude (Anthropic)         Reasons about findings ---
                                            catches false positives,
                                            weighs severity, identifies
                                            quick wins, generates
                                            plain-English explanations

  3              Report Output              Claude's reasoning formatted
                                            as structured markdown
  ------------------------------------------------------------------------

Without Claude, Hermes Clew is a dumb linter. Claude is what makes it a
reasoning tool.

### Proof in Demo

The demo video will show one or more of:

-   Model name visible in agent configuration (e.g.,
    `anthropic/claude-*` in the Duo settings)
-   Claude's reasoning visible in the report (contextual judgments that
    a rule-based engine couldn't produce)
-   The agent config YAML specifying the Anthropic model

### SPIKE REQUIRED

Verify during Phase 0:

-   [ ] Which Anthropic model(s) are available in the hackathon group?
    (Claude Sonnet 4, Claude Haiku 4.5, etc.)
-   [ ] How is the model specified in the agent/flow configuration?
    (model selector field? YAML key?)
-   [ ] Is there a way to log or display the model name in the agent's
    response?
-   [ ] Does using Anthropic through GitLab Duo count for the Anthropic
    prize track? (Confirm via Discord/rules.)

------------------------------------------------------------------------

## 18. Platform Capability Matrix

**This is the single biggest risk.** The entire build depends on GitLab
Duo Agent Platform capabilities that may be feature-flag controlled,
availability-gated, or undocumented. "It should work" is not a plan.

### Capability Matrix

Each capability is verified during Phase 0 spikes. Status is updated as
spikes complete.

  ------------------------------------------------------------------------
  Capability    Required By     Spike    Status    Fallback if FAIL
  ------------- --------------- -------- --------- -----------------------
  Custom agent  Everything      Spike 1  ⬜ NOT    Switch to flow instead
  responds in                   (Day 5)  TESTED    of custom agent
  Duo Chat                                         

  Agent can     Scan engine     Spike 2  ⬜ NOT    Flow triggers CI job
  read files in                 (Day 6)  TESTED    that reads files
  repo                                             

  Agent can     Scan engine     Spike 2  ⬜ NOT    **Plan C: CI pipeline
  execute                       (Day 6)  TESTED    fallback** (see below)
  Python script                                    

  Anthropic     Reasoning layer Spike 3  ⬜ NOT    Use GitLab's default
  Claude                        (Day 6)  TESTED    model; may lose
  available                                        Anthropic prize

  Agent can     Two-step AI     Spike 4  ⬜ NOT    If agent IS Claude,
  invoke Claude                 (Day 6)  TESTED    reasoning is built-in
  for reasoning                                    (simpler)

  Duo namespace Everything      Day 1    ⬜ NOT    Follow onboarding docs
  set to                        setup    TESTED    exactly
  hackathon                                        
  group                                            
  ------------------------------------------------------------------------

### Plan A: Agent Executes Python Directly (Ideal)

    User → Duo Chat → Custom Agent → runs Python scanner → sends JSON to Claude → posts report

This is the cleanest path. Agent has file access and script execution.
One tool, one flow.

### Plan B: Agent Reads Files, Sends to Claude for Analysis (No Python)

    User → Duo Chat → Custom Agent → reads files directly → sends file content to Claude → Claude does both scanning + reasoning → posts report

If the agent can read files but can't run Python, we skip the Python
scan engine entirely. Claude receives the raw file content and performs
both the pattern detection AND reasoning in a single prompt. This works
because Claude can count semantic tags, check for ARIA attributes, etc.
The prompt engineering just needs to be more detailed.

**Tradeoff:** Slower (more tokens per scan), less structured (no JSON
intermediate), but functional.

### Plan C: CI Pipeline Fallback (If Agent Can't Execute OR Read Files)

    User → Duo Chat → Agent/Flow triggers CI pipeline → pipeline runs Python scanner → stores JSON as artifact → Agent reads artifact → sends to Claude → posts report

This is the critical fallback your CTO flagged. If the agent can't
directly execute Python or read arbitrary files, we route through GitLab
CI/CD:

1.  Agent/flow receives user request in Duo Chat
2.  Agent triggers a CI pipeline job (via GitLab API or flow action)
3.  Pipeline job runs `python scanner.py` in a CI runner
4.  Scanner output (JSON) is stored as a CI artifact
5.  Agent/flow retrieves the artifact
6.  Agent sends JSON to Claude for reasoning
7.  Agent posts report to Duo Chat

**Why this still qualifies for the hackathon:** The agent reacts to a
trigger (chat message) and takes an action (triggers pipeline, retrieves
results, reasons, reports). It's not chat-only --- it orchestrates a
multi-step workflow. The scan still happens automatically. The user
doesn't run anything manually.

**Additional files needed for Plan C:**

    .gitlab-ci.yml              # Pipeline definition with scan job
    scan/ci_wrapper.sh           # Shell script that runs scanner and saves artifact

**When to activate Plan C:** If Spike 2 fails (agent can't execute
Python AND can't read files), implement Plan C starting Day 8. This adds
\~3 hours to Phase 1 for CI pipeline setup.

### Plan D: Nuclear Fallback (Agent Is Extremely Limited)

    User → runs Python scanner locally → pastes JSON into Duo Chat → Agent sends to Claude → posts report

This is survival mode. It works, but it's weak for judging because the
user does manual work. Only use if Plans A, B, and C all fail.

**If Plan D is the only option:** Reframe in the demo as "bring your
scan results to Hermes Clew for AI-powered analysis" --- emphasize the
Claude reasoning value, not the automation.

### Decision Tree (Phase 0 Exit)

    Can agent respond in Duo Chat?
    ├── NO → Ask Discord. If unresolved in 2 days, pivot project entirely.
    └── YES →
        Can agent execute Python?
        ├── YES → PLAN A ✅ (ideal path)
        └── NO →
            Can agent read repo files?
            ├── YES → PLAN B (Claude does scanning + reasoning)
            └── NO →
                Can agent/flow trigger CI pipeline?
                ├── YES → PLAN C ✅ (CI fallback — strong)
                └── NO → PLAN D (manual paste — survival mode)

------------------------------------------------------------------------

## 19. Submission Checklist

Per hackathon requirements:

-   [ ] **URL to project in GitLab AI Hackathon group** --- public, MIT
    licensed, license visible at top
-   [ ] **All source code, assets, instructions** --- repo is
    self-contained
-   [ ] **Text description** --- features and functionality (Devpost
    form)
-   [ ] **Demo video ≤3 minutes** --- YouTube, public, shows trigger →
    action → result
-   [ ] **At least one custom public agent or flow** --- Hermes Clew is
    a custom public agent
-   [ ] **Agent reacts to trigger and takes action** --- trigger: user
    asks to scan. Action: scans and posts report.
-   [ ] **Uses Anthropic through GitLab** --- Claude is the reasoning
    layer (targets \$10K+ Anthropic prize track)
-   [ ] **Default Duo namespace set to hackathon group** --- verified
    during setup
-   [ ] **Anthropic track proof** --- model name visible in config or
    demo

------------------------------------------------------------------------

## 20. Stubbed Features (Post-Hackathon)

These features are mentioned in code comments and README "Roadmap"
section but have ZERO implementation.

### Stub Format in Code

``` python
# STUB: {Feature Name}
# Post-hackathon: {One-sentence description of what this would do.}
# See PRD Section 20 for specification.
def stub_function_name() -> None:
    raise NotImplementedError("{Feature Name} — post-hackathon feature")
```

### Stubbed Features List

1.  **Path B: External URL Scanning** --- Accept public GitHub URL or
    deployed URL. Clone, scan, report, delete.
2.  **MR-Triggered Scanning** --- Scan runs on MR open. Report posted as
    MR comment.
3.  **Score Threshold Gate** --- Team configures min score in config. MR
    blocked below threshold.
4.  **Historical Tracking** --- Store scores per commit. Trend line.
    Regression alerts.
5.  **NLWeb Compatibility** --- Check if app could serve as NLWeb
    endpoint.
6.  **MCP Endpoint Detection** --- Check if app exposes MCP-compatible
    interfaces.
7.  **Visual Split-Screen** --- Generate "human view vs agent view"
    comparison image.
8.  **Fix Diff Generation** --- Generate code diffs for suggested fixes
    (still read-only).

------------------------------------------------------------------------

## 21. Known Risks & Mitigations

  -------------------------------------------------------------------------------
  Risk              Likelihood            Impact          Mitigation
  ----------------- --------------------- --------------- -----------------------
  **Platform        HIGH                  CRITICAL        Platform Capability
  capabilities are                                        Matrix (Section 18).
  feature-gated**                                         Every dependency has a
  (CTO flag A)                                            spike + fallback. "It
                                                          should work" is not a
                                                          plan.

  GitLab learning   HIGH                  CRITICAL        Start Day 1. If Day 5
  curve exceeds                                           spike fails, simplify
  Phase 0                                                 to flow instead of
                                                          custom agent.

  Custom agent      MEDIUM                HIGH            Spike Day 6. **Plan C:
  can't execute                                           CI pipeline fallback**
  Python (CTO flag                                        --- agent triggers
  B)                                                      pipeline, scanner runs
                                                          in CI runner, agent
                                                          reads artifact. Still
                                                          qualifies as "reacts +
                                                          takes action." See
                                                          Section 18.

  Anthropic not     LOW                   HIGH            Spike Day 6. Verify
  available /                                             model selector,
  unclear what                                            invocation path, and
  "counts" (CTO                                           whether GitLab Duo
  flag E)                                                 integration counts for
                                                          prize. Confirm via
                                                          Discord. See Section
                                                          17.

  JSX/TSX regex     MEDIUM                MEDIUM          Explicitly heuristic,
  produces false                                          not AST. Claude softens
  positives (CTO                                          false positives. If
  flag C)                                                 unreliable, fall back
                                                          to HTML-only. See
                                                          Section 7 disclaimer.

  Category 5 erodes MEDIUM                HIGH            Labeled LOW CONFIDENCE.
  trust with wrong                                        Only safe checks
  SSR/CSR scoring                                         scored. Everything else
  (CTO flag D)                                            is Claude advisory. See
                                                          Section 7 Category 5.

  Scope creep /     HIGH (historical)     HIGH            This PRD is the
  "cool feature"                                          contract. NEVER =
  distraction                                             never. STUB = comment.
                                                          Re-read Section 3 when
                                                          tempted.

  Demo repos all    LOW                   MEDIUM          Pre-select 5 repos in
  score similarly                                         Phase 1 --- need at
                                                          least one high and one
                                                          low scorer.

  Video recording   MEDIUM                MEDIUM          Script in Section 15.
  drags on                                                Max 2 takes. Ship what
                                                          you have.

  Claude reasoning  MEDIUM                MEDIUM          Test prompt on 5+ repos
  produces                                                during Phase 2. Refine
  inconsistent                                            prompt if results are
  results                                                 inconsistent. Pin to
                                                          specific phrasing.

  Duo namespace not HIGH                  CRITICAL        Set FIRST in Phase 0
  set to hackathon                                        Day 1. If agents aren't
  group (CTO flag)                                        responding, check this
                                                          before debugging
                                                          anything else. See
                                                          Section 16.
  -------------------------------------------------------------------------------

------------------------------------------------------------------------

## 22. Spikes (Verify Before Building)

### Spike 1: GitLab Duo Custom Agent Basics (Day 5, 2 hours max)

**Question:** Can I create a custom agent that responds in Duo Chat?
**Steps:** 1. Follow docs: create custom agent in hackathon group
project 2. Simple system prompt: "You are a helpful assistant" 3. Enable
in project 4. Open Duo Chat, select agent, say "hello" **Pass:** Agent
responds. **Fail:** Ask Discord. If unresolved in 1 day, pivot to
flow-only.

### Spike 2: Agent File Access + Script Execution (Day 6, 2 hours max)

**Question:** Can a custom agent read repo files and/or run a Python
script? **Steps:** 1. Ask agent to list files in project 2. Ask agent to
read README.md contents 3. If agent can read but not execute: evaluate
Plan B (Claude does scanning + reasoning) 4. If agent can't read OR
execute: test triggering a CI pipeline from a flow 5. Test: simple
Python script that prints file names, run via agent/flow/pipeline
**Pass:** Agent returns file contents or script output → Plan A.
**Partial:** Agent reads but can't execute → Plan B. **Fail:** CI
pipeline works → Plan C. **Total fail:** Plan D (see Section 18 decision
tree).

### Spike 3: Anthropic Claude Access (Day 6, 30 minutes max)

**Question:** Is Claude available in the hackathon group? **Steps:** 1.
Try using Anthropic model in Duo Chat 2. Check hackathon docs/Discord
for Anthropic confirmation 3. Test simple Claude generation task
**Pass:** Claude works. **Fail:** Use default model. Note Anthropic
prize may not be eligible.

### Spike 4: Custom Agent Invoking Claude Separately (Day 6, 30 minutes max)

**Question:** If the custom agent IS Claude, can it still call Claude
separately for the reasoning step? Or is it one and the same?
**Steps:** 1. Determine if custom agent's underlying model is Claude 2.
If yes: the reasoning layer IS the agent itself --- no separate call
needed. Adjust architecture. 3. If no: agent needs to invoke Claude
explicitly for reasoning. **Impact on architecture:** If the agent IS
Claude, simplify to: agent runs Python scan → agent reasons about
results itself → agent posts report. Two layers, not three.

------------------------------------------------------------------------

## 23. Glossary

  -----------------------------------------------------------------------
  Term                      Definition
  ------------------------- ---------------------------------------------
  **Agentic Web**           The emerging internet paradigm where AI
                            agents are primary users of websites

  **Agent-Ready**           A web application that AI agents can
                            navigate, understand, and interact with

  **Clew Suite**            Shara's collection of developer tools named
                            after Greek/Roman mythology

  **Div-Soup**              HTML markup using generic `<div>` and
                            `<span>` instead of semantic tags

  **GitLab Duo**            GitLab's AI-powered developer platform with
                            agents, flows, and chat

  **Custom Agent**          A user-defined agent on GitLab Duo with
                            custom system prompt and tools

  **Flow**                  A GitLab Duo multi-step workflow combining
                            agents and tools

  **Hermes**                Greek messenger god who moved between worlds
                            --- bridges human web and agent web

  **MCP**                   Model Context Protocol --- Anthropic's
                            standard for AI-to-tool communication

  **NLWeb**                 Microsoft's protocol for natural language
                            interfaces on websites

  **A2A**                   Agent-to-Agent protocol by Google

  **Schema.org**            Vocabulary for structured data markup used by
                            search engines and AI agents

  **Semantic HTML**         HTML tags (`<button>`, `<nav>`, `<form>`)
                            that describe purpose, not just appearance

  **STUB**                  Placeholder in code indicating future
                            functionality with zero current
                            implementation

  **Vibecoder**             Developer who uses AI tools to generate code
                            while providing creative direction
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## End of PRD

This document is the single source of truth for Hermes Clew.

Every build decision references this document. If something isn't here,
it's not in the build. If the build contradicts this document, the build
is wrong.

**Re-read Section 3 (Scope Contract) before every build session.**

**Now go build.** 🕯️

------------------------------------------------------------------------

# v1.3 Patch --- Platform Resilience & Judge Alignment Updates

## 1. Updated Buffer Rules (Replaces Prior Fallback Language)

If Phase 2 has an agent-execution blocker:

-   Activate **Plan C (CI pipeline fallback)** first.
-   If Plan C is impossible due to platform constraints, activate **Plan
    D (manual paste survival mode)**.
-   Manual script execution by the user is the *last* fallback, not the
    default fallback.

This ensures Hermes Clew still qualifies as "trigger + action" under
hackathon rules.

------------------------------------------------------------------------

## 2. Plan B Hard Constraints (Token & Repo Volume Controls)

To prevent token overflow and scanning instability:

-   Maximum files scanned: 100
-   Maximum file size: 50KB per file
-   Excluded directories: node_modules/, dist/, build/, .next/,
    coverage/, .git/
-   Prioritized directories: src/, app/, pages/, components/
-   Files are sorted by likelihood of containing interactive markup
    before inclusion

If limits are exceeded: - The scan engine logs skipped files - Claude
reasoning layer includes note: "Partial scan due to file limits"

This prevents token exhaustion and maintains consistent performance.

------------------------------------------------------------------------

## 3. Plan C Validation Clarification

Plan C requires explicit validation during Spike 2:

-   Confirm agent or flow can trigger a GitLab CI pipeline.
-   Confirm pipeline can store JSON artifact.
-   Confirm agent/flow can retrieve artifact output.

If any of the above fails: - Plan C degrades to manual pipeline trigger
(still qualifies as action). - Plan D becomes final fallback.

------------------------------------------------------------------------

## 4. Anthropic Track Compliance Clarification

Hermes Clew will:

-   Use the Anthropic model available in the GitLab Duo environment.
-   Log the exact model identifier discovered during Spike 3.
-   Display model identifier in demo (if possible) or log output.

Model name examples previously listed are placeholders and will be
replaced with the verified identifier available in the hackathon group.

------------------------------------------------------------------------

## 5. Platform Capability Matrix Enhancement

Add a column titled:

**Proof Artifact** --- screenshot, log output, or GitLab issue link
confirming capability was validated.

This provides evidence during judging and strengthens technical
credibility.

------------------------------------------------------------------------

# End v1.3 Patch
