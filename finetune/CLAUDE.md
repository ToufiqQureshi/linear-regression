# Rules for working in this folder

This folder builds a coding-specialized small language model (SLM) to replace
paid coding APIs. Any agent (Claude or otherwise) working here must follow
these rules, in this priority order.

## Base model
`zai-org/GLM-4-9B-0414` (Zhipu AI / GLM4 architecture, MIT license).
Do not swap the base model without updating this file and explaining why in
the same commit.

## Priority order (highest first)

1. **Size reduction without breaking capability.** Before adding features,
   before chasing higher benchmark scores, before anything else: is there a
   way to make the deployed model smaller that does NOT measurably hurt
   coding quality? Try in this order, cheapest/safest first:
   - GGUF Q4_K_M (research shows ~0.5% perplexity loss, safe default)
   - AWQ 4-bit (activation-aware, retains ~95-97% of fp16 quality, better
     than GPTQ on hard reasoning/instruction-following)
   - GPTQ 4-bit (fallback if AWQ tooling doesn't support GLM4 yet)
   - Never go below 4-bit (3-bit/2-bit) — research consistently shows real,
     noticeable degradation on code generation below this point.
   - After any quantization change, benchmark before/after on a held-out
     set of real coding tasks (see Evaluation below) and record the numbers
     in this file's changelog before merging.

2. **Dataset quality over dataset size.** A coding agent working on this
   project must curate the training dataset itself — don't grab a generic
   public instruction dataset and call it done. Source examples from:
   - Real, working code across: **Go, Python, JavaScript/TypeScript, React
     (frontend), PostgreSQL** (schema design, queries, migrations)
   - System design / architecture reasoning (not just syntax — "why", not
     just "what")
   - Bug-fix pairs (broken code -> instruction -> fixed code) — these teach
     debugging, not just generation
   - Prefer real repos/PRs/code reviews over synthetic Q&A when possible;
     synthetic examples should be reviewed for correctness before inclusion
   - Target: quality > quantity. 500 verified-correct examples beat 5000
     unverified ones.

3. **Capability breadth**, in this priority: Go and Python first (most
   requested), then JavaScript/TypeScript + React, then PostgreSQL, then
   general system-design reasoning. Don't sacrifice an earlier item's
   quality to add a later one.

## Continuous improvement

Periodically (each time this project is revisited), search for and read new
research on:
- Low-bit quantization methods for LLMs (arXiv, HF blog) — is there a newer
  technique that keeps more capability at the same size, or the same
  capability at a smaller size?
- Small-model fine-tuning techniques (LoRA rank selection, QLoRA variants,
  distillation from larger coding models)

Summarize anything actionable as a short note + source link in the
changelog below before changing the pipeline based on it. Don't change the
pipeline on a paper's claims alone — validate on this project's eval set
first.

## Evaluation before shipping any change

Before merging a change to the base model, dataset, or quantization method,
run the fine-tuned model against a fixed set of held-out coding prompts
covering all five domains above and compare pass/fail + code correctness
against the previous version. Never ship a smaller model that regresses on
this eval set without saying so explicitly.

## Changelog

- (empty — add an entry here each time size/dataset/quantization changes,
  with what changed, why, and the eval result)
