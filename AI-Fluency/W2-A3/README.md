# Prompt Iteration Log — Foundations Assignment

Part of the AI Fluency Internship (FlyRank.ai × 10x.ai × Anthropic, July 2026 Cohort).

## Overview

This repo documents a structured prompt-engineering exercise: take one real task, write the naive prompt you'd have used before learning any technique, then iterate five more times — each version applying exactly one named technique — and compare the final result across models.

The goal wasn't to write a "good prompt." It was to isolate *which specific technique* produces *which specific change* in output, so the reasoning is reusable on tasks this repo never saw.

## Task

Writing a LinkedIn caption to announce a completed backend internship milestone (FastAPI JSON-endpoint assignment), aimed at recruiters and founders evaluating junior AI-automation talent. Pulled directly from the FL-01 AI Workflow Audit — a real, recurring task, not a toy example.

## What's inside

| Version | Technique | What changed |
|---|---|---|
| V0 | — (naive baseline) | Generic, could describe any internship anywhere |
| V1 | Role assignment | Tone shifted from "grateful journey" to engineer-voice |
| V2 | Context & motivation | Model produced a real, specific claim instead of a summary |
| V3 | Few-shot examples | Output borrowed sentence structure, not just tone |
| V4 | Output structure | First version usable without a manual edit pass |
| V5 | Step decomposition | Model selected among alternatives instead of first-plausible-idea |

Each version includes the exact prompt, the verbatim output, and a note on the observed difference — not just what was changed, but why it mattered.

## Cross-model comparison

The final (V5) prompt was run on Claude and ChatGPT. Findings are specific, not "both were fine": constraint-following (character limits, hashtag caps) diverged more than tone did. Full breakdown in the log.

## Reusable template

The final deliverable is a fill-in-the-blank template — role, context, examples, output constraints, step decomposition — designed to work on any "announce a completed task" prompt, not just this one. See `prompt_iteration_log.pdf` for the full template with usage notes.

## Files

- `prompt_iteration_log.pdf` — full iteration log, cross-model comparison, and template

---
# Author

**Riffat Yasmeen**

BS Computer Science  
Flyrank internship cohort July 2026.

*Built as part of Anthropic's Prompt Engineering Interactive Tutorial + the DAIR.AI Prompt Engineering Guide.*
