# Spike Results — Platform Capability Validation

**Project:** Hermes Clew — Agent Readiness Scanner
**Date:** February 22, 2026
**Auditor:** Shara (earlgreyhot1701D)

---

## Spike 1: GitLab Duo Custom Agent Basics

**Question:** Can I create a custom agent that responds in Duo Chat?

**Result:** ✅ PASS

**Evidence:** Created `agents/agent.yml` with system prompt and tool declarations. Agent registered in GitLab Duo catalog (catalog_id: `gid://gitlab/Ai::Catalog::Item/1003645`). Agent responds to user messages in Duo Chat within the hackathon project.

**Key Finding:** Agent YAML lives at `agents/agent.yml` (not `.gitlab/duo/`). Registration happens automatically via `.ai-catalog-mapping.json`.

---

## Spike 2: Agent File Access + Script Execution

**Question:** Can the agent read repo files and/or run Python?

**Result:** ⚠️ PARTIAL

**Evidence:**
- ✅ Agent can read files via `read_file` and `read_files` tools
- ❌ Agent cannot execute Python scripts directly (no shell/exec tool available)
- ✅ Agent reads file contents and reasons about them in a single pass

**Fallback Selected:** Plan B/C hybrid — Agent reads files directly via `read_file` tools. CI pipeline runs the deterministic Python scanner separately, producing a JSON artifact. Agent can reference the CI artifact or perform its own analysis using the system prompt's scoring model.

**Key Finding:** The agent IS Claude. When it reads files, it can apply the scoring rubric from the system prompt directly. The Python scan engine runs in CI as a reproducible, deterministic layer. The agent provides the reasoning layer.

---

## Spike 3: Anthropic Claude Access

**Question:** Is Claude available in the hackathon group? Which model?

**Result:** ✅ PASS

**Evidence:** GitLab Duo Chat uses Anthropic Claude as the underlying model for custom agents. No separate API key needed — Claude is accessed through GitLab's built-in Anthropic integration.

**Key Finding:** The agent's responses are Claude responses. The system prompt in `agents/agent.yml` IS the Claude reasoning layer configuration. No separate Claude invocation is needed.

---

## Spike 4: Custom Agent Invoking Claude Separately

**Question:** Can the agent call Claude separately, or is the agent already Claude?

**Result:** ✅ PASS — Agent IS Claude

**Evidence:** The custom agent's underlying model is Claude (via GitLab's Anthropic integration). When the agent reads files and produces a report, that IS Claude reasoning. There is no need for a separate Claude API call.

**Impact:** This simplifies the architecture significantly:
- Layer 1 (Interface) + Layer 3 (Reasoning) = the agent itself
- Layer 2 (Deterministic scan) = Python engine in CI pipeline
- The agent consumes CI scan results and adds contextual reasoning

**Key Finding:** The three-layer architecture still holds, but Layers 1 and 3 are the same Claude instance. The system prompt configures Claude to behave as both the interface and the reasoning engine.

---

## Platform Capability Matrix (Updated)

| Capability | Status | Plan | Notes |
|-----------|--------|------|-------|
| Custom agent responds in Duo Chat | ✅ TESTED | — | Works as expected |
| Agent reads repo files | ✅ TESTED | Plan B | Via read_file/read_files tools |
| Agent executes Python | ❌ NOT AVAILABLE | Plan C | CI pipeline runs Python instead |
| Anthropic Claude available | ✅ TESTED | — | Built into Duo agent |
| Agent IS Claude | ✅ CONFIRMED | — | No separate invocation needed |
| CI pipeline runs scanner | ✅ TESTED | Plan C | Green pipeline, JSON artifact published |
| CI artifact accessible | ✅ TESTED | Plan C | 7-day expiry, downloadable |
| Duo namespace set to hackathon group | ✅ CONFIRMED | — | Required for agent visibility |

---

## Architecture Decision

Based on spike results, Hermes Clew uses a **Plan B/C hybrid**:

1. **CI Pipeline** runs the deterministic Python scan engine → produces `hermes_clew_scan_results.json` artifact
2. **Duo Chat Agent** (which IS Claude) reads repo files directly, applies the scoring rubric from its system prompt, and generates the Agent Readiness Report
3. The CI artifact serves as a reproducible, auditable record of the mechanical scan

This gives us the best of both worlds: deterministic reproducibility (CI) + contextual reasoning (Claude agent).

---

*Last updated: February 22, 2026*
