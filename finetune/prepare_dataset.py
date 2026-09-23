"""
Convert curated code examples into an instruction-tuning dataset
(Alpaca-style JSONL) for fine-tuning. See CLAUDE.md in this folder for the
dataset-quality rules this project follows before adding examples.

Usage:
    python prepare_dataset.py --src ./my_code_samples --out dataset.jsonl

Input format expected in --src: a folder of .txt/.md files, each containing
blocks separated by "---" like:

    ### INSTRUCTION
    Write a Go function that reverses a linked list

    ### OUTPUT
    func reverseList(head *Node) *Node { ... }

Target domains (per CLAUDE.md, in priority order): Go, Python, JavaScript/
TypeScript + React (frontend), PostgreSQL, and system-design/architecture
reasoning. Cover all five — don't only collect examples from one language.

If you don't have curated examples yet, the simplest bootstrap is:
  1. Take your best past PRs / code answers / bug fixes across the domains above.
  2. For each, write one line describing the task (instruction) and paste
     the final, verified-correct code as output.
  3. Prefer real, working examples over synthetic ones — quality beats
     quantity (500 verified examples beat 5000 unverified ones).
  4. Aim for 300-1000 examples minimum for a noticeable fine-tune effect,
     spread across all five domains.
"""
import argparse
import json
import re
from pathlib import Path

BLOCK_RE = re.compile(
    r"###\s*INSTRUCTION\s*\n(.*?)\n###\s*OUTPUT\s*\n(.*?)(?=\n###\s*INSTRUCTION|\Z)",
    re.DOTALL,
)


def parse_file(path: Path):
    text = path.read_text(encoding="utf-8")
    examples = []
    for m in BLOCK_RE.finditer(text):
        instruction = m.group(1).strip()
        output = m.group(2).strip()
        if instruction and output:
            examples.append({"instruction": instruction, "input": "", "output": output})
    return examples


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="Folder with raw instruction/output text files")
    ap.add_argument("--out", default="dataset.jsonl")
    args = ap.parse_args()

    src = Path(args.src)
    all_examples = []
    for f in src.rglob("*.txt"):
        all_examples.extend(parse_file(f))
    for f in src.rglob("*.md"):
        all_examples.extend(parse_file(f))

    if not all_examples:
        raise SystemExit(f"No examples found in {src}. Check the ### INSTRUCTION / ### OUTPUT format.")

    with open(args.out, "w", encoding="utf-8") as f:
        for ex in all_examples:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")

    print(f"Wrote {len(all_examples)} examples to {args.out}")


if __name__ == "__main__":
    main()
